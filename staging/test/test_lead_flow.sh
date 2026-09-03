#!/usr/bin/env bash
# End-to-end test for ALU-ON lead flow (TEST only)
# No PII, no external sends, no production
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STAGING="$(cd "$SCRIPT_DIR/.." && pwd)"
ENDPOINT="$STAGING/endpoint/lead_endpoint.py"
DB="$STAGING/db/leads.db"
NOTIFY_LOG="$STAGING/notify/notifications.jsonl"
LEAD_LOG="$STAGING/notify/lead_log.jsonl"
PORT=8787
PASS=0
FAIL=0

assert_eq() {
  local test_name="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    echo "  ✅ $test_name"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $test_name — expected='$expected' actual='$actual'"
    FAIL=$((FAIL + 1))
  fi
}

assert_contains() {
  local test_name="$1" needle="$2" haystack="$3"
  if echo "$haystack" | grep -q "$needle"; then
    echo "  ✅ $test_name"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $test_name — '$needle' not found"
    FAIL=$((FAIL + 1))
  fi
}

cleanup() {
  # Kill server if running
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  # Clean test data
  rm -f "$DB" "$NOTIFY_LOG" "$LEAD_LOG"
}

trap cleanup EXIT

echo "=== ALU-ON Lead Flow — End-to-End Test ==="
echo ""

# Clean slate
rm -f "$DB" "$NOTIFY_LOG" "$LEAD_LOG"

# Start server in background
echo "[Setup] Starting endpoint server on port $PORT..."
python3 "$ENDPOINT" "$PORT" &
SERVER_PID=$!
sleep 1

# Verify server is running
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
  echo "❌ Server failed to start"
  exit 1
fi
echo "[Setup] Server running (PID=$SERVER_PID)"
echo ""

# --- Test 1: Valid lead ---
echo "[Test 1] Valid TEST lead"
RESP=$(curl -s -w "\n%{http_code}" -X POST "http://127.0.0.1:$PORT/aluon/v1/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"TEST","phone":"0500000000","service_type":"aluminum","source":"contact","page_url":"/test"}')
HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | head -n -1)

assert_eq "HTTP 201" "201" "$HTTP_CODE"
assert_contains "success=true" '"success": true' "$BODY"
assert_contains "has lead_id" '"lead_id"' "$BODY"
assert_contains "dispatch=SENT" '"dispatch_status": "SENT"' "$BODY"

LEAD_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['lead_id'])" 2>/dev/null || echo "")
assert_contains "lead_id is UUID" "-" "$LEAD_ID"
echo ""

# --- Test 2: DB verification ---
echo "[Test 2] DB contains lead"
DB_COUNT=$(python3 -c "
import sqlite3
conn = sqlite3.connect('$DB')
count = conn.execute('SELECT COUNT(*) FROM leads').fetchone()[0]
print(count)
conn.close()
")
assert_eq "DB has 1 lead" "1" "$DB_COUNT"

DB_NAME=$(python3 -c "
import sqlite3
conn = sqlite3.connect('$DB')
name = conn.execute('SELECT name FROM leads').fetchone()[0]
print(name)
conn.close()
")
assert_eq "Lead name=TEST" "TEST" "$DB_NAME"
echo ""

# --- Test 3: Mock notification logged ---
echo "[Test 3] Mock notification"
NOTIFY_COUNT=$(wc -l < "$NOTIFY_LOG" 2>/dev/null || echo "0")
assert_eq "notifications.jsonl has 1 entry" "1" "$NOTIFY_COUNT"
assert_contains "channel=MOCK" '"channel": "MOCK"' "$(cat "$NOTIFY_LOG" 2>/dev/null)"
echo ""

# --- Test 4: Invalid phone ---
echo "[Test 4] Invalid phone → rejection"
RESP=$(curl -s -w "\n%{http_code}" -X POST "http://127.0.0.1:$PORT/aluon/v1/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"BAD","phone":"123","service_type":"hpl"}')
HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | head -n -1)

assert_eq "HTTP 422" "422" "$HTTP_CODE"
assert_contains "success=false" '"success": false' "$BODY"
assert_contains "phone error" "phone" "$BODY"

DB_COUNT_AFTER=$(python3 -c "
import sqlite3
conn = sqlite3.connect('$DB')
count = conn.execute('SELECT COUNT(*) FROM leads').fetchone()[0]
print(count)
conn.close()
")
assert_eq "DB still has 1 lead (bad one rejected)" "1" "$DB_COUNT_AFTER"
echo ""

# --- Test 5: Missing name ---
echo "[Test 5] Missing name → rejection"
RESP=$(curl -s -w "\n%{http_code}" -X POST "http://127.0.0.1:$PORT/aluon/v1/lead" \
  -H "Content-Type: application/json" \
  -d '{"phone":"0501234567"}')
HTTP_CODE=$(echo "$RESP" | tail -1)
assert_eq "HTTP 422" "422" "$HTTP_CODE"
echo ""

# --- Test 6: Invalid JSON ---
echo "[Test 6] Invalid JSON → 400"
RESP=$(curl -s -w "\n%{http_code}" -X POST "http://127.0.0.1:$PORT/aluon/v1/lead" \
  -H "Content-Type: application/json" \
  -d 'NOT JSON')
HTTP_CODE=$(echo "$RESP" | tail -1)
assert_eq "HTTP 400" "400" "$HTTP_CODE"
echo ""

# --- Test 7: 404 on wrong path ---
echo "[Test 7] Wrong endpoint → 404"
RESP=$(curl -s -w "\n%{http_code}" -X POST "http://127.0.0.1:$PORT/wrong/path" \
  -H "Content-Type: application/json" \
  -d '{}')
HTTP_CODE=$(echo "$RESP" | tail -1)
assert_eq "HTTP 404" "404" "$HTTP_CODE"
echo ""

# --- Test 8: Retry mechanism ---
echo "[Test 8] Retry failed dispatches"
# Insert a FAILED lead directly
python3 -c "
import sqlite3, uuid
from datetime import datetime, timezone
conn = sqlite3.connect('$DB')
conn.execute('''INSERT INTO leads
    (lead_id, created_at, name, phone, service_type, status, dispatch_status, retry_count)
    VALUES (?, ?, 'RETRY_TEST', '0509999999', 'hpl', 'NEW', 'FAILED', 0)''',
    (str(uuid.uuid4()), datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')))
conn.commit()
conn.close()
"

# Run retry
python3 -c "
import sys
sys.path.insert(0, '$STAGING/endpoint')
from lead_endpoint import retry_failed, init_db
init_db()
results = retry_failed()
for r in results:
    print(f'  retry: lead_id={r[\"lead_id\"][:8]}... status={r[\"status\"]}')
"

FAILED_COUNT=$(python3 -c "
import sqlite3
conn = sqlite3.connect('$DB')
count = conn.execute(\"SELECT COUNT(*) FROM leads WHERE dispatch_status='FAILED'\").fetchone()[0]
print(count)
conn.close()
")
assert_eq "No FAILED leads after retry" "0" "$FAILED_COUNT"

SENT_COUNT=$(python3 -c "
import sqlite3
conn = sqlite3.connect('$DB')
count = conn.execute(\"SELECT COUNT(*) FROM leads WHERE dispatch_status='SENT'\").fetchone()[0]
print(count)
conn.close()
")
assert_eq "All leads now SENT" "2" "$SENT_COUNT"
echo ""

# --- Test 9: Second valid lead (duplicates) ---
echo "[Test 9] Second valid lead"
RESP=$(curl -s -w "\n%{http_code}" -X POST "http://127.0.0.1:$PORT/aluon/v1/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"TEST2","phone":"0501111111","service_type":"curtain-walls","source":"calculator"}')
HTTP_CODE=$(echo "$RESP" | tail -1)
assert_eq "HTTP 201" "201" "$HTTP_CODE"

TOTAL=$(python3 -c "
import sqlite3
conn = sqlite3.connect('$DB')
count = conn.execute('SELECT COUNT(*) FROM leads').fetchone()[0]
print(count)
conn.close()
")
assert_eq "DB has 3 leads total" "3" "$TOTAL"
echo ""

# --- Test 10: Lead log has entries ---
echo "[Test 10] Lead event log"
LOG_COUNT=$(wc -l < "$LEAD_LOG" 2>/dev/null || echo "0")
assert_contains "lead_log.jsonl has entries" "1" "$([ "$LOG_COUNT" -gt 0 ] && echo 1 || echo 0)"
echo ""

# --- Summary ---
echo "=== Results: $PASS passed, $FAIL failed ==="
echo ""
echo "=== Evidence ==="
echo "DB path: $DB"
echo "Notifications: $NOTIFY_LOG"
echo "Lead log: $LEAD_LOG"

# Final DB dump
echo ""
echo "=== DB Contents ==="
python3 -c "
import sqlite3
conn = sqlite3.connect('$DB')
conn.row_factory = sqlite3.Row
rows = conn.execute('SELECT lead_id, name, phone, service_type, status, dispatch_status, retry_count FROM leads').fetchall()
print(f'{'lead_id':36} | {'name':12} | {'phone':10} | {'service':14} | {'status':6} | {'dispatch':8} | retry')
print('-' * 105)
for r in rows:
    print(f'{r[\"lead_id\"]:36} | {r[\"name\"]:12} | {r[\"phone\"]:10} | {str(r[\"service_type\"]):14} | {r[\"status\"]:6} | {r[\"dispatch_status\"]:8} | {r[\"retry_count\"]}')
conn.close()
"

exit $FAIL

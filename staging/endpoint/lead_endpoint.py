"""
ALU-ON Lead Endpoint — TEST / Staging Only
No production, no real PII, no external sends.
Python stdlib only — no pip installs.
"""
import sqlite3
import json
import uuid
import os
import re
from datetime import datetime, timezone

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'db', 'leads.db')
NOTIFY_LOG = os.path.join(BASE_DIR, '..', 'notify', 'notifications.jsonl')
LEAD_LOG = os.path.join(BASE_DIR, '..', 'notify', 'lead_log.jsonl')


def init_db():
    """Create leads table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            lead_id         TEXT PRIMARY KEY,
            created_at      TEXT NOT NULL,
            name            TEXT NOT NULL,
            phone           TEXT NOT NULL,
            service_type    TEXT,
            source          TEXT,
            page_url        TEXT,
            status          TEXT DEFAULT 'NEW',
            dispatch_status TEXT DEFAULT 'PENDING',
            dispatch_error  TEXT,
            dispatch_at     TEXT,
            retry_count     INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def validate_lead(data):
    """Validate lead data. Returns (is_valid, errors)."""
    errors = []
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()

    if not name:
        errors.append('name is required')
    if not phone:
        errors.append('phone is required')
    elif not re.match(r'^0\d{9}$', phone):
        errors.append('phone must be 10 digits starting with 0')

    return len(errors) == 0, errors


def mock_notify(lead_id, name, phone, service_type):
    """Mock notification — writes to file, sends nothing externally."""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    entry = {
        'ts': ts,
        'lead_id': lead_id,
        'name': name,
        'phone': phone,
        'service': service_type,
        'channel': 'MOCK',
        'status': 'delivered'
    }
    os.makedirs(os.path.dirname(NOTIFY_LOG), exist_ok=True)
    with open(NOTIFY_LOG, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    return True, None


def log_event(event_type, lead_id, detail):
    """Append to lead event log."""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    entry = {
        'ts': ts,
        'event': event_type,
        'lead_id': lead_id,
        'detail': detail
    }
    os.makedirs(os.path.dirname(LEAD_LOG), exist_ok=True)
    with open(LEAD_LOG, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def create_lead(data):
    """
    Full lead creation flow:
    1. Validate
    2. Generate lead_id
    3. Insert to DB
    4. Mock notify
    5. Update dispatch status
    6. Return result

    Returns dict with lead_id, status, dispatch_status, or errors.
    """
    # Validate
    is_valid, errors = validate_lead(data)
    if not is_valid:
        log_event('VALIDATION_FAILED', None, {'errors': errors, 'input': data})
        return {
            'success': False,
            'errors': errors,
            'lead_id': None
        }

    # Generate ID and timestamp
    lead_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    name = data['name'].strip()
    phone = data['phone'].strip()
    service_type = data.get('service_type', '').strip() or None
    source = data.get('source', '').strip() or None
    page_url = data.get('page_url', '').strip() or None

    # Insert to DB
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            '''INSERT INTO leads
               (lead_id, created_at, name, phone, service_type, source, page_url,
                status, dispatch_status, retry_count)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'NEW', 'PENDING', 0)''',
            (lead_id, created_at, name, phone, service_type, source, page_url)
        )
        conn.commit()
        log_event('LEAD_CREATED', lead_id, {'name': name, 'phone': phone})
    except Exception as e:
        conn.rollback()
        log_event('DB_ERROR', lead_id, {'error': str(e)})
        return {
            'success': False,
            'errors': [f'DB error: {e}'],
            'lead_id': lead_id
        }

    # Mock notify
    notify_ok, notify_err = mock_notify(lead_id, name, phone, service_type)

    # Update dispatch status
    dispatch_status = 'SENT' if notify_ok else 'FAILED'
    dispatch_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    conn.execute(
        '''UPDATE leads SET dispatch_status=?, dispatch_at=?, dispatch_error=?
           WHERE lead_id=?''',
        (dispatch_status, dispatch_at, notify_err, lead_id)
    )
    conn.commit()
    conn.close()

    log_event('DISPATCH_' + dispatch_status, lead_id, {
        'channel': 'MOCK',
        'error': notify_err
    })

    return {
        'success': True,
        'lead_id': lead_id,
        'status': 'NEW',
        'dispatch_status': dispatch_status
    }


def retry_failed(max_retries=3):
    """
    Retry failed dispatches.
    Returns list of results.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    failed = conn.execute(
        "SELECT * FROM leads WHERE dispatch_status='FAILED' AND retry_count < ?",
        (max_retries,)
    ).fetchall()

    results = []
    for lead in failed:
        lead_id = lead['lead_id']
        retry_count = lead['retry_count'] + 1

        notify_ok, notify_err = mock_notify(
            lead_id, lead['name'], lead['phone'], lead['service_type']
        )

        if notify_ok:
            conn.execute(
                '''UPDATE leads SET dispatch_status='SENT',
                   dispatch_at=?, retry_count=?, dispatch_error=NULL
                   WHERE lead_id=?''',
                (datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                 retry_count, lead_id)
            )
            log_event('RETRY_SUCCESS', lead_id, {'attempt': retry_count})
        else:
            new_status = 'DEAD_LETTER' if retry_count >= max_retries else 'FAILED'
            conn.execute(
                '''UPDATE leads SET dispatch_status=?, retry_count=?,
                   dispatch_error=? WHERE lead_id=?''',
                (new_status, retry_count, notify_err, lead_id)
            )
            log_event('RETRY_FAILED', lead_id, {
                'attempt': retry_count,
                'new_status': new_status
            })

        results.append({
            'lead_id': lead_id,
            'retry_count': retry_count,
            'status': 'SENT' if notify_ok else ('DEAD_LETTER' if retry_count >= max_retries else 'FAILED')
        })

    conn.commit()
    conn.close()
    return results


# HTTP server for POST /lead
if __name__ == '__main__':
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import sys

    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8787

    init_db()

    class LeadHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path != '/aluon/v1/lead':
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error":"not found"}')
                return

            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"invalid JSON"}')
                return

            result = create_lead(data)
            status_code = 201 if result['success'] else 422
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode())

        def log_message(self, format, *args):
            pass  # Suppress default HTTP logging

    print(f'Lead endpoint running on http://localhost:{PORT}/aluon/v1/lead')
    HTTPServer(('127.0.0.1', PORT), LeadHandler).serve_forever()

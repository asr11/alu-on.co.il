DROP TABLE IF EXISTS leads;
CREATE TABLE leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  phone TEXT,
  service TEXT,
  notes TEXT,
  gclid TEXT,
  utm_source TEXT,
  utm_campaign TEXT,
  utm_medium TEXT,
  landing_path TEXT,
  session_id TEXT,
  status TEXT DEFAULT 'new',
  deal_value REAL,
  revenue REAL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

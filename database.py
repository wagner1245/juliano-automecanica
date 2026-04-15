
import sqlite3
from config import DB_PATH

def db():
    return sqlite3.connect(DB_PATH)

def init_db():
    con = db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpf TEXT,
    name TEXT NOT NULL,
    address TEXT,
    district TEXT,
    city TEXT,
    phone TEXT,
    vehicle TEXT,
    mileage TEXT,
    plate TEXT,
    color TEXT,
    year TEXT,
    created_at TEXT NOT NULL
)
""")
    
    cur.execute("PRAGMA table_info(clients)")
    client_cols = [row[1] for row in cur.fetchall()]

    if "address" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN address TEXT")

    if "district" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN district TEXT")

    if "city" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN city TEXT")

    if "phone" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN phone TEXT")

    if "vehicle" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN vehicle TEXT")

    if "mileage" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN mileage TEXT")

    if "plate" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN plate TEXT")
    
    if "color" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN color TEXT")

    if "year" not in client_cols:
        cur.execute("ALTER TABLE clients ADD COLUMN year TEXT")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS services(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        quantity REAL NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        created_at TEXT,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Aberto',
        notes TEXT,
        total REAL NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        service_id INTEGER,
        description TEXT NOT NULL,
        quantity REAL NOT NULL DEFAULT 1,
        unit_price REAL NOT NULL DEFAULT 0,
        line_total REAL NOT NULL DEFAULT 0,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(service_id) REFERENCES services(id)
    )
    """)

    cur.execute("PRAGMA table_info(services)")
    cols = [row[1] for row in cur.fetchall()]

    if "client_id" not in cols:
        cur.execute("ALTER TABLE services ADD COLUMN client_id INTEGER")

    if "created_at" not in cols:
        cur.execute("ALTER TABLE services ADD COLUMN created_at TEXT")

    con.commit()
    con.close()

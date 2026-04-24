import sqlite3
from config import DB_PATH


def db():
    return sqlite3.connect(DB_PATH)


def add_column_if_not_exists(cur, table_name, column_name, column_definition):
    """
    Adiciona uma coluna somente se ela ainda não existir na tabela.
    Evita erro quando o sistema for aberto várias vezes.
    """
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cur.fetchall()]

    if column_name not in cols:
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")


def init_db():
    con = db()
    cur = con.cursor()

    # Tabela principal de clientes
    # IMPORTANTE:
    # Ela precisa ser criada antes de qualquer ALTER TABLE em clients.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cpf TEXT,
        address TEXT,
        district TEXT,
        city TEXT,
        phone TEXT,
        vehicle TEXT,
        mileage TEXT,
        plate TEXT,
        color TEXT,
        year TEXT,
        notes TEXT,
        created_at TEXT
    )
    """)

    # Tabela de orçamentos enviados
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orcamentos_enviados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_nome TEXT,
        telefone TEXT,
        veiculo TEXT,
        caminho_imagem TEXT,
        mao_de_obra TEXT,
        total_pecas TEXT,
        total_servicos TEXT,
        data_criacao TEXT,
        status_envio TEXT
    )
    """)

    # Garante compatibilidade com bancos antigos que não tinham essas colunas
    add_column_if_not_exists(cur, "clients", "cpf", "TEXT")
    add_column_if_not_exists(cur, "clients", "address", "TEXT")
    add_column_if_not_exists(cur, "clients", "district", "TEXT")
    add_column_if_not_exists(cur, "clients", "city", "TEXT")
    add_column_if_not_exists(cur, "clients", "phone", "TEXT")
    add_column_if_not_exists(cur, "clients", "vehicle", "TEXT")
    add_column_if_not_exists(cur, "clients", "mileage", "TEXT")
    add_column_if_not_exists(cur, "clients", "plate", "TEXT")
    add_column_if_not_exists(cur, "clients", "color", "TEXT")
    add_column_if_not_exists(cur, "clients", "year", "TEXT")
    add_column_if_not_exists(cur, "clients", "notes", "TEXT")
    add_column_if_not_exists(cur, "clients", "created_at", "TEXT")

    # Tabela de serviços
    cur.execute("""
    CREATE TABLE IF NOT EXISTS services(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        quantity REAL NOT NULL DEFAULT 1,
        description TEXT NOT NULL,
        price REAL NOT NULL DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    """)

    # Tabela de ordens
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

    # Itens da ordem
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

    # Garante compatibilidade com bancos antigos da tabela services
    add_column_if_not_exists(cur, "services", "client_id", "INTEGER")
    add_column_if_not_exists(cur, "services", "created_at", "TEXT")

    con.commit()
    con.close()

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from src.core.config import DATA_DIR, DATABASE_URL

# Garante que o diretório de dados exista
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Cria a conexão com o banco de dados
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Habilita a integridade referencial no SQLite
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Fábrica de sessões do banco de dados
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False, 
)
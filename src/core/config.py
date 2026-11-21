from pathlib import Path

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).resolve().parents[2]

# Diretório destinado aos dados persistidos
DATA_DIR = ROOT_DIR / "data"

# Caminho para o banco de dados
DATABASE_URL = f"sqlite:///{DATA_DIR / 'app.db'}"

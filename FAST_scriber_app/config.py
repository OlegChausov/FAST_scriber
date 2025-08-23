from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "audio"
DB_PATH = BASE_DIR.parent / "transcriber.db"
TEXT_DIR = STATIC_DIR / "text"
SQLITE_URL = f"sqlite:///{DB_PATH}"
IMAGES_DIR = STATIC_DIR / "images"

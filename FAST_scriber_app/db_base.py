#этот файл нужен только для того, чтобы database.by и models.py делали импорт отсюда,
#иначе проблема - петля импорта

from sqlalchemy.orm import declarative_base

Base = declarative_base()
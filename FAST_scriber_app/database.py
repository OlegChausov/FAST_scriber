from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from FAST_scriber_app.config import SQLITE_URL
from FAST_scriber_app.db_base import Base


# ✅ Создаём движок подключения
engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False}
)

# ✅ Сессия для общения с БД
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🛠️ (Опционально) Создание таблиц - УДАЛИТЬ ПОСЛЕ ПЕРЕХОДА НА АЛЕМБИК, но мы сохраним, просто закомментируем вызов init_db в main.py
def init_db():
    Base.metadata.create_all(bind=engine)
# 🛠️ (Опционально) Создание таблиц - УДАЛИТЬ ПОСЛЕ ПЕРЕХОДА НА АЛЕМБИК
if __name__ == "__main__":
    print("🚀 Запуск инициализации базы данных...")
    init_db()
    print("✅ Таблицы успешно созданы.")

from FAST_scriber_app.config import BASE_DIR, TEMPLATES_DIR
from FAST_scriber_app.routers import all_routers
from fastapi.staticfiles import StaticFiles
import asyncio
from fastapi import FastAPI
from FAST_scriber_app.database import SessionLocal
from FAST_scriber_app.deleteon_and_scedule_cleaning import scedule_selfcleaninig



#init_db()
app = FastAPI()

#подключаем статику
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")




#подключаем все роутеры из routers/__init__.py
for r in all_routers:
    app.include_router(r)


#Да, on_event("startup") помечен как deprecated
#Но он всё ещё работает, и FastAPI не удалит его внезапно. 
@app.on_event("startup")
async def start_cleanup_loop():
    async def loop():
        while True:
            try:
                db = SessionLocal()
                await scedule_selfcleaninig(db)
                db.close()
            except Exception as e:
                print(f"Ошибка при очистке: {e}")
            await asyncio.sleep(600)  # 10 минут

    asyncio.create_task(loop())

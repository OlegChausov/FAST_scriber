from datetime import datetime, UTC
from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile
from fastapi import Depends
from sqlalchemy.orm import Session
router = APIRouter()



@router.get("/move-to-bin/{item_id}", summary="Отправка единичного объекта в корзину")
def move_to_bin(item_id: str, db: Session = Depends(get_db)):
    item = db.query(AudioFile).filter(AudioFile.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Файл не найден")

    item.in_bin = True
    item.time_of_throwing_to_bin = datetime.now(UTC)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
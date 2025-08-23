from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile

router = APIRouter()

@router.get("/restore/{item_id}", summary="Восстановление единичного объекта из корзины")
def restore_from_bin(item_id: str, db: Session = Depends(get_db)):
    print(f'restoring of {item_id} object')
    # item = db.query(AudioFile).filter(AudioFile.id == item_id).first() #аналогично
    item = db.get(AudioFile, item_id)
    if not item or not item.in_bin:
        raise HTTPException(status_code=404, detail="Файл не найден в корзине")

    item.in_bin = False
    item.time_of_throwing_to_bin = None
    db.commit()
    return RedirectResponse(url="/bin", status_code=303)
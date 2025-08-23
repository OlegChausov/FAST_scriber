from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from starlette.concurrency import run_in_threadpool
from FAST_scriber_app.config import TEMPLATES_DIR, UPLOAD_DIR, TEXT_DIR
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/delete-single-manual/{item_id}", summary="Окончательное удаление единичного объекта")
async def delete_single_manual(item_id: str, db: Session = Depends(get_db)):
    print(f"Попытка удалить файл: {item_id}")
    # obj = db.query(AudioFile).filter(AudioFile.id == item_id).first()
    obj = db.get(AudioFile, item_id)
    if not obj:
        print(f"Попытка удалить несуществующий объект: {item_id}")
        raise HTTPException(status_code=404, detail="Файл не найден")
    print(f"Попытка удалить файл: {item_id}")
    file_to_delete = UPLOAD_DIR / obj.audio_uuid_name

    if not file_to_delete.exists():
        raise HTTPException(status_code=404, detail=f"{obj.original_filename} file missing")

    if obj.transcript_uuid_name:
        transcription_to_delete = TEXT_DIR / obj.transcript_uuid_name
        if transcription_to_delete.exists():
            await run_in_threadpool(transcription_to_delete.unlink)

    await run_in_threadpool(file_to_delete.unlink)
    db.delete(obj)
    db.commit()

    return RedirectResponse(url="/bin", status_code=303)
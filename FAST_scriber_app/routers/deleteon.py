from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from uuid import UUID

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from FAST_scriber_app.config import UPLOAD_DIR, TEXT_DIR
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile

router = APIRouter()

@router.get("/delete/{audio_id}", summary="Удаление единичного объекта")
async def delete_audio(audio_id: UUID, db: Session = Depends(get_db)):
    obj = db.get(AudioFile, audio_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Audio record not found")

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
    return RedirectResponse("/", status_code=303)

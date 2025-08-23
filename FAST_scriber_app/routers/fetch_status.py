from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile

router = APIRouter()


@router.get("/status/{audio_id}", summary="Обновление статусов состояния объектов")
async def get_transcription_status(audio_id: str, db: Session = Depends(get_db)):
    audio = db.get(AudioFile, audio_id)

    if not audio:
        return {"status": "Missing"}

    return {"status": audio.is_transcript_ready}



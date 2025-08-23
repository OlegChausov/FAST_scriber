from sqlalchemy.orm import Session
import logging

from starlette.concurrency import run_in_threadpool

from FAST_scriber_app.config import UPLOAD_DIR, TEXT_DIR
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile

logger = logging.getLogger("fastapi_app")

async def scedule_selfcleaninig ( db: Session ):

    items = db.query(AudioFile).filter(AudioFile.in_bin == True).all()
    for obj in items:
        if obj.is_expired == True:
            file_to_delete = UPLOAD_DIR / obj.audio_uuid_name

            if not file_to_delete.exists():
                logger.error(f"Файл для объекта {obj.id} не найден: {file_to_delete}")

            if obj.transcript_uuid_name:
                transcription_to_delete = TEXT_DIR / obj.transcript_uuid_name
                if transcription_to_delete.exists():
                    await run_in_threadpool(transcription_to_delete.unlink)

            await run_in_threadpool(file_to_delete.unlink)
            db.delete(obj)
            db.commit()



import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from starlette.responses import RedirectResponse
from datetime import datetime, timezone
from FAST_scriber_app.config import UPLOAD_DIR, TEXT_DIR
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile
import json
from FAST_scriber_app.transcriber import transcribe
router = APIRouter()


@router.get("/transcribe/{audio_id}", summary="Транскрибация единичного объекта")
async def transcribe_audio(
    audio_id: str,
    selected_model: str = Query("base"),
    db: Session = Depends(get_db)
):
    audio = db.get(AudioFile, audio_id)
    if not audio:
        raise HTTPException(status_code=404, detail="Файл не найден")

    if audio.transcript_uuid_name:
        old_path = TEXT_DIR / audio.transcript_uuid_name
        if old_path.exists():
            try:
                old_path.unlink()
            except Exception as e:
                print(f'Ошибка удаления старого транскрипта для {audio.id}: {e}')
                audio.is_transcript_ready = None
                audio.transcribed_at = None
                db.commit()
                #продолжаем
        audio.transcript_uuid_name = None #очистим место для нового файла
        print(f'{audio.id} транскрипт будет заменен')

    audio.is_transcript_ready = "In process"
    db.commit()

    start_time = datetime.now()
    path = UPLOAD_DIR / audio.audio_uuid_name

    try:
        text = await run_in_threadpool(transcribe, str(path), selected_model)
    except Exception as e:
        audio.is_transcript_ready = "Failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Ошибка транскрипции: {e}")

    # Сохраняем транскрипт в JSON
    transcript_uuid = f"{uuid.uuid4()}.json"
    transcript_path = TEXT_DIR / transcript_uuid
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump({"text": text}, f, ensure_ascii=False, indent=2)

    # Обновляем объект

    audio.transcribed_at = datetime.now(timezone.utc)
    audio.transcript_uuid_name = transcript_uuid # перезаписываем старую ссылку
    audio.is_transcript_ready = "Done"
    db.commit()
    time_of_processing = datetime.now() - start_time
    print(f'{time_of_processing} секунд')
    return RedirectResponse(url="/", status_code=303)


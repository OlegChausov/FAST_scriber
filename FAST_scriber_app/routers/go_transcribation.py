from fastapi.responses import HTMLResponse
from fastapi import Request, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
import json
from FAST_scriber_app.config import UPLOAD_DIR, TEXT_DIR, TEMPLATES_DIR
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile
from FAST_scriber_app.utils.template_functions import seconds_to_mmss

from FAST_scriber_app.utils.template_functions import templates
templates.env.filters["mmss"] = seconds_to_mmss
router = APIRouter()

@router.get("/go_transcribation/{audio_id}", response_class=HTMLResponse, summary="Просмотр и редактирование объекта")
async def transcribe_audio_view(audio_id: str, request: Request, db: Session = Depends(get_db)):
    obj = db.get(AudioFile, audio_id)
    if not obj or not obj.transcript_uuid_name:
        raise HTTPException(status_code=404, detail="Транскрипт не найден")

    transcript_path = TEXT_DIR / obj.transcript_uuid_name

    transcript_path = TEXT_DIR / obj.transcript_uuid_name
    if not transcript_path.exists():
        raise HTTPException(status_code=404, detail="Файл транскрипта не найден")

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)
    # print(transcript_data['text']['segments'][0])
    return templates.TemplateResponse(
        "transcription.html",
        {
            "request": request,
            "transcript": transcript_data,
            "audio": obj  # чтобы получить имя файла
        }
    )


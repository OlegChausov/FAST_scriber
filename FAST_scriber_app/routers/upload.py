from typing import List
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from uuid import uuid4
import aiofiles
import time
from starlette.concurrency import run_in_threadpool
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile
from FAST_scriber_app.config import TEMPLATES_DIR, UPLOAD_DIR
from FAST_scriber_app.utils.preprocessing import convert_to_wav_16k_mono

router = APIRouter()



@router.post("/upload", summary="Загрузка и конвертация аудиофайлов")
async def upload_audio(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):

    for file in files:
        try:
            print(f"[UPLOAD] Получен файл: {file.filename}")
            temp_name = f"{uuid4()}_{file.filename}"
            temp_path = UPLOAD_DIR / temp_name

            # Сохраняем временный файл
            async with aiofiles.open(temp_path, "wb") as out_file:
                while chunk := await file.read(1024 * 1024):
                    await out_file.write(chunk)
            print(f"[SAVE] Временный файл сохранён: {temp_path}")

            # Генерируем путь для WAV
            output_path = temp_path.with_suffix(".wav")

            # Преобразуем в WAV 16kHz mono
            start = time.time()
            convert_to_wav_16k_mono(str(temp_path), str(output_path))
            duration = time.time() - start
            print(f"[CONVERT] Конвертация завершена: {output_path.name} за {duration:.2f} сек")

            # Удаляем исходный файл
            await run_in_threadpool(temp_path.unlink)
            print(f"[CLEANUP] Исходный файл удалён: {temp_path.name}")

            # Сохраняем метаданные
            audio_record = AudioFile(
                original_filename=file.filename,
                audio_uuid_name=output_path.name,
                format="wav"
            )
            db.add(audio_record)
            db.commit()
            db.refresh(audio_record)
            print(f"[DB] Запись добавлена: ID={audio_record.id}, format={audio_record.format}")

        except Exception as e:
            print(f"[ERROR] Ошибка при обработке файла {file.filename}: {e}")

    return RedirectResponse(url="/", status_code=303)

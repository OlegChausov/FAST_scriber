from datetime import datetime, timezone
import json
from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from uuid import UUID
import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool
from FAST_scriber_app.transcriber import transcribe
from FAST_scriber_app.config import UPLOAD_DIR, TEXT_DIR
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile


router = APIRouter()

async def throw_bulk_to_bin_func(selected_ids: List, db: Session):
    success_count = 0
    fail_count = 0
    for audio_id in selected_ids:
            obj = db.get(AudioFile, audio_id)
            if obj:
                try:
                    obj.in_bin = True
                    obj.time_of_throwing_to_bin = datetime.now(timezone.utc)
                    db.add(obj)
                    db.commit()
                    success_count += 1
                except Exception as e:
                    print(f"Ошибка при удалении в корзину файла: {obj.original_filename} {e}")
                    fail_count += 1
            else:
                print(f"Файл с id {audio_id} не найден для удаления в корзину")
                fail_count += 1
    return success_count, fail_count


async def transcribe_bulk_func(selected_ids: List, db: Session, selected_model: str = "base"):
    success_count = 0
    fail_count = 0
    for audio_id in selected_ids:
        obj = db.get(AudioFile, audio_id)
        if not obj:
            print(f"⚠️ Файл с id {audio_id} не найден для транскрибирования")
            fail_count += 1
            continue

        # Удаление старого транскрипта, если он есть
        old_path = TEXT_DIR / obj.transcript_uuid_name if obj.transcript_uuid_name else None
        if old_path and old_path.exists():
            try:
                old_path.unlink()
                print(f"🗑️ Удалён старый транскрипт для {obj.id}")
            except Exception as e:
                print(f"❌ Ошибка удаления транскрипта для {obj.id}: {e}")
                obj.is_transcript_ready = None
                obj.transcribed_at = None
                db.commit()

        obj.transcript_uuid_name = None  # очистим место для нового файла
        obj.is_transcript_ready = "In process"
        db.add(obj)
        db.commit()

        # Транскрипция
        path = UPLOAD_DIR / obj.audio_uuid_name
        try:
            text = await run_in_threadpool(lambda: transcribe(path, selected_model))

            transcript_uuid = f"{uuid.uuid4()}.json"
            transcript_path = TEXT_DIR / transcript_uuid

            with open(transcript_path, "w", encoding="utf-8") as f:
                json.dump({"text": text}, f, ensure_ascii=False, indent=2)

            obj.transcript_uuid_name = transcript_uuid
            obj.time_of_throwing_to_bin = datetime.now(timezone.utc)
            obj.is_transcript_ready = "Done"
            db.add(obj)
            db.commit()
            success_count += 1
            print(f"✅ Успешно транскрибирован файл {obj.original_filename}")
        except Exception as e:
            print(f"❌ Ошибка транскрипции файла {obj.original_filename}: {e}")
            obj.is_transcript_ready = "Failed"
            db.add(obj)
            db.commit()
            fail_count += 1
    return success_count, fail_count

async def restore_bulk_func(selected_ids: List, db: Session):
    success_count = 0
    fail_count = 0
    for audio_id in selected_ids:
        obj = db.get(AudioFile, audio_id)
        if obj:
            try:
                obj.in_bin = False
                obj.time_of_throwing_to_bin = None
                db.add(obj)
                db.commit()
                success_count += 1
            except Exception as e:
                print(f"Ошибка при восстановлении файла: {obj.original_filename} {e}")
                fail_count += 1
        else:
            print(f"Файл с id {audio_id} не найден для восстановления")
            fail_count += 1
    return success_count, fail_count


async def delete_bulk_func(selected_ids: List, db: Session):
    success_count = 0
    fail_count = 0
    for audio_id in selected_ids:
        obj = db.get(AudioFile, audio_id)
        if obj:
            file_to_delete = UPLOAD_DIR / obj.audio_uuid_name
            if file_to_delete.exists():
                await run_in_threadpool(file_to_delete.unlink)
            else:
                print(f"Аудиофайл не найден: {file_to_delete}")

            if obj.transcript_uuid_name:
                transcription_to_delete = TEXT_DIR / obj.transcript_uuid_name
                if transcription_to_delete.exists():
                    await run_in_threadpool(transcription_to_delete.unlink)
            db.delete(obj)
            db.commit()
            success_count += 1
        else:
            print(f"Файл с id {audio_id} не найден для удаления")
            fail_count += 1
    return success_count, fail_count


@router.post("/bulk-action", summary="Действия для группы объектов")
async def bulk_action(
    request: Request,
    selected_ids: List[str] = Form(default=[]),
    action: str = Form(...),
    db: Session = Depends(get_db),
    selected_model: str = Form("base")

):
    if not selected_ids:
        raise HTTPException(status_code=400, detail="No files selected")

#словарь действий
    actions = {
        "throw_bulk_to_bin": throw_bulk_to_bin_func,
        "transcribe_bulk": transcribe_bulk_func,
        "restore_bulk": restore_bulk_func,
        "delete_bulk": delete_bulk_func,
    }

    if action not in actions:
        raise HTTPException(status_code=400, detail="Unknown action")

    if action == "transcribe_bulk":
        success_count, fail_count = await transcribe_bulk_func(selected_ids, db, selected_model)
    else:
        success_count, fail_count = await actions[action](selected_ids, db)

    print(f"{action}: успешно обработано {success_count}, не удалось {fail_count}")
    return RedirectResponse("/", status_code=303)

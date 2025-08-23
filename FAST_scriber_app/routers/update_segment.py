from fastapi import Request, HTTPException, APIRouter
import json
from FAST_scriber_app.config import TEXT_DIR
import aiofiles

router = APIRouter()


def find_segment_by_start(start: float, segments: list):
    for segment in segments:
        try:
            seg_start = float(segment["start"])
        except (TypeError, ValueError):
            continue
        if abs(seg_start - start) < 0.01:
            return segment
    return None


@router.post("/update_segment", summary="Редактирование транскрипта по сегментам")
async def update_segment(request: Request):
    data = await request.json()
    start = data.get("start")
    text = data.get("text")
    transcript_id = data.get("transcript_id")
    transcript_path = TEXT_DIR / transcript_id

    if start is None or text is None or transcript_id is None:
        print("⚠️ Отсутствуют обязательные поля")
        raise HTTPException(status_code=400, detail="Missing required fields")


    # Шаг 1: прочитать JSON асинхронно
    try:
        async with aiofiles.open(transcript_path, "r", encoding="utf-8") as f:
            content = await f.read()
            transcript_data = json.loads(content)
    except FileNotFoundError:
        print("❌ Файл транскрипта не найден")
        raise HTTPException(status_code=404, detail="Transcript file not found")

    # Шаг 2: найти и обновить сегмент
    segment = find_segment_by_start(start, transcript_data['text']['segments'])
    if not segment:
        print(f"❌ Сегмент с start={start} не найден")
        raise HTTPException(status_code=404, detail="Segment not found")

    print(f"✏️ Старый текст сегмента: {segment['text']}")
    segment["text"] = text
    print(f"✅ Новый текст сегмента: {segment['text']}")

    # Шаг 3: сохранить обратно асинхронно
    async with aiofiles.open(transcript_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(transcript_data, ensure_ascii=False, indent=2))
    print("💾 Файл успешно сохранён")

    return {"text": segment["text"]}




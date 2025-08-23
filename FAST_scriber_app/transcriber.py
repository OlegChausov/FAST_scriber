from faster_whisper import WhisperModel

def transcribe(path: str, selected_model: str) -> dict:

    model = WhisperModel(selected_model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(path)

    result = {
        "language": info.language,
        "duration": info.duration,
        "segments": []
    }

    for segment in segments:
        result["segments"].append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })

    return result
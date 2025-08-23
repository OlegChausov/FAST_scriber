from starlette.templating import Jinja2Templates

from FAST_scriber_app.config import TEMPLATES_DIR

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

def seconds_to_mmss(seconds: float | str) -> str:
    if isinstance(seconds, str):
        if ":" in seconds:
            try:
                minutes, secs = map(int, seconds.split(":"))
                total_seconds = minutes * 60 + secs
            except ValueError:
                return "00:00"
        else:
            try:
                total_seconds = float(seconds)
            except ValueError:
                return "00:00"
    else:
        total_seconds = float(seconds)

    minutes = int(total_seconds // 60)
    secs = int(total_seconds % 60)
    return f"{minutes:02}:{secs:02}"


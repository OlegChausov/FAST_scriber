from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile
from fastapi import Depends
from sqlalchemy.orm import Session
from FAST_scriber_app.utils.template_functions import templates

router = APIRouter()





@router.get("/", response_class=HTMLResponse, summary="Главная страница")
async def render_home(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:

    items = db.query(AudioFile).filter(AudioFile.in_bin == False).order_by(AudioFile.created_at.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})



from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from FAST_scriber_app.database import get_db
from FAST_scriber_app.models import AudioFile
from sqlalchemy.orm import Session
from FAST_scriber_app.utils.template_functions import templates


router = APIRouter()


@router.get("/bin", summary="Корзина", response_class=HTMLResponse)
async def bin(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:

    items = db.query(AudioFile).filter(AudioFile.in_bin == True).order_by(AudioFile.time_of_throwing_to_bin.desc()).all()

    return templates.TemplateResponse("bin.html", {"request": request, "items": items})


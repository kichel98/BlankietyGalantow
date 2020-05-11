import codecs
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    return codecs.open("resources/index.html", "r", "utf-8").read()

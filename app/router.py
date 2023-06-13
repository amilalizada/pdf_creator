from fastapi import Request
from fastapi.param_functions import Depends, File
from fastapi.routing import APIRouter
from pydantic.types import Json
from starlette import status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.schemas import *
from app.models import User
import hashlib

router = APIRouter(prefix="", tags=["pdf"])

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def main(request: Request):
    
    return templates.TemplateResponse("main.html", {"request": request})


@router.get('/login')
def login_get(request: Request):

    return templates.TemplateResponse("log_in.html", {"request": request})


@router.post("/login")
def log_in(data: LoginInputSchema):
    print(data)
    user = User.get_or_404(User.email==data.email)

    if user.password != hashlib.sha256(data.password.encode()).hexdigest():
        return False 

    return {"ok": "ok"}


@router.get('/create')
def create_user(request: Request):

    return templates.TemplateResponse("create_user.html", {"request": request})


@router.post('/create')
def create_user(data: CreateUserInput):
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    
    user = User.create(
        fullname=data.fullname.strip(),
        email=data.email.strip(),
        password=hashed_password
    )

    return RedirectResponse(url="http://0.0.0.0:8081/api/pdf")


@router.get('/invoice-create')
def create_user(request: Request):

    return templates.TemplateResponse("invoice_create.html", {"request": request})
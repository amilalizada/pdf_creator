import hashlib
import time
import os
from fastapi import Request
from fastapi.param_functions import Depends, File
from fastapi.routing import APIRouter
from starlette import status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, Response, FileResponse
from fastapi.templating import Jinja2Templates
from app.schemas import *
from app.models import Project, User, Company
from jinja2 import Environment, FileSystemLoader
from app.utils import convert_to_pdf


router = APIRouter(prefix="", tags=["pdf"])

templates = Jinja2Templates(directory="templates")
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
print(templates_dir)
env = Environment(loader=FileSystemLoader(templates_dir))


@router.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("log_in.html", {"request": request})


@router.post("/login")
def log_in(data: LoginInputSchema):
    user = User.get_or_404(User.email == data.email)

    if user.password != hashlib.sha256(data.password.encode()).hexdigest():
        return False

    return {"ok": "ok"}


@router.get("/create")
def create_user_get(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


@router.post("/create")
def create_user(data: CreateUserInput):
    user = User.select().where(User.email == data.email)

    if user:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    user = User.create(
        full_name=data.fullname.strip(),
        email=data.email.strip(),
        password=hashed_password,
        created_at=int(time.time()),
    )

    return status.HTTP_200_OK


@router.get("/invoice-create")
def create_user_get(request: Request):
    return templates.TemplateResponse("invoice_create.html", {"request": request})


@router.post("/create-company")
def create_comp(data: CreateCompanyInputSchema):
    print(data)
    Company.create(
        name=data.name.strip(),
        address=data.address.strip(),
        location=data.location.strip(),
        created_at=int(time.time())
    )

    return status.HTTP_200_OK


@router.get("/create-company")
def create_comp_get(request: Request):

    return templates.TemplateResponse("create_company.html", {"request": request})

@router.post("/create-project")
def create_proj(data: CreateProjectInputSchema):
    
    Project.create(
        name=data.name.strip(),
        comp_id=int(data.comp_id),
        currency=data.currency.strip(),
        created_at=int(time.time())
    )

    return status.HTTP_200_OK


@router.get("/create-project")
def create_proj_get(request: Request):
    # companies = Company.select().dicts()

    # return templates.TemplateResponse("create_project.html", {"request": request, "companies": list(companies)})
    return templates.TemplateResponse("create_project.html", {"request": request})



@router.get("/create-doc")
def create_doc(request: Request):
    companies = Company.select().dicts()

    return templates.TemplateResponse("invoice_create.html", {"request": request, "companies": list(companies)})



@router.get("/projects/{comp_id}")
def get_projects(comp_id: int, request: Request):
    projects = Project.select().where(Project.comp_id == comp_id).dicts()

    return list(projects)


@router.post("/convert-invoice")
def convert_pdf(data: ConvertInvoiceInputSchema, request: Request):
    print(data)
    # company = list(Company.select().where(Company.id == data.comp_id).dicts())[0]
    # project = list(Project.select().where(Project.id == data.proj_id).dicts())[0]

    # obj = {
    #     "company_name": company["name"],
    #     "company_address": company["address"],
    #     "company_location": company["location"],
    #     "project_name": project["name"],
    #     "project_currency": project["currency"]
    # }
    obj = {
        "company_name": "Micro",
        "company_address": "ASdsdasDsadas",
        "company_location": "baku/Azerbaijan",
        "project_name": "tableau",
        "project_currency": "usd"
    }

    template = env.get_template("invoice.html")
    path = f"{templates_dir}/invoice.html"
    convert_to_pdf(templates_dir,"new.pdf", obj)


    # Render the template with the given data
    # rendered_html = template.render(data)

    # Generate a unique filename for the PDF file
    # output_path = "/path/to/output.pdf"

    # Convert HTML to PDF using pdfkit
    # pdfkit.from_string(rendered_html, output_path)

    # return FileResponse(output_path, media_type="application/pdf", filename="output.pdf")

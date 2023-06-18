import hashlib
import time
import os
import json
from fastapi import Request
from fastapi.param_functions import Depends, File
from fastapi.routing import APIRouter
from starlette import status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, Response, FileResponse
from fastapi.templating import Jinja2Templates
from app.schemas import *
from app.models import Project, User, Company, PdfData
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
    Company.create(
        name=data.name.strip(),
        address=data.address.strip(),
        location=data.location.strip(),
        tax_id=data.tax_id,
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
    # companies = list(Company.select().dicts())
    # projects = list(Project.select(Project.id, Project.name, Project.currency, Company.name.alias("company_name"))
    # .join(Company, on=Company.id == Project.comp_id)
    # .dicts())
    # , "companies": companies}

    return templates.TemplateResponse("invoice_create.html", {"request": request})



@router.get("/projects/{comp_id}")
def get_projects(comp_id: int, request: Request):
    projects = Project.select().where(Project.comp_id == comp_id).dicts()

    return list(projects)


@router.post("/convert-invoice")
def convert_pdf(data: ConvertInvoiceInputSchema, request: Request):
    
    # print(data)
    company = list(Company.select().where(Company.id == data.comp_id).dicts())[0]
    project = list(Project.select().where(Project.id == data.proj_id).dicts())[0]

    obj = {
        "company_name": company["name"],
        "company_address": company["address"],
        "company_location": company["location"],
        "company_tax": company["tax_id"],
        "project_name": project["name"],
        "project_currency": project["currency"],
        "desciptions": data.descriptions,
        "invoice_id": data.invoice_id,
        "date": data.date,
        "due_date": data.due_date
    }

    pdf_data = PdfData.create(
        data=json.dumps(obj, separators=(',', ':')),
        comp_id=data.comp_id,
        proj_id=data.proj_id,
        created_at=int(time.time())
    )

    return {"id": pdf_data.id}


@router.get("/preview/{id}")
def preview(id: int, request: Request):
    pdf_data = list(PdfData.select().where(PdfData.id == id).dicts())[0]
    company = list(Company.select().where(Company.id == pdf_data["comp_id"]).dicts())[0]
    proje = list(Project.select().where(Project.id == pdf_data["proj_id"]).dicts())[0]
    pdf_data = json.loads(pdf_data["data"])

    pdf_data["currency"] = proje["currency"]
    pdf_data["tax_id"] = company["tax_id"]
    inv_id = pdf_data["invoice_id"]
    options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None
}
    convert_to_pdf("./templates/invoice.html", f"output{inv_id}.pdf", options=options)

    return templates.TemplateResponse("invoice.html", {"request": request, "data": pdf_data})


@router.get("/admin")
def admin(request: Request):
    companies = list(Company.select().dicts())
    projects = list(Project.select(Project.id, Project.name, Project.currency, Company.name.alias("company_name"))
    .join(Company, on=Company.id == Project.comp_id)
    .dicts())

    return templates.TemplateResponse("admin.html", {"request": request, "companies": companies, "projects": projects})


@router.get("/open")
def open(request: Request):
    # companies = Company.select().dicts()

    return templates.TemplateResponse("invoice.html", {"request": request})


@router.get("/list-comps")
def open(request: Request):
    companies = list(Company.select().dicts())

    return companies
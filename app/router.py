import hashlib
from posixpath import abspath, sep
import time
import os
import json
import pdfkit
from fastapi import Request, File, UploadFile
from fastapi.param_functions import Depends, File
from fastapi.routing import APIRouter
from peewee import Ordering
from starlette import status
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    RedirectResponse,
    Response,
    FileResponse,
)
from fastapi.templating import Jinja2Templates
from app.schemas import *
from app.models import Project, User, Company, PdfData, Contract, TTAData
from jinja2 import Environment, FileSystemLoader, Template
from app.utils import convert_to_pdf, get_html_string, get_image_file_as_base64_data, get_tta_html_string, date_covnerting_to_human
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from fastapi_mail import FastMail, MessageSchema, MessageType
from core.extensions import email_conf


router = APIRouter(prefix="", tags=["pdf"])

templates = Jinja2Templates(directory="templates")
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

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
        created_at=int(time.time()),
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
        created_at=int(time.time()),
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
        "due_date": data.due_date,
    }

    pdf_data = PdfData.create(
        data=json.dumps(obj, separators=(",", ":")),
        comp_id=data.comp_id,
        proj_id=data.proj_id,
        created_at=int(time.time()),
    )

    return {"id": pdf_data.id}


@router.get("/preview/{id}")
async def preview(id: int, request: Request):
    pdf_data = list(PdfData.select().where(PdfData.id == id).dicts())[0]
    company = list(Company.select().where(Company.id == pdf_data["comp_id"]).dicts())[0]
    comp_id = pdf_data["comp_id"]
    proje = list(Project.select().where(Project.id == pdf_data["proj_id"]).dicts())[0]
    pdf_data = json.loads(pdf_data["data"])
    pdf_data["date"] = pdf_data["date"].replace("-", "/")
    pdf_data["due_date"] = pdf_data["due_date"].replace("-", "/")
    pdf_data["currency"] = proje["currency"]
    pdf_data["tax_id"] = company["tax_id"]
    final = 0
    for i in pdf_data["desciptions"]:
        final += int(i["qty"]) * int(i["unitprice"])
    total = final
    vat = final * 18 / 100
    pdf_data["vat"] = vat
    pdf_data["comp_id"] = comp_id
    pdf_data["final_amount"] = round(final + vat, 2)
    pdf_data["total"] = total
    inv_id = pdf_data["invoice_id"]
    options = {
        "page-size": "A4",
        "margin-top": "20mm",
        "margin-right": "0mm",
        "margin-bottom": "0mm",
        "margin-left": "0mm",
        "zoom": "1.0",
        "enable-local-file-access": True,
    }
    # img = get_image_file_as_base64_data()
    # print(img)
    # pdf_data["img"] = img
    html_string = get_html_string()
    html_template = Template(html_string)
    rendered_html = html_template.render(data=pdf_data)
    wkhtmltopdf_path = "/usr/local/bin/wkhtmltopdf"
    await convert_to_pdf(rendered_html, f"output{inv_id}.pdf", options=options, config_path=wkhtmltopdf_path)

    return templates.TemplateResponse(
        "invoice.html", {"request": request, "data": pdf_data}
    )


@router.get("/download/{inv_id}")
def admin(inv_id: int, request: Request):
    attach_name = f"output{inv_id}.pdf"
    print(attach_name)

    return FileResponse(
        attach_name, filename="invoice.pdf", media_type="application/pdf"
    )


@router.get("/admin")
def admin(request: Request):
    companies = list(Company.select().dicts())
    projects = list(
        Project.select(
            Project.id,
            Project.name,
            Project.currency,
            Company.name.alias("company_name"),
        )
        .join(Company, on=Company.id == Project.comp_id)
        .dicts()
    )

    return templates.TemplateResponse(
        "admin.html", {"request": request, "companies": companies, "projects": projects}
    )


@router.get("/open")
def openn(request: Request):
    # companies = Company.select().dicts()

    return templates.TemplateResponse("invoice.html", {"request": request})


@router.get("/list-comps")
def list_comps(request: Request):
    companies = list(Company.select().dicts())

    return companies


@router.get("/contract-list/{comp_id}")
def list_contracts(comp_id: int, request: Request):

    contracts = list(Contract.select().where(Contract.comp_id == comp_id).dicts())

    return contracts


@router.post("/send-email")
async def send_mail(data: SendMailInput, request: Request):
    company = list(Company.select(Company.email).where(Company.id == data.comp_id))[0]
    email = company.email
    attach_name = f"output{data.inv_id}.pdf"

    message = MessageSchema(
        subject="Invoice",
        recipients=[email],
        body="Invoice for Project",
        subtype=MessageType.html,
        attachments=[attach_name],
    )

    fm = FastMail(email_conf)
    await fm.send_message(message)

    return {"status": "ok"}


@router.get("/navigation")
async def navig(request: Request):
    return templates.TemplateResponse("navigation.html", {"request": request})


@router.get("/invoice-list")
async def navig(request: Request):
    docs = list(PdfData.select().dicts())

    response_list = []
    for doc in docs:
        data = json.loads(doc["data"])
        response_list.append(
            {
                "id": doc["id"],
                "company_name": data["company_name"],
                "project_name": data["project_name"],
                "due_date": data["due_date"],
                "date": data["date"],
                "invoice_id": data["invoice_id"],
            }
        )

    return templates.TemplateResponse(
        "inv_list.html", {"request": request, "docs": response_list}
    )


@router.get("/tta-preview/{c_id}")
async def prew_tta(c_id: int, request: Request):
    contract_doc_data = list(TTAData.select().where(TTAData.id == c_id).dicts())[0]
    company = list(Company.select().where(Company.id == contract_doc_data["comp_id"]).dicts())[0]
    contract = list(Contract.select().where(Contract.id == contract_doc_data["contract_id"]).dicts())[0]
    data = json.loads(contract_doc_data["data"])
    converted_date = date_covnerting_to_human(contract["date"])
    contract_doc_data["create_date"] = contract_doc_data["create_date"].replace("-", ".")
    doc_data = {
        "company_name": company["name"],
        "drc_name": contract_doc_data["name"],
        "date": contract_doc_data["create_date"],
        "con_date": converted_date,
        "con_name": contract["name"],
        "additional": data["additional"],
        "po": data["po"],
        "descs": data["desc"],
    }
    options = {
        "page-size": "A4",
        "margin-top": "20mm",
        "margin-right": "0mm",
        "margin-bottom": "0mm",
        "margin-left": "0mm",
        "zoom": "1.0mm"
    }
    # print(data)
    html_string = get_tta_html_string()
    html_template = Template(html_string)
    rendered_html = html_template.render(data=doc_data)
    wkhtmltopdf_path = "/usr/local/bin/wkhtmltopdf"

    await convert_to_pdf(rendered_html, f"tta{c_id}.pdf", options=options, config_path=wkhtmltopdf_path)

    return templates.TemplateResponse(
        "tta.html", {"request": request, "data": doc_data}
    )


@router.get("/tta-create")
async def tta_get(request: Request):

    companies = Company.select()
    
    return templates.TemplateResponse(
        "tta_create.html", {"request": request, "companies": companies}
    )


@router.post("/tta-create")
async def tta_post(data: TTAInputSchema, reuqest: Request):

    contract = Contract.create(
        name=data.name.strip(),
        comp_id=data.comp_id,
        date=data.date,
        currency=data.currency,
        created_at=int(time.time())
    )

    return {"status": "ok"}


@router.post("/tta-doc")
async def tta_doc_post(data: TTADocInputSchema, reuqest: Request):

    obj = {
        "currency": data.currency,
        "desc": data.descs,
        "additional": data.additional,
        "po": data.po
    }

    tta_doc = TTAData.create(
        name=data.drc_name.strip(),
        comp_id=data.comp_id,
        contract_id=int(data.contract_id),
        date=data.date,
        data=json.dumps(obj, separators=(",", ":")),
        create_date=data.date
    )

    return {"id": tta_doc.id}



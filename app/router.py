import hashlib
import time
import os
import json
import pdfkit
import subprocess
from fastapi import Request, File, UploadFile, HTTPException
from fastapi.param_functions import Depends, File
from fastapi.routing import APIRouter
from peewee import Ordering
from starlette import status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
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
from app.utils import (
    convert_to_pdf,
    get_html_string,
    get_image_file_as_base64_data,
    get_tta_html_string,
    date_covnerting_to_human,
    convert_pdf_to_doc,
    aa,
    AuthUser,
)
from datetime import datetime, timedelta

# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
from fastapi_mail import FastMail, MessageSchema, MessageType
from core.extensions import email_conf
from fastapi_jwt_auth import AuthJWT
from .auth_utils import create_access_token, jwt_check
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(prefix="", tags=["pdf"])

templates = Jinja2Templates(directory="templates")
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
env = Environment(loader=FileSystemLoader(templates_dir))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("log_in.html", {"request": request})


@router.post("/login")
def log_in(data: LoginInputSchema):
    user = User.get_or_404(User.email == data.username)

    if user.password != hashlib.sha256(data.password.encode()).hexdigest():
        return JSONResponse(
            status_code=401, content={"error": "Invalid username or password"}
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": user.is_admin},
        expires_delta=access_token_expires,
    )
    print({"access_token": access_token})
    return JSONResponse(status_code=200, content={"access": access_token})


@router.get("/create")
def create_user_get(request: Request, token: str = Depends(oauth2_scheme)):
    return templates.TemplateResponse("create_user.html", {"request": request})


@router.post("/create")
def create_user(
    request: Request, data: CreateUserInput, token: str = Depends(oauth2_scheme)
):
    admin = jwt_check(token)
    if not admin:
        return JSONResponse(
            status_code=403,
            content={"error": "You don't have permission for this action"},
        )
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
def create_comp(data: CreateCompanyInputSchema, token: str = Depends(oauth2_scheme)):
    admin = jwt_check(token)
    if not admin:
        return JSONResponse(
            status_code=403,
            content={"error": "You don't have permission for this action"},
        )
    user = User.select().where(User.email == admin["email"])
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
def create_proj(data: CreateProjectInputSchema, token: str = Depends(oauth2_scheme)):
    admin = jwt_check(token)
    if not admin:
        return JSONResponse(status_code=403, content={"error": "You don't have permission for this action"})
    
    Project.create(
        name=data.name.strip(),
        comp_id=int(data.comp_id),
        currency=data.currency.strip(),
        created_at=int(time.time()),
    )

    return status.HTTP_200_OK


@router.get("/create-project")
def create_proj_get(request: Request):
    return templates.TemplateResponse("create_project.html", {"request": request})


@router.get("/create-doc")
def create_doc(request: Request):
    last_inv = PdfData.select(PdfData.data).order_by(PdfData.id.desc())
    if last_inv:
        last_inv = list(last_inv)[0]
        last_inv = json.loads(last_inv.data)["invoice_id"] + 1
    else:
        last_inv = 1

    return templates.TemplateResponse(
        "invoice_create.html", {"request": request, "inv_id": last_inv}
    )


@router.get("/projects/{comp_id}")
def get_projects(comp_id: int, request: Request):
    projects = Project.select().where(Project.comp_id == comp_id).dicts()

    return list(projects)


@router.post("/convert-invoice")
def convert_pdf(
    data: ConvertInvoiceInputSchema,
    request: Request,
    token: str = Depends(oauth2_scheme),
):
    admin = jwt_check(token)
    if not admin:
        return JSONResponse(
            status_code=403,
            content={"error": "You don't have permission for this action"},
        )
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
        "invoice_id": int(data.invoice_id),
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


@router.get("/update-invoice/{inv_id}")
def get_invoice(inv_id: int, request: Request):
    # admin = jwt_check(token)
    # if not admin:
    #     return JSONResponse(status_code=403, content={"error": "You don't have permission for this action"})
    invoice = list(PdfData.select().where(PdfData.id == inv_id).dicts())[0]
    company = list(Company.select().where(Company.id == invoice["comp_id"]).dicts())[0]
    project = list(Project.select().where(Project.id == invoice["proj_id"]).dicts())[0]
    inv_data = json.loads(invoice["data"])
    print(company)

    payload = {
        "id": inv_id,
        "comp_id": invoice["comp_id"],
        "proj_id": invoice["proj_id"],
        "data": inv_data["desciptions"],
        "invoice_id": inv_data["invoice_id"],
    }

    return templates.TemplateResponse(
        "upt_inv.html",
        {
            "request": request,
            "data": payload,
            "date": inv_data["date"],
            "due_date": inv_data["due_date"],
            "company": company,
            "project": project,
        },
    )


@router.put("/update-invoice/{inv_id}")
def put_invoice(
    inv_id: int,
    data: ConvertInvoiceInputSchema,
    request: Request,
    token: str = Depends(oauth2_scheme),
):
    admin = jwt_check(token)
    if not admin:
        return JSONResponse(
            status_code=403,
            content={"error": "You don't have permission for this action"},
        )
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
        "invoice_id": int(data.invoice_id),
        "date": data.date,
        "due_date": data.due_date,
    }

    pdf_data = (
        PdfData.update(
            data=json.dumps(obj, separators=(",", ":")),
            comp_id=data.comp_id,
            proj_id=data.proj_id,
            created_at=int(time.time()),
        )
        .where(PdfData.id == inv_id)
        .execute()
    )

    return {"id": inv_id}


@router.get("/preview-upd/{id}")
async def preview(id: int, request: Request):
    pdf_data = list(PdfData.select().where(PdfData.id == id).dicts())[0]
    company = list(Company.select().where(Company.id == pdf_data["comp_id"]).dicts())[0]
    comp_id = pdf_data["comp_id"]
    proje = list(Project.select().where(Project.id == pdf_data["proj_id"]).dicts())[0]
    pdf_data = json.loads(pdf_data["data"])
    pdf_data["date"] = pdf_data["date"].replace("-", "/")
    pdf_data["due_date"] = pdf_data["due_date"].replace("-", "/")
    currency_icon_2 = None
    if proje["currency"] == "usd":
        currency = "$"
        currency_icon = "$"
        currecny_icon_2 = "$"
    else:
        currency = "₼"
        currency_icon_2 = '<img src="/app/static/az_curr.svg" width="20px" height="20px">'
        currency_icon = '<img src="/app/static/Azeri_manat_symbol.svg" width="10px" height="10px">'
    pdf_data["currency_2"] = currency
    pdf_data["currency"] = currency
    pdf_data["cur_icon"] = currency_icon
    pdf_data["cur_icon2"] = currency_icon_2

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

    return templates.TemplateResponse(
        "preview-upd.html", {"request": request, "data": pdf_data}
    )


@router.get("/preview/{id}")
async def preview(id: int, request: Request):
    pdf_data = list(PdfData.select().where(PdfData.id == id).dicts())[0]
    company = list(Company.select().where(Company.id == pdf_data["comp_id"]).dicts())[0]
    comp_id = pdf_data["comp_id"]
    proje = list(Project.select().where(Project.id == pdf_data["proj_id"]).dicts())[0]
    pdf_data = json.loads(pdf_data["data"])
    pdf_data["date"] = pdf_data["date"].replace("-", "/")
    pdf_data["due_date"] = pdf_data["due_date"].replace("-", "/")
    currency_icon_2 = None
    if proje["currency"] == "usd":
        currency = "$"
        currency_icon = "$"
        currecny_icon_2 = "$"
    else:
        currency = "₼"
        currency_icon_2 = '<img src="/app/static/az_curr.svg" width="20px" height="20px">'
        currency_icon = '<img src="/app/static/Azeri_manat_symbol.svg" width="10px" height="10px">'
    pdf_data["currency_2"] = currency
    pdf_data["currency"] = currency
    pdf_data["cur_icon"] = currency_icon
    pdf_data["cur_icon2"] = currency_icon_2

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
        "page-size": "Letter",
        "margin-top": "40mm",
        "zoom": "1.0",
        "enable-local-file-access": True,
    }
    html_string = get_html_string()
    html_template = Template(html_string)
    rendered_html = html_template.render(data=pdf_data)
    wkhtmltopdf_path = "/usr/local/bin/wkhtmltopdf"
    path = os.getcwd()
    if not os.path.exists(f"{path}/invoice_folder"):
        os.mkdir("invoice_folder")
    await convert_to_pdf(
        rendered_html,
        f"{path}/output{id}.pdf",
        options=options,
        config_path=wkhtmltopdf_path,
    )

    return templates.TemplateResponse(
        "invoice.html", {"request": request, "data": pdf_data}
    )


@router.get("/update-tta/{tta_id}")
def get_tta(tta_id: int, request: Request):
    # admin = jwt_check(token)
    # if not admin:
    #     return JSONResponse(status_code=403, content={"error": "You don't have permission for this action"})
    tta = list(TTAData.select().where(TTAData.id == tta_id).dicts())[0]
    print(tta)
    company = list(Company.select().where(Company.id == tta["comp_id"]).dicts())[0]
    contract = list(Contract.select().where(Contract.id == tta["contract_id"]).dicts())[
        0
    ]
    tta_data = json.loads(tta["data"])

    payload = {
        "id": tta_id,
        "comp_id": tta["comp_id"],
        "contract_id": tta["contract_id"],
        "data": tta_data["desc"],
        "position": tta_data["position"],
        "name": tta["name"],
    }

    return templates.TemplateResponse(
        "upd_tta.html",
        {
            "request": request,
            "data": payload,
            "create_date": tta["create_date"],
            "company": company,
            "contract": contract,
        },
    )




@router.put("/update-tta/{tta_id}")
def put_tta(
    tta_id: int,
    data: TTADocInputSchema,
    token: str = Depends(oauth2_scheme),
):
    admin = jwt_check(token)
    if not admin:
        return JSONResponse(
            status_code=403,
            content={"error": "You don't have permission for this action"},
        )

    obj = {
        "currency": data.currency,
        "desc": data.descs,
        "additional": data.additional,
        "po": data.po,
        "position": data.position,
    }

    tta_doc = TTAData.update(
        name=data.drc_name.strip(),
        comp_id=data.comp_id,
        contract_id=int(data.contract_id),
        data=json.dumps(obj, separators=(",", ":")),
        create_date=data.date,
    ).where(TTAData.id == tta_id).execute()


    return {"id": tta_id}


@router.get("/tta-preview-upd/{id}")
async def preview(id: int, request: Request):
    contract_doc_data = list(TTAData.select().where(TTAData.id == id).dicts())[0]
    company = list(
        Company.select().where(Company.id == contract_doc_data["comp_id"]).dicts()
    )[0]
    contract = list(
        Contract.select().where(Contract.id == contract_doc_data["contract_id"]).dicts()
    )[0]
    data = json.loads(contract_doc_data["data"])
    converted_date = date_covnerting_to_human(contract["date"])
    contract_doc_data["create_date"] = contract_doc_data["create_date"].replace(
        "-", "."
    )
    final = 0
    for i in data["desc"]:
        final += int(i["qty"]) * int(i["price_one"])
    total = final
    vat = final * 18 / 100
    cur_icon = "₼"
    if data["currency"] == "usd":
        currency = "$"
        cur_icon = "$"
    else:
        currency = "₼"
        cur_icon = (
            '<img src="/app/static/Azeri_manat_symbol.svg" width="10px" height="10px">'
        )
    doc_data = {
        "id": id,
        "company_name": company["name"],
        "drc_name": contract_doc_data["name"],
        "date": contract_doc_data["create_date"],
        "con_date": converted_date,
        "con_name": contract["name"],
        "additional": data["additional"],
        "po": data["po"],
        "descs": data["desc"],
        "position": data["position"],
        "currency": data["currency"],
        "vat": vat,
        "final": total,
        "total": round(final + vat, 2),
        "cur_icon": cur_icon,
        "cur_icon_2": currency,
    }
    # doc_file = f"tta_doc_{c_id}.docx"
    # await convert_pdf_to_doc(f"tta{c_id}.pdf", doc_file)

    return templates.TemplateResponse(
        "tta_prev_upd.html", {"request": request, "data": doc_data}
    )

@router.get("/download/{inv_id}")
def admin(inv_id: int, request: Request):
    attach_name = f"output{inv_id}.pdf"

    return FileResponse(
        attach_name, filename="invoice.pdf", media_type="application/pdf"
    )


@router.get("/download-tta/{id}")
def admin(id: int, request: Request):
    attach_name = f"tta{id}.pdf"

    return FileResponse(attach_name, filename="tta.pdf", media_type="application/pdf")


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
    return templates.TemplateResponse("invoice.html", {"request": request})


@router.get("/list-comps")
def list_comps(request: Request):
    companies = list(Company.select().dicts())

    return companies


@router.get("/contract-list/{comp_id}")
def list_contracts(
    comp_id: int,
    request: Request,
):
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
    print("ey")

    return templates.TemplateResponse("navigation.html", {"request": request})


@router.get("/invoice-list")
async def inv_list(request: Request):
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


@router.get("/tta-list")
def tta_list(request: Request):
    docs = list(
        TTAData.select(
            TTAData.id,
            TTAData.name,
            Company.name.alias("comp_name"),
            TTAData.create_date,
            Contract.name.alias("contract"),
            Contract.currency.alias("currency"),
        )
        .join(Company, on=Company.id == TTAData.comp_id)
        .join(Contract, on=Contract.id == TTAData.contract_id)
        .dicts()
    )
    response_list = []
    for doc in docs:
        response_list.append(
            {
                "id": doc["id"],
                "company_name": doc["comp_name"],
                "name": doc["name"],
                "create_date": doc["create_date"],
                "contract": doc["contract"],
                "currency": doc["currency"],
            }
        )

    return templates.TemplateResponse(
        "tta_list.html", {"request": request, "docs": docs}
    )


@router.get("/tta-preview/{c_id}")
async def prew_tta(c_id: int, request: Request):
    contract_doc_data = list(TTAData.select().where(TTAData.id == c_id).dicts())[0]
    company = list(
        Company.select().where(Company.id == contract_doc_data["comp_id"]).dicts()
    )[0]
    contract = list(
        Contract.select().where(Contract.id == contract_doc_data["contract_id"]).dicts()
    )[0]
    data = json.loads(contract_doc_data["data"])
    converted_date = date_covnerting_to_human(contract["date"])
    contract_doc_data["create_date"] = contract_doc_data["create_date"].replace(
        "-", "."
    )
    final = 0
    for i in data["desc"]:
        final += int(i["qty"]) * int(i["price_one"])
    total = final
    vat = final * 18 / 100
    cur_icon = "₼"
    if data["currency"] == "usd":
        currency = "$"
        cur_icon = "$"
    else:
        currency = "₼"
        cur_icon = '<img src="/app/static/Azeri_manat_symbol.svg" width="10px" height="10px">'
    doc_data = {
        "id": c_id,
        "company_name": company["name"],
        "drc_name": contract_doc_data["name"],
        "date": contract_doc_data["create_date"],
        "con_date": converted_date,
        "con_name": contract["name"],
        "additional": data["additional"],
        "po": data["po"],
        "descs": data["desc"],
        "position": data["position"],
        "currency": data["currency"],
        "vat": vat,
        "final": total,
        "total": round(final + vat, 2),
        "cur_icon": cur_icon,
        "cur_icon_2": currency
    }
    options = {
        "page-size": "A4",
        "margin-top": "20mm",
        "margin-right": "0mm",
        "margin-bottom": "0mm",
        "margin-left": "0mm",
        "zoom": "1.0",
        "enable-local-file-access": True,
    }
    html_string = get_tta_html_string()
    html_template = Template(html_string)
    rendered_html = html_template.render(data=doc_data)
    print(rendered_html)
    wkhtmltopdf_path = "/usr/local/bin/wkhtmltopdf"
    path = os.getcwd()
    if not os.path.exists(f"{path}/tta_folder"):
        os.mkdir("data_folder")
    await convert_to_pdf(rendered_html, f"{path}/tta{c_id}.pdf", wkhtmltopdf_path, options)
    print(doc_data["descs"])
    # doc_file = f"tta_doc_{c_id}.docx"
    # await convert_pdf_to_doc(f"tta{c_id}.pdf", doc_file)

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
async def tta_post(
    data: TTAInputSchema, reuqest: Request, token: str = Depends(oauth2_scheme)
):
    contract = Contract.create(
        name=data.name.strip(),
        comp_id=data.comp_id,
        date=data.date,
        currency=data.currency,
        created_at=int(time.time()),
    )

    return {"status": "ok"}


@router.post("/tta-doc")
async def tta_doc_post(
    data: TTADocInputSchema, reuqest: Request, token: str = Depends(oauth2_scheme)
):
    obj = {
        "currency": data.currency,
        "desc": data.descs,
        "additional": data.additional,
        "po": data.po,
        "position": data.position,
    }

    tta_doc = TTAData.create(
        name=data.drc_name.strip(),
        comp_id=data.comp_id,
        contract_id=int(data.contract_id),
        date=data.date,
        data=json.dumps(obj, separators=(",", ":")),
        create_date=data.date,
    )

    return {"id": tta_doc.id}


@router.get("/open-mail/{id}")
def open_mail_app(id: int):
    try:
        subprocess.run(["open", "-a", "Mail", f"tta{id}.pdf"])
        return "Default mail app opened successfully."
    except FileNotFoundError:
        return "Default mail app not found."


@router.get("/open-mail-inv/{id}")
def open_mail_app(id: int):
    try:
        subprocess.run(
            [
                "open",
                "-a",
                "Mail",
                f"output{id}.pdf",
                "--args",
                "mailto:" + "amil@gmail.com",
            ]
        )
        return "Default mail app opened successfully."
    except FileNotFoundError:
        return "Default mail app not found."

from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Optional


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class CreateUserInput(BaseModel):
    fullname: str = ''
    email: EmailStr = ''
    password: str = ''

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict 


class LoginInputSchema(BaseModel):
    username: EmailStr
    password: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict 


class CreateCompanyInputSchema(BaseModel):
    name: str
    address: str
    location: str = ""
    tax_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict 


class CreateProjectInputSchema(BaseModel):
    name: str
    currency: str
    comp_id: int
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict 


class ConvertInvoiceInputSchema(BaseModel):
    comp_id: str
    contract: str
    proj_id: str
    date: str
    curr: str
    due_date: str
    invoice_id: str
    descriptions: List


class SendMailInput(BaseModel):
    inv_id: str
    comp_id: str


class TTAInputSchema(BaseModel):
    name: str
    comp_id: int
    date: str
    currency: str


class TTADocInputSchema(BaseModel):
    contract_id: str
    comp_id: str
    drc_name: str
    currency: str
    date: str
    descs: List 
    additional: str = None
    po: str = None
    position: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict 
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
    email: EmailStr
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
    proj_id: str
    date: str
    due_date: str
    invoice_id: str
    descriptions: List


class SendMailInput(BaseModel):
    inv_id: str
    comp_id: str
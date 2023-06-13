from peewee import (
    CharField,
    IntegerField,
    BigIntegerField,
    AutoField,
    SQL,
    TextField,
    BigAutoField,
    FloatField,
    DateField,
    ForeignKeyField,
)

from core.database import BaseModel


class User(BaseModel):
    id = AutoField()
    full_name = CharField()
    email = CharField()
    password = CharField()
    created_at = BigIntegerField()

    class Meta:
        table_name = "user"


class Company(BaseModel):
    id = AutoField()
    name = CharField()
    address = CharField()
    location = CharField()
    created_at = BigIntegerField()

    class Meta:
        table_name = "companies"


class Project(BaseModel):
    id = AutoField()
    name = CharField()
    comp_id = ForeignKeyField(column_name='comp_id', field='id', model=Company, null=True)
    currency = CharField()
    created_at = BigIntegerField()

    class Meta:
        table_name = "projects"
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
    fullname = CharField()
    email = CharField()
    password = CharField()
    created_at = BigIntegerField()

    class Meta:
        table_name = "user"
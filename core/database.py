from abc import ABC
from fastapi import HTTPException
from peewee import Model, MySQLDatabase, DoesNotExist
from playhouse.shortcuts import ReconnectMixin
from starlette import status

from core.extensions import db
from core.config import settings


class StrictMySQLDatabase(ReconnectMixin, MySQLDatabase, ABC):
    def _connect(self, **kwargs):

        return super(StrictMySQLDatabase, self)._connect()

db_connection = StrictMySQLDatabase(
    database=settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
    port=3309,
    host="localhost",
)

class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_or_404(cls, *query, **filters):
        try:
            return cls.get(*query, **filters)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{cls.__name__} with given id not found.",
            )

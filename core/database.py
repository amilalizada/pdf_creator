from abc import ABC

from fastapi import HTTPException
from peewee import Model, MySQLDatabase, DoesNotExist
from playhouse.shortcuts import ReconnectMixin
from starlette import status

from core.extensions import db
from core.config import settings


class StrictMySQLDatabase(ReconnectMixin, MySQLDatabase, ABC):
    def _connect(self, **kwargs):
        # cursor = self.cursor()
        # cursor.execute("SET SESSION sql_mode='NO_BACKSLASH_ESCAPES,NO_ENGINE_SUBSTITUTION';")
        # cursor.execute("SET NAMES utf8mb4;")

        return super(StrictMySQLDatabase, self)._connect()

db_connection = StrictMySQLDatabase(
    database=str(settings.db_name),
    user=str(settings.db_user),
    password=str(settings.db_password),
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

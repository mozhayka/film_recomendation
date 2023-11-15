import dataclasses
import enum
from typing import List
import peewee as pw


database = pw.SqliteDatabase("chat.db")


class BaseModel(pw.Model):
    class Meta:
        database = database


class User(BaseModel):
    username = pw.CharField()
    chat_id = pw.CharField(unique=True)
    mode = pw.CharField(default='ivi')
    film1 = pw.CharField(null=True)
    film2 = pw.CharField(null=True)


database.connect()
database.create_tables([User])


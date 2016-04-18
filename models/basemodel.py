from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('data.db')

class BaseModel(Model):
    class Meta:
        database = db

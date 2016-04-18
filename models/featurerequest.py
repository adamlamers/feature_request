from peewee import *
from .basemodel import BaseModel

class Client(BaseModel):
    name = CharField()

class ProductCategory(BaseModel):
    name = CharField()

class FeatureRequest(BaseModel):
    title = CharField()
    description = TextField()
    client = ForeignKeyField(Client, related_name='from_client')
    client_priority = IntegerField()
    target_date = DateTimeField()
    ticket_url = TextField()
    category = ForeignKeyField(ProductCategory, related_name='in_category')


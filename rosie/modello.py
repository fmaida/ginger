import os
from peewee import *


baseurl = os.path.join(os.path.dirname(__file__), "data", "data.sqlite")
DATABASE = SqliteDatabase(baseurl)


class Elemento(Model):
    id = CharField(max_length=160, primary_key=True)
    title = CharField(max_length=160)
    tags = TextField()
    properties = TextField()
    content = TextField()

    class Meta:
        database = DATABASE


DATABASE.connect()
DATABASE.create_tables([Elemento], safe=True)

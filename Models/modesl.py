from playhouse.db_url import connect
from peewee import Model, CharField

db = connect('sqlite:///users.db')


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        return f"{self.id}"


class Accounts(BaseModel):
    PENDING_SEND = 'Pending_send'
    SENT = 'send'

    username = CharField(max_length=50)
    status = CharField(max_length=15, default=PENDING_SEND)


db.create_tables([Accounts])

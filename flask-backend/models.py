from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('youcoin.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True) 
    email = CharField(unique=True)
    password = CharField()
    profit = IntegerField()

    class Meta:

        database = DATABASE

class Youcoin(Model):
    user=ForeignKeyField(User, backref='youcoin')
    channelUrl= CharField()
    channelTitle=CharField()
    channelId=CharField()
    startingNum= IntegerField()
    currentNum= IntegerField()
    profit = IntegerField()
    createdDate = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Stat(Model):
    youcoin = ForeignKeyField(Youcoin, backref="state")
    date = DateTimeField(default=datetime.datetime.now)
    currentSubs= IntegerField()

    class Meta: 
        database = DATABASE

def initialize():
    DATABASE.connect()
    # DATABASE.drop_tables([User, Youcoin])
    # print("TABLES DROPPED")
    DATABASE.create_tables([User, Youcoin, Stat], safe=True)
    print("TABLES CREATED")
    DATABASE.close()




from peewee import *
from datetime import date, datetime
from postgres_ext import *
from dotenv import load_dotenv
import os

load_dotenv()

postgresDb = os.getenv('POSTGRES_DB')
postgresUser = os.getenv('POSTGRES_USER')
postgresPassword = os.getenv('POSTGRES_PASSWORD')
postgresHost = os.getenv('POSTGRES_HOST')
postgresPort = os.getenv('POSTGRES_POST')

database = PostgresqlDatabase(postgresDb, user=postgresUser, password=postgresPassword, host=postgresHost, port=postgresPort)

class User(Model):
    id = AutoField()
    domainName = CharField(max_length=100)
    domainEmail = CharField(max_length=100)
    password = CharField(max_length=100)
    
    class Meta:
        database = database

User.create_table()


class UserStatistic(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref='statistics')
    sendMessagesCount = IntegerField()
    receivedMessagesCount =  IntegerField()
    recipientCounts = IntegerField()
    bccCount = IntegerField()
    ccCount = IntegerField()
    daysBetweenReceivedAndRead = ArrayField(IntegerField)
    repliedMessagesCount = IntegerField()
    sentCharactersCount = IntegerField()
    messagesOutsideWorkingHours = IntegerField()
    receivedToSentRatio = FloatField()
    bytesReceivedToSentRatio = FloatField()
    messagesWithQuestionAndNoReply = IntegerField()
    readMessagesMoreThan4Hours = IntegerField()
    startInterval = DateField()
    endInterval = DateField()
    toxic_messages_percent = FloatField()

    class Meta:
        database = database

UserStatistic.create_table()

def get_users():
    return User.select()
    


    
    

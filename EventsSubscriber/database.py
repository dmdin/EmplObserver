from peewee import *
from datetime import date, datetime
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

    class Meta:
        database = database


User.create_table()


class App(Model):
    id = AutoField()
    appName = CharField(max_length=255)

    class Meta:
        database = database

App.create_table()

class EventApplication(Model):
    id = AutoField()
    application = ForeignKeyField(App, related_name='events')
    user = ForeignKeyField(User, related_name="events")
    count = IntegerField()
    date = DateField()

    class Meta:
        database = database

    @property
    def date_without_time(self):
        return self.date.strftime('%Y-%m-%d')

    @date_without_time.setter
    def date_without_time(self, value):
        self.date = date.fromisoformat(value)

EventApplication.create_table()

class TimeIntervalEvent(Model):
    id = AutoField()
    user = ForeignKeyField(User, related_name="timeIntervalEvents")
    count = IntegerField()
    intervalStart = DateTimeField()
    intervalEnd = DateTimeField()

    class Meta:
        database = database

TimeIntervalEvent.create_table()
    

def get_user_or_create(user_name):
    exists = User.select().where(User.domainName == user_name).exists()
    
    user = None
    if exists:
        user = User.get(User.domainName == user_name)
    else:
        user = User(domainName = user_name)
        user.save()
    
    return user

def get_application_or_create(app_name):
    exists = App.select().where(App.appName == app_name).exists()

    app = None
    if exists:
        app = App.get(App.appName == app_name)
    else:
        app = App(appName = app_name)
        app.save()

    return app

def register_app_event(user, app):
    today = datetime.today().date()

    exists = EventApplication.select().where((EventApplication.user == user) & (EventApplication.application == app) & (EventApplication.date == today)).exists()

    if exists:
        userAppEvent = EventApplication.get((EventApplication.user == user) & (EventApplication.application == app) & (EventApplication.date == today))
        userAppEvent.count+=1
        userAppEvent.save()
    else:
         userAppEvent = EventApplication(user=user, application=app, date=today, count=1)
         userAppEvent.save()

def get_current_interval_start(now):
    minutes = 0
    if now.minute >= 30:
        minutes = 30

    return datetime(now.year, now.month, now.day, now.hour, minutes, 0)
        
def get_current_interval_end(now):
    minutes = 30
    hour = now.hour
    if now.minute >= 30:
        minutes = 0
        hour +=1

    return datetime(now.year, now.month, now.day, hour, minutes, 0)

def register_time_interval_event(user):
    now = datetime.utcnow()

    exists = TimeIntervalEvent.select().where((TimeIntervalEvent.user == user) & (TimeIntervalEvent.intervalStart < now) & (TimeIntervalEvent.intervalEnd > now)).exists()

    if exists:
        timeIntervalEvent = TimeIntervalEvent.get((TimeIntervalEvent.user == user) & (TimeIntervalEvent.intervalStart < now) & (TimeIntervalEvent.intervalEnd > now))
        timeIntervalEvent.count += 1
        timeIntervalEvent.save()
    else:
        start_interval = get_current_interval_start(now)
        end_interval = get_current_interval_end(now)

        timeIntervalEvent = TimeIntervalEvent(user=user, intervalStart = start_interval, intervalEnd = end_interval, count=1)
        timeIntervalEvent.save()


def register_event(user_name, app_name):
    user = get_user_or_create(user_name)
    app = get_application_or_create(app_name)

    register_app_event(user, app)
    register_time_interval_event(user)
    
    


    
    

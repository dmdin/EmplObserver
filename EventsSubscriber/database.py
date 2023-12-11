from peewee import *
from datetime import date, datetime

database = PostgresqlDatabase()

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

def register_event(user_name, app_name):
    user = get_user_or_create(user_name)
    app = get_application_or_create(app_name)
    today = datetime.today().date()
    
    exists = EventApplication.select().where(EventApplication.user == user and EventApplication.application == app and EventApplication.date == today).exists()

    if exists:
        userAppEvent = EventApplication.get(EventApplication.user == user and EventApplication.application == app and EventApplication.date == today)
        userAppEvent.count+=1
        userAppEvent.save()
    else:
         userAppEvent = EventApplication(user=user, application=app, date=today, count=0)
         userAppEvent.save()


    
    

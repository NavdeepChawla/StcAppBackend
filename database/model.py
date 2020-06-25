from database.db import db


class User(db.Document):
    email = db.StringField(require=True, unique=True)
    password = db.StringField(require=True)
    token = db.ListField(db.StringField())

class Article(db.Document):
    link = db.StringField(required=True)
    title = db.StringField(required=True)
    domain = db.StringField(required=True)

class Event(db.Document):
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    link = db.StringField(required=True)
    image = db.StringField(required=True)

class Feed(db.Document):
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    link = db.StringField(required=True)
    image = db.StringField(required=True)

class Github(db.Document):
    link = db.StringField(required=True)
    title = db.StringField(required=True)

class Project(db.Document):
    link = db.StringField(required=True)
    title = db.StringField(required=True)
    contributors = db.ListField(db.StringField())
    description = db.StringField(required=True)

class Resource(db.Document):
    link = db.StringField(required=True)
    title = db.StringField(required=True)
    domain = db.StringField(required=True)

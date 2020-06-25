from flask import Flask
from database.db import initialize_db
from flask_jwt_extended import JWTManager
from routes.user import user
from routes.article import article
from routes.project import project
from routes.feed import feed
from routes.event import event
from routes.resource import resource
from routes.github import github

app = Flask(__name__)
app.config['MONGODB_HOST'] = 'Enter Mongo DB URL'
app.config['MONGODB_DB'] = 'Enter DB Name'
app.config['JWT_SECRET_KEY'] = 'Enter Secret Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
initialize_db(app)
jwt = JWTManager(app)

app.register_blueprint(user)
app.register_blueprint(article)
app.register_blueprint(event)
app.register_blueprint(feed)
app.register_blueprint(github)
app.register_blueprint(project)
app.register_blueprint(resource)

@app.route("/")
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname('__file__'))

# autoload template changes
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db Init
db = SQLAlchemy(app)

# ma Init
ma = Marshmallow(app)

# register rest api
from web.rest.routes import api
app.register_blueprint(api, url_prefix='/api')

# register site
from web.views.home import home
from web.views.dashboard import dashboard
from web.views.admin import admin

app.register_blueprint(home, url_prefix='/')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(admin, url_prefix='/admin')


# database create console
# from web import db
# from web.model.models import Book
# # db.drop_all()
# db.create_all()


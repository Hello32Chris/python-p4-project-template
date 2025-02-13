from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table
from flask_cors import CORS
from flask_bcrypt import Bcrypt

import sqlalchemy as sa
import os




BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})



db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

CORS(app)
import os

from flask_bootstrap import Bootstrap
from flask import Flask
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yourhjbsfhsh_sojgjsecretsjngjonsojg_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config['CKEDITOR_PKG_TYPE'] = 'full'
UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Directory to save uploaded files

db = SQLAlchemy(app)
ckeditor = CKEditor(app)

Bootstrap(app)

from Routes import *  # noqa
from database import *  # noqa

if __name__ == "__main__":
    app.run(debug=True, port=3000)

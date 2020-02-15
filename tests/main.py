from epihq import create_app, db, User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


if __name__ == "__main__":
    print(1)
    app = Flask('epihq')
    db = SQLAlchemy(app)

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
import json
from flask_migrate import Migrate

database_name = "agency"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
# database_path = 'postgres://postgres@localhost:5432/agency'
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(String)
    actmov = db.relationship('ActMov', backref="movies", lazy=True)

    def __init__(self, title, date):
        self.title = title
        self.date = date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date
            }

'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    gender = Column(String)
    actmov = db.relationship('ActMov', backref="actors", lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }

'''
Actors/Movies

'''


class ActMov(db.Model):
    __tablename__ = 'actmov'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, db.ForeignKey('actors.id'), nullable=False)
    movie_id = Column(Integer, db.ForeignKey('movies.id'), nullable=False)

from .. import db


class User(db.Model):
    """ User Model for storing GitHub users """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    image_url = db.Column(db.String)
    type = db.Column(db.String)
    profile_url = db.Column(db.String)

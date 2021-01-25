from settings import db


class User(db.Model):
    """
    This class models the user's credentials
    """
    __tablename__ = 'user_login'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(255))
    name = db.Column(db.String(50))
    password = db.Column(db.String(255))

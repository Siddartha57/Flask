from module import db
from module import bcrypt,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable = False, unique=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    phone =  db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable = False, unique=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Busses(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(),nullable=False)
    disc = db.Column(db.String(),nullable=False)
    amount = db.Column(db.String(),nullable=False)
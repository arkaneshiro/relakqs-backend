from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    avi_url = db.Column(db.Text, default="https://res.cloudinary.com/"
                        "dgzcv1mcs/image/upload/v1589817904/"
                        "bw2djxdddpa1mjpshity.jpg"
                        )
    username = db.Column(db.String(20), unique=True, nullable=False)
    h_password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    bio = db.Column(db.String(100), default="", nullable=False)

    @property
    def password(self):
        return h_password

    @password.setter
    def password(self, password):
        self.h_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.h_password, password)

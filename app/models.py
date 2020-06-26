from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


container_users = db.Table(
    "container_users",
    db.Model.metadata,
    db.Column("user_id",
              db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True
              ),
    db.Column("container_id",
              db.Integer,
              db.ForeignKey("containers.id"),
              primary_key=True
              ),
)


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

    container = db.relationship("Container", back_populates="admin")
    containers = db.relationship("Container",
                                 secondary=container_users,
                                 back_populates="members"
                                 )

    @property
    def password(self):
        return h_password

    @password.setter
    def password(self, password):
        self.h_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.h_password, password)


class Container(db.Model):
    __tablename__ = "containers"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_channel = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(25), nullable=False)
    topic = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now(),
                           nullable=False)

    admin = db.relationship("User", back_populates="container")
    members = db.relationship("User",
                              secondary=container_users,
                              back_populates="containers"
                              )

    @property
    def user_list(self):
        return [member.username for member in self.members]

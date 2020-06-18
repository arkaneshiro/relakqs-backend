from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import User


with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(
        username='Riki',
        h_password='pbkdf2:sha256:150000$ltOXv3W8$'
        '6e1e42bfc60f89dde0a8cd8e1f6999c16d5473ac1ccc7b74906b2cb9dde76a38',
        email='riki@riki.com',
        bio='hi im riki',
    )

    db.session.add(user1)
    db.session.commit()

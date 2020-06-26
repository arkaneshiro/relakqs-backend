from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import User, Container


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
    user2 = User(
        username='God',
        h_password='pbkdf2:sha256:150000$RAQL3sNi$'
        '2f0e4093a24a192f1a3a112820a0957683972fecefc106f246ee5cc22172ecc8',
        email='god@riki.com',
        bio='hi !',
    )

    container1 = Container(
        admin=user2,
        is_channel=True,
        title='first channel',
        topic='this is the first channel',
    )

    container1.members.append(user2)
    container1.members.append(user1)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(container1)
    db.session.commit()

    print(container1.user_list)

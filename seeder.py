from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import User, Container, Message


with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(
        username='Riki',
        h_password='pbkdf2:sha256:150000$ltOXv3W8$'
        '6e1e42bfc60f89dde0a8cd8e1f6999c16d5473ac1ccc7b74906b2cb9dde76a38',
        email='riki@riki.com',
        bio='hi im riki',
        avi_url='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1592235884/b0emvohw3sgn7oz3vlkx.jpg'
    )
    user2 = User(
        username='Pikachu',
        h_password='pbkdf2:sha256:150000$RAQL3sNi$'
        '2f0e4093a24a192f1a3a112820a0957683972fecefc106f246ee5cc22172ecc8',
        email='god@riki.com',
        bio='hi !',
        avi_url='https://res.cloudinary.com/dgzcv1mcs/image/upload/v1591979148/in1wgr6ehi2rdflpipah.png'
    )
    user3 = User(
        username='Guest',
        h_password='pbkdf2:sha256:150000$ltOXv3W8$'
        '6e1e42bfc60f89dde0a8cd8e1f6999c16d5473ac1ccc7b74906b2cb9dde76a38',
        email='guest@riki.com',
        bio='hi I\'m a guest!',
    )

    container1 = Container(
        admin=user2,
        is_channel=True,
        title='#first-channel',
        topic='this is the first channel',
    )

    container1.members.append(user2)
    container1.members.append(user1)
    container1.members.append(user3)

    container2 = Container(
        admin=user1,
        is_channel=True,
        title='#other-channel',
        topic='this is the good channel',
    )

    container2.members.append(user1)
    container2.members.append(user2)

    container3 = Container(
        admin=user1,
        is_channel=True,
        title='#riki-channel',
        topic='riki channel riki channel riki channel riki channel',
    )

    container3.members.append(user1)

    message1 = Message(
        messager=user1,
        container=container3,
        message='riki channel riki channel',
    )

    message2 = Message(
        messager=user1,
        container=container3,
        message='hi im riki',
    )

    message3 = Message(
        messager=user1,
        container=container3,
        message='this is my channel',
    )

    message4 = Message(
        messager=user1,
        container=container1,
        message='Hi! welcome to the first channel!'
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(container1)
    db.session.add(container2)
    db.session.add(container3)
    db.session.add(message1)
    db.session.add(message2)
    db.session.add(message3)
    db.session.commit()

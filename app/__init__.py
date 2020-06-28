from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Configuration
from .routes import session, channel
from .models import db


app = Flask(__name__)
CORS(app)
app.config.from_object(Configuration)
app.register_blueprint(session.bp)
app.register_blueprint(channel.bp)
db.init_app(app)
Migrate(app, db)

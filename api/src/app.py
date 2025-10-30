"""
AWS Beanstalk Application Entry Point
Universidad de los Andes - MISW4304
Blacklist Microservice
"""
import os
import logging
from dotenv import load_dotenv
from flask import Flask
from .routes.blacklist_router import blacklist_bp
from .config.config import Config, TestingConfig
from .models.models import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    load_dotenv()

    app = Flask(__name__)

    if os.getenv("FLASK_ENV") == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    app.register_blueprint(blacklist_bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
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
    logger.info("=" * 50)
    logger.info("Creating Flask application...")
    logger.info(f"FLASK_ENV: {os.getenv('FLASK_ENV', 'Not set')}")
    
    logger.info("Loading environment variables...")
    load_dotenv()
    logger.info("Environment variables loaded from .env (if present)")
    logger.info("=" * 50)
    logger.info("Environment variables:")
    logger.info(f"  DB_USER: {'***' if os.getenv('DB_USER') else 'Not set'}")
    logger.info(f"  DB_PASSWORD: {'***' if os.getenv('DB_PASSWORD') else 'Not set'}")
    logger.info(f"  DB_HOST: {os.getenv('DB_HOST') if os.getenv('DB_HOST') else 'Not set'}")
    logger.info(f"  DB_PORT: {os.getenv('DB_PORT') if os.getenv('DB_PORT') else 'Not set'}")
    logger.info(f"  DB_NAME: {os.getenv('DB_NAME') if os.getenv('DB_NAME') else 'Not set'}")
    logger.info(f"  SECRET_TOKEN: {'***' if os.getenv('SECRET_TOKEN') else 'Not set'}")
    logger.info(f"  FLASK_ENV: {os.getenv('FLASK_ENV', 'Not set')}")
    logger.info("=" * 50)
    logger.info("=" * 50)

    app = Flask(__name__)
    logger.info("Flask app instance created")

    if os.getenv("FLASK_ENV") == "testing":
        app.config.from_object(TestingConfig)
        logger.info("Using TestingConfig")
    else:
        app.config.from_object(Config)
        logger.info("Using Config")
        logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[0]}@***")

    app.register_blueprint(blacklist_bp)
    logger.info("Blacklist blueprint registered")

    logger.info("Initializing database...")
    db.init_app(app)
    
    with app.app_context():
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("Database tables created/verified")
    
    logger.info("Flask application created successfully!")
    logger.info("=" * 50)
    return app


# Create app instance for Gunicorn
logger.info("Starting application initialization...")
app = create_app()
logger.info("Application ready to serve requests")

if __name__ == "__main__":
    app.run()
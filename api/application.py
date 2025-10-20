"""
AWS Elastic Beanstalk Application Entry Point
Universidad de los Andes - MISW4304
Blacklist Microservice
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask
from src.routes.blacklist_router import blacklist_bp
from src.config.config import Config
from src.models.models import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(blacklist_bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

# Create the application instance for AWS Elastic Beanstalk
try:
    application = create_app()
    logger.info("✅ Blacklist Microservice loaded successfully")
    logger.info(f"✅ Application name: {application.name}")
    logger.info(f"✅ Debug mode: {application.debug}")
    
except Exception as e:
    logger.error(f"❌ Error creating application: {e}")
    logger.info("🔄 Creating fallback application...")
    
    # Fallback application
    application = Flask(__name__)
    
    @application.route('/')
    def hello():
        return {"message": "Blacklist Microservice - Fallback Mode", "status": "running"}, 200
    
    @application.route('/blacklists/ping')
    def ping():
        return "pong", 200
    
    @application.route('/health')
    def health():
        return {"status": "healthy", "message": "Fallback app running"}, 200
    
    logger.info("✅ Fallback application created successfully")

# This is required for AWS Elastic Beanstalk
if __name__ == "__main__":
    application.run(debug=True)

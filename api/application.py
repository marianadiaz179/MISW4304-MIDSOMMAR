"""
AWS Beanstalk Application Entry Point
Universidad de los Andes - MISW4304
"""
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.app import create_app
    # Create the Flask application
    application = create_app()
except Exception as e:
    print(f"Error creating app: {e}")
    # Fallback simple app
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def hello():
        return "Hello from Beanstalk!"
    
    @application.route('/blacklists/ping')
    def ping():
        return "pong", 200

if __name__ == "__main__":
    application.run()

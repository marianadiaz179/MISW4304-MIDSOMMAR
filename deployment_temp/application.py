"""
AWS Beanstalk Application Entry Point
Universidad de los Andes - MISW4304
"""
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import create_app

# Create the Flask application
application = create_app()

if __name__ == "__main__":
    application.run()

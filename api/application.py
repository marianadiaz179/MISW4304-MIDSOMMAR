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
    # Create the Flask application using your main app
    application = create_app()
    print("✅ Main application loaded successfully")
except Exception as e:
    print(f"❌ Error creating main app: {e}")
    print("🔄 Falling back to simple app...")
    # Fallback simple app if there's an error
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def hello():
        return "Hello from Beanstalk! App is running."
    
    @application.route('/blacklists/ping')
    def ping():
        return "pong", 200
    
    @application.route('/health')
    def health():
        return {"status": "healthy", "message": "Fallback app running"}, 200
    
    print("✅ Fallback application loaded successfully")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000)

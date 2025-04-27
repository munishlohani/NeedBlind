from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pathlib

# Fix for Windows path issues with fastai
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Initialize extensions
cors = CORS()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    
    # Initialize extensions
    cors.init_app(app)

    
    # Import and register routes
    from routes import register_routes
    register_routes(app)
    
    return app 
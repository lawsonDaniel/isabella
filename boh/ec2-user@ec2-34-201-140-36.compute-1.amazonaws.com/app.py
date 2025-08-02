import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS
from routes.routes import initialize_routes
from dotenv import load_dotenv
from config import Config
from db_config import init_db, db
from flask_jwt_extended import JWTManager

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

# Enable CORS for all routes
CORS(app)

app.config.from_object(Config)  # Load configuration from Config class
# Load the API Key from environment variable
app.config['YOUTUBE_API_KEY'] = os.environ.get('YOUTUBE_API_KEY')
app.secret_key = os.environ.get('SECRET_KEY')

init_db(app)  # Initialize SQLAlchemy with the app
migrate = Migrate(app, db)  # Set up Flask-Migrate with app and db
# Initialize routes
initialize_routes(api, app)

# Remove or comment out the following block
if __name__ == "__main__":
    with app.app_context():  # Ensures the app context is available
        db.create_all()
    app.run(debug=True, port=5001)

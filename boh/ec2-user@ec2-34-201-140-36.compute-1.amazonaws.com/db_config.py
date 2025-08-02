from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    # Set the PostgreSQL database URL using an environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URL', 'postgresql://bol_user:W6r7Ih90mM2NIdYlamWgLXVGgfnF7ztQ@dpg-crq710ij1k6c738c9o8g-a.oregon-postgres.render.com/bol')
    db.init_app(app)

import os
from flask import Flask
from config import Config
from .extensions import db, mail

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Try connecting to primary database, fallback to local SQLite if unreachable
    try:
        db.init_app(app)
        with app.app_context():
            # Test DB connection
            db.engine.connect()
    except Exception as e:
        print(f"Warning: Primary database connection failed ({e}). Falling back to local SQLite database.")
        os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.LOCAL_SQLITE_URI
        db.init_app(app)

    mail.init_app(app)

    with app.app_context():
        from . import models, routes
        db.create_all()
        
        # Seed database catalog if empty
        from .seed import seed_database
        try:
            seed_database()
        except Exception as seed_err:
            print(f"Seed note: {seed_err}")

    return app

app = create_app()

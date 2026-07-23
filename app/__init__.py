import os
import pymysql
from flask import Flask
from config import Config
from .extensions import db, mail

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Check if primary remote MySQL is reachable
    use_sqlite = False
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            connect_timeout=3
        )
        connection.close()
    except Exception as e:
        print(f"Notice: Primary MySQL database ({Config.DB_HOST}) not directly reachable from local environment ({e}). Using local SQLite database.")
        use_sqlite = True
        
    if use_sqlite:
        os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.LOCAL_SQLITE_URI

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)
        
        from . import models
        db.create_all()
        
        # Seed database catalog if empty
        from .seed import seed_database
        try:
            seed_database()
        except Exception as seed_err:
            print(f"Seed note: {seed_err}")

    return app

app = create_app()

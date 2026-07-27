import os
try:
    import pymysql
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

from flask import Flask
from config import Config
from .extensions import db, mail

app = Flask(__name__)
app.config.from_object(Config)

# Check if primary remote MySQL is reachable
use_sqlite = False
if HAS_PYMYSQL:
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
else:
    use_sqlite = True

if use_sqlite:
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.LOCAL_SQLITE_URI

db.init_app(app)
mail.init_app(app)

with app.app_context():
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from . import models
    db.create_all()
    
    # Schema migration helper for new admin columns
    try:
        inspector = db.inspect(db.engine)
        tables_columns = {
            'contact_messages': [
                ('status', 'VARCHAR(30) DEFAULT "New"'),
                ('admin_notes', 'TEXT'),
                ('is_read', 'BOOLEAN DEFAULT 0'),
                ('updated_at', 'DATETIME')
            ],
            'enrollment_requests': [
                ('status', 'VARCHAR(30) DEFAULT "Pending"'),
                ('admin_notes', 'TEXT'),
                ('is_read', 'BOOLEAN DEFAULT 0'),
                ('updated_at', 'DATETIME')
            ],
            'consultation_requests': [
                ('status', 'VARCHAR(30) DEFAULT "Pending"'),
                ('admin_notes', 'TEXT'),
                ('is_read', 'BOOLEAN DEFAULT 0'),
                ('updated_at', 'DATETIME')
            ]
        }
        for table, columns in tables_columns.items():
            if inspector.has_table(table):
                existing_cols = [c['name'] for c in inspector.get_columns(table)]
                for col_name, col_type in columns:
                    if col_name not in existing_cols:
                        with db.engine.connect() as conn:
                            conn.execute(db.text(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}"))
                            conn.commit()
    except Exception as mig_err:
        print(f"Migration note: {mig_err}")

    # Seed database catalog if empty
    from .seed import seed_database
    try:
        seed_database()
    except Exception as seed_err:
        print(f"Seed note: {seed_err}")

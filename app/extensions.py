from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security

db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
security = Security()

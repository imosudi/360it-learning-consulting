import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '360it-learning-consulting-secret-key-2026'
    
    # Primary DB configuration as specified in dev_requirements.txt
    DB_USER = os.environ.get('DB_USER', 'debian-sys-maint')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'xZ9AR4WE6wd2qkRr')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_NAME = os.environ.get('DB_NAME', '360it-learning')
    
    MYSQL_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    LOCAL_SQLITE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', '360it_learning.db')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or MYSQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail Config
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'mio3.serverafrica.net')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'info@360it-learning.serverafrica.net')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'info@360it-learning.serverafrica.net')

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '360it-learning-consulting-secret-key-2026'
    
    # Primary DB configuration as specified in dev_requirements.txt
    DB_USER = os.environ.get('DB_USER', '360it-learning')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'just4it-Learning')
    DB_HOST = os.environ.get('DB_HOST', 'mio3.serverafrica.net')
    DB_NAME = os.environ.get('DB_NAME', '360it-learning')
    
    MYSQL_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    LOCAL_SQLITE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', '360it_learning.db')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or MYSQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail Config (AWS SES / Server Africa)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or os.environ.get('360_MAIL_SERVER') or 'email-smtp.us-east-1.amazonaws.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or os.environ.get('360_MAIL_PORT') or 587)
    MAIL_USE_TLS = str(os.environ.get('MAIL_USE_TLS') or os.environ.get('360_MAIL_USE_TLS') or 'True').lower() in ['true', 'on', '1']
    MAIL_USE_SSL = str(os.environ.get('MAIL_USE_SSL') or os.environ.get('360_MAIL_USE_SSL') or 'False').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or os.environ.get('360_MAIL_USERNAME') or 'AKIAR5E3BAJNPMJDJFD2'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or os.environ.get('360_MAIL_PASSWORD') or 'BHo62PF5AJhI8DTvIxr7u0K1Se1dEI/sG9GoY+b9jXK9'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or os.environ.get('360_MAIL_DEFAULT_SENDER') or 'noreply@serverafrica.net'

    # Flask-Security-Too Config
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', '360it-learning-security-salt-2026')
    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False

IP_ADDRESS='0.0.0.0'
PORT=5000

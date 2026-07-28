import pytest
import os
import sys

# Ensure app module is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from app.extensions import db
from app.models import AdminUser

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def admin_user(app):
    user = AdminUser(
        username='testadmin',
        email='testadmin@360it.com',
        full_name='Test Administrator',
        role='Super Admin',
        must_change_password=False
    )
    user.set_password('StrongTestPass123!')
    db.session.add(user)
    db.session.commit()
    return user

def test_admin_login_page_renders(client):
    response = client.get('/admin/login')
    assert response.status_code == 200
    # Verify cleartext credentials tip is not present
    assert b'Default Admin Login: <strong>admin</strong>' not in response.data

def test_admin_login_success(client, admin_user):
    response = client.post('/admin/login', data={
        'username': 'testadmin',
        'password': 'StrongTestPass123!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back' in response.data or b'Dashboard' in response.data

def test_admin_login_invalid_password(client, admin_user):
    response = client.post('/admin/login', data={
        'username': 'testadmin',
        'password': 'WrongPassword'
    })
    assert response.status_code == 200
    assert b'Invalid username/email or password' in response.data

def test_forced_password_change_redirect(client, app):
    from app.extensions import db
    from app.models import AdminUser
    
    with app.app_context():
        user = AdminUser(
            username='mustchange',
            email='mustchange@360it.com',
            full_name='Temp Admin',
            role='Super Admin',
            must_change_password=True
        )
        user.set_password('TempPass123!')
        db.session.add(user)
        db.session.commit()
    
    # Login with must_change_password=True user
    client.post('/admin/login', data={
        'username': 'mustchange',
        'password': 'TempPass123!'
    })
    
    # Access dashboard should redirect to change-password
    response = client.get('/admin/dashboard')
    assert response.status_code == 302
    assert '/admin/change-password' in response.headers['Location']

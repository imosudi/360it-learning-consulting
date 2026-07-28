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

def test_admin_create_course_flow(client, admin_user):
    client.post('/admin/login', data={
        'username': 'testadmin',
        'password': 'StrongTestPass123!'
    })
    
    # Render create course form
    get_res = client.get('/admin/courses/create')
    assert get_res.status_code == 200
    assert b'Create New Training Course' in get_res.data
    
    # Submit create course
    post_res = client.post('/admin/courses/create', data={
        'title': 'Test Kubernetes Masterclass',
        'icon': 'fa-cubes',
        'duration': '6 Weeks',
        'delivery_mode': 'Online Live Interactive',
        'skill_level': 'Intermediate to Advanced',
        'short_desc': 'Comprehensive hands-on Kubernetes orchestration training.',
        'syllabus_list': 'Module 1|Module 2',
        'featured': 'y'
    }, follow_redirects=True)
    assert post_res.status_code == 200
    assert b'Test Kubernetes Masterclass' in post_res.data

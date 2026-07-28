def test_homepage_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'360IT Learning' in response.data or b'Consulting' in response.data

def test_about_route(client):
    response = client.get('/about')
    assert response.status_code == 200

def test_services_route(client):
    response = client.get('/services')
    assert response.status_code == 200

def test_courses_route(client):
    response = client.get('/courses')
    assert response.status_code == 200

def test_contact_route_get(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact 360IT' in response.data or b'Send Us a Message' in response.data

def test_privacy_route(client):
    response = client.get('/privacy')
    assert response.status_code == 200

def test_terms_route(client):
    response = client.get('/terms')
    assert response.status_code == 200

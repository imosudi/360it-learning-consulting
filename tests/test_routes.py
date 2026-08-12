def test_homepage_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Enterprise Technology' in response.data
    assert b'Engineering the Future of' in response.data
    assert b'360IT delivers enterprise software, cloud infrastructure, ERP solutions' in response.data
    assert b'Request a Consultation' in response.data
    assert b'Explore Solutions' in response.data
    assert b'Years of Experience' in response.data
    assert b'Enterprise Projects' in response.data
    assert b'Professionals Trained' in response.data
    assert b'Technology That Moves Business Forward' in response.data
    assert b'Deliver innovative technology solutions that simplify, automate, and accelerate business success.' in response.data
    assert b'To become a trusted global partner in enterprise technology and digital transformation.' in response.data
    assert b'Enterprise Technology Solutions' in response.data
    assert b'Why 360IT?' in response.data

def test_about_route(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'Technology That Moves Business Forward' in response.data

def test_services_route(client):
    response = client.get('/services')
    assert response.status_code == 200
    assert b'Enterprise Technology Solutions' in response.data

def test_training_route(client):
    response = client.get('/training')
    assert response.status_code == 200

def test_contact_route_get(client):
    response = client.get('/contact')
    assert response.status_code == 200

def test_projects_route(client):
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'DELIVERED ENGAGEMENTS' in response.data
    assert b'Proven Delivery. Trusted Enterprise Solutions.' in response.data
    assert b'Enterprise Multi-Region Cloud Migration' in response.data
    assert b'Government Health Platform Modernization' in response.data
    assert b'Telecommunications Infrastructure Modernization' in response.data
    assert b'Government Digital Transformation' in response.data
    assert b'Enterprise Workflow &amp; Business Rules Automation' in response.data or b'Enterprise Workflow' in response.data
    assert b'Enterprise Document Automation' in response.data
    assert b'High-Availability Database Solutions' in response.data
    assert b'Cybersecurity Assessment &amp; Infrastructure Hardening' in response.data or b'Cybersecurity Assessment' in response.data
    assert b'Enterprise Analytics &amp; Business Intelligence' in response.data or b'Enterprise Analytics' in response.data
    assert b'Enterprise Commerce Platform' in response.data
    assert b'24/7 Managed Infrastructure Services' in response.data
    assert b'Ready to Transform Your Business?' in response.data



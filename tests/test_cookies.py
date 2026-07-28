import pytest

def test_cookie_consent_banner_in_response(client):
    """Test that the cookie consent banner partial is rendered in HTML responses."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'cookieBanner' in response.data
    assert b'Cookie & Privacy Preferences' in response.data
    assert b'btnCookieAcceptAll' in response.data
    assert b'btnCookieEssential' in response.data

def test_session_cookie_security_config(app):
    """Test that session cookie security configurations are properly set."""
    assert app.config['SESSION_COOKIE_HTTPONLY'] is True
    assert app.config['SESSION_COOKIE_SAMESITE'] == 'Lax'
    assert app.config['REMEMBER_COOKIE_HTTPONLY'] is True
    assert app.config['REMEMBER_COOKIE_SAMESITE'] == 'Lax'

def test_privacy_policy_cookie_section_rendered(client):
    """Test that Privacy Policy renders cookie information."""
    response = client.get('/privacy')
    assert response.status_code == 200
    assert b'Cookies & Tracking Technologies' in response.data

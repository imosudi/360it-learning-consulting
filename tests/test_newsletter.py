import io
from app.models import NewsletterSubscriber
from app.extensions import db


def test_public_newsletter_subscription(client, app):
    """Test public newsletter subscription form submission."""
    response = client.post('/newsletter-subscribe', data={
        'email': 'subscriber@example.com',
        'source': 'Footer Form'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Thank you for subscribing' in response.data

    with app.app_context():
        sub = NewsletterSubscriber.query.filter_by(email='subscriber@example.com').first()
        assert sub is not None
        assert sub.status == 'Subscribed'
        assert sub.source == 'Footer Form'


def test_duplicate_newsletter_subscription(client, app):
    """Test duplicate newsletter subscription handling."""
    with app.app_context():
        sub = NewsletterSubscriber(email='existing@example.com', status='Subscribed')
        db.session.add(sub)
        db.session.commit()

    response = client.post('/newsletter-subscribe', data={
        'email': 'existing@example.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'already subscribed' in response.data


def test_admin_newsletter_subscribers_management(client, app):
    """Test admin newsletter management dashboard, status filtering, and toggling."""
    with app.app_context():
        sub1 = NewsletterSubscriber(email='user1@example.com', status='Subscribed')
        sub2 = NewsletterSubscriber(email='user2@example.com', status='Unsubscribed')
        db.session.add_all([sub1, sub2])
        db.session.commit()
        sub1_id = sub1.id

    with client.session_transaction() as sess:
        sess['admin_user_id'] = 1

    # Access management dashboard
    response = client.get('/admin/newsletter-subscribers')
    assert response.status_code == 200
    assert b'user1@example.com' in response.data
    assert b'user2@example.com' in response.data

    # Toggle status of user1
    toggle_res = client.post(f'/admin/newsletter-subscribers/{sub1_id}/toggle', follow_redirects=True)
    assert toggle_res.status_code == 200

    with app.app_context():
        updated_sub = db.session.get(NewsletterSubscriber, sub1_id)
        assert updated_sub.status == 'Unsubscribed'


def test_admin_newsletter_export_csv(client, app):
    """Test admin CSV export of subscribers."""
    with app.app_context():
        sub = NewsletterSubscriber(email='export@example.com', status='Subscribed', source='Homepage')
        db.session.add(sub)
        db.session.commit()

    with client.session_transaction() as sess:
        sess['admin_user_id'] = 1

    response = client.get('/admin/export/newsletter-subscribers')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert b'export@example.com' in response.data
    assert b'Homepage' in response.data

def test_admin_newsletter_subscribers_dummy_route(client):
    """Test accessing dummy newsletter subscribers management page in admin."""
    with client.session_transaction() as sess:
        sess['admin_user_id'] = 1

    response = client.get('/admin/newsletter-subscribers')
    assert response.status_code == 200
    assert b'Newsletter Subscribers' in response.data
    assert b'john.doe@enterprise.com' in response.data
    assert b'Subscribed' in response.data


def test_admin_export_newsletter_subscribers_dummy_route(client):
    """Test exporting dummy newsletter subscribers CSV."""
    with client.session_transaction() as sess:
        sess['admin_user_id'] = 1

    response = client.get('/admin/export/newsletter-subscribers')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert b'Email Address' in response.data
    assert b'john.doe@enterprise.com' in response.data

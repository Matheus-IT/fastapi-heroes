def test_health_check(client):
    """Test the health check endpoint is working"""
    response = client.get("/")
    assert response.status_code == 200

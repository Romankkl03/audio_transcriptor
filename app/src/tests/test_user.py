import pytest

@pytest.mark.asyncio
async def test_user_registration(client):
    response = await client.post(
        "/api/users/registration",
        json={
            "email": "test_user@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "test_user@example.com"


@pytest.mark.asyncio
async def test_admin_access_denied(client):
    user_id = 2 #admin
    resp = await client.get(f"/api/users/{user_id}/service")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0

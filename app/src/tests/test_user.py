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

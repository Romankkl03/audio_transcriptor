import pytest


@pytest.mark.asyncio
async def test_duplicate_user_registration(client):
    payload = {"email": "dup@test.com", "password": "123456"}

    await client.post("/api/users/registration", json=payload)

    resp = await client.post("/api/users/registration", json=payload)

    assert resp.status_code == 500

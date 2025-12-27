import pytest

@pytest.mark.asyncio
async def test_login_success(client):
    resp = await client.post(
        "/api/users/registration",
        json={"email": "test@test.com", "password": "20252025"}
    )
    assert resp.status_code == 200

    resp = await client.post(
        "/api/users/auntification",
        json={"email": "test@test.com", "password": "20252025"}
    )

    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    resp = await client.post(
        "/api/users/auntification",
        json={"email": "test@test.com", "password": "123456"}
    )

    assert resp.status_code == 403

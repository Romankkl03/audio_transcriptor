import pytest


@pytest.mark.asyncio
async def test_threads_user_not_found(client):
    user_id = 99999
    resp = await client.get(f"/api/thread/{user_id}/threads")
    assert resp.status_code in (200, 404)


@pytest.mark.asyncio
async def test_admin_access_denied(client):
    resp = await client.post(
        "/api/users/registration",
        json={"email": "service@test.com", "password": "123456"}
    )
    assert resp.status_code == 200
    user_id = resp.json()["id"]
    resp = await client.get(f"/api/users/{user_id}/service")
    assert resp.status_code == 403
    assert resp.json()["detail"] == "This operation is forbidden."

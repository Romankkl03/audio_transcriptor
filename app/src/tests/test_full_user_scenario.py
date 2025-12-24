import pytest


@pytest.mark.asyncio
async def test_full_user_flow(client):
    resp = await client.post(
        "/api/users/registration",
        json={"email": "flow@test.com", "password": "123456"}
    )
    assert resp.status_code == 200
    user_id = resp.json()["id"]

    await client.post(
        f"/api/balance/{user_id}/new_balance",
        json={"user_id": user_id, "amount": 0}
    )

    resp = await client.post(
        f"/api/balance/{user_id}/credit",
        json={"user_id": user_id, "amount": 100}
    )
    assert resp.json()["balance"] == 100

    resp = await client.post(
        f"/api/thread/{user_id}/predictions",
        json={
            "user_id": user_id,
            "audio_name": "test.mp3",
            "duration": 5,
            "content": "hello"
        }
    )
    assert resp.status_code == 200

    resp = await client.post(
        f"/api/balance/{user_id}/credit",
        json={"user_id": user_id, "amount": 0}
    )
    assert resp.json()["balance"] == 50

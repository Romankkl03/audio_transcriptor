import pytest


@pytest.mark.asyncio
async def test_not_enough_balance(client):
    resp = await client.post(
        "/api/users/registration",
        json={"email": "poor@test.com", "password": "123456"}
    )
    user_id = resp.json()["id"]

    await client.post(
        f"/api/balance/{user_id}/new_balance",
        json={"user_id": user_id, "amount": 0}
    )

    resp = await client.post(
        f"/api/thread/{user_id}/predictions",
        json={
            "user_id": user_id,
            "audio_name": "test.mp3",
            "duration": 10,
            "content": "hello"
        }
    )

    assert resp.status_code == 402
    assert resp.json()["detail"] == "Not enough balance"

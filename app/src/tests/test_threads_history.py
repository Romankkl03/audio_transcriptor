import pytest

@pytest.mark.asyncio
async def test_get_threads_history(client):
    resp = await client.post(
        "/api/users/registration",
        json={"email": "threads@test.com", "password": "123456"}
    )
    assert resp.status_code == 200
    user_id = resp.json()["id"]

    await client.post(
        f"/api/balance/{user_id}/new_balance",
        json={"user_id": user_id, "amount": 100}
    )

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

    resp = await client.get(f"/api/thread/{user_id}/threads")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["audio_name"] == "test.mp3"  

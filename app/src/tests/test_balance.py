import pytest

@pytest.mark.asyncio
async def test_create_and_increase_balance(client):
    user_resp = await client.post(
        "/api/users/registration",
        json={"email": "balance_user@test.com", "password": "123456"}
    )
    user_id = user_resp.json()["id"]

    balance_resp = await client.post(
        f"/api/balance/{user_id}/new_balance",
        json={"user_id": user_id, "amount": 100}
    )
    assert balance_resp.status_code == 200

    inc_resp = await client.post(
        f"/api/balance/{user_id}/credit",
        json={"user_id": user_id, "amount": 50}
    )
    assert inc_resp.status_code == 200
    assert inc_resp.json()["balance"] == 150

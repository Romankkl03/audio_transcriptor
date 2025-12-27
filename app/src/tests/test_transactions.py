import pytest

@pytest.mark.asyncio
async def test_transactions_history(client):
    user_resp = await client.post(
        "/api/users/registration",
        json={"email": "trx@test.com", "password": "123456"}
    )
    user_id = user_resp.json()["id"]
    await client.post(
        f"/api/balance/{user_id}/new_balance",
        json={"user_id": user_id, "amount": 200}
    )

    trx_resp = await client.post(
        f"/api/transactions/{user_id}/new_transactions",
        json={
            "user_id": user_id,
            "amount": 50,
            "type": "debit"
        }
    )

    assert trx_resp.status_code == 200

    history = await client.get(
        f"/api/transactions/{user_id}/transactions_history"
    )

    assert history.status_code == 200
    data = history.json()["transactions"]
    assert len(data) >= 1
    assert data[0]["amount"] == 50

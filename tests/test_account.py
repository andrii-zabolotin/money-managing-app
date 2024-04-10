from httpx import AsyncClient


async def test_create_account(
        ac: AsyncClient,
        authenticated_user_cookie: dict,
        get_or_create_currency_id: int,
        get_or_create_user_id: int,
) -> None:
    response = await ac.post(
        "/account/create",
        cookies=authenticated_user_cookie,
        json={
            "name": "MonoBank",
            "note": "Food",
            "summ": 1000,
            "is_savings_account": False,
            "image_url": None,
            "fk_currency_id": get_or_create_currency_id,
            "fk_user_id": get_or_create_user_id,
        }
    )
    assert response.status_code == 201

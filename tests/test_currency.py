from httpx import AsyncClient


async def test_currency_create(ac: AsyncClient, authenticated_superuser_cookie: dict) -> None:
    response = await ac.post(
        "/currency/create",
        json={"name": "Гривня", "symbol": "UAH"},
        cookies=authenticated_superuser_cookie
    )
    assert response.status_code == 201


async def test_currency_create_error(ac: AsyncClient, authenticated_user_cookie: dict) -> None:

    response = await ac.post(
        "/currency/create",
        json={"name": "Гривня", "symbol": "UAH"},
        cookies=authenticated_user_cookie
    )

    assert response.status_code == 400


async def test_get_currency(ac: AsyncClient) -> None:
    response = await ac.get("/currency/list")

    assert response.status_code == 200


async def test_update_currency(ac: AsyncClient, authenticated_superuser_cookie: dict) -> None:
    response = await ac.patch("/currency/update/1", json={"name": "UAH"}, cookies=authenticated_superuser_cookie)
    print(response.json(), "||||||")
    response = await ac.get("/currency/list/1")
    print(response.json())

from httpx import AsyncClient


async def test_currency_create(ac: AsyncClient, authenticated_superuser_cookie: dict) -> None:
    response = await ac.post(
        "/currency/create",
        json={"name": "Гривня", "symbol": "UAH"},
        cookies=authenticated_superuser_cookie
    )
    assert response.status_code == 201


async def test_get_currency(ac: AsyncClient) -> None:
    response = await ac.get("/currency/list")

    assert response.status_code == 200


async def test_get_currency_by_id(ac: AsyncClient) -> None:
    response = await ac.get("/currency/1")

    assert response.status_code == 200
    assert response.json()["symbol"] == "UAH"


async def test_update_currency(ac: AsyncClient, authenticated_superuser_cookie: dict) -> None:
    response = await ac.patch("/currency/update/1", json={"name": "UAH"}, cookies=authenticated_superuser_cookie)
    updated_currency = await ac.get("/currency/1")

    assert response.status_code == 200
    assert updated_currency.json()["name"] == "UAH"


async def test_delete_currency(ac: AsyncClient, authenticated_superuser_cookie: dict) -> None:
    response = await ac.delete("/currency/delete/1", cookies=authenticated_superuser_cookie)

    assert response.status_code == 200

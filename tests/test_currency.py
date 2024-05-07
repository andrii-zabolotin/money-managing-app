from httpx import AsyncClient


class TestCurrency:
    currency_id = None

    async def test_currency_create(self, ac: AsyncClient, authenticated_superuser_cookie: dict) -> None:
        response = await ac.post(
            "/currency/create",
            json={"name": "Гривня", "symbol": "UAH"},
            cookies=authenticated_superuser_cookie
        )
        TestCurrency.currency_id = response.json()["id"]
        assert response.status_code == 201

    async def test_get_currency(self, ac: AsyncClient) -> None:
        response = await ac.get("/currency/list")

        assert response.status_code == 200

    async def test_get_currency_by_id(self, ac: AsyncClient) -> None:
        response = await ac.get(f"/currency/{self.currency_id}")

        assert response.status_code == 200
        assert response.json()["symbol"] == "UAH"

    async def test_update_currency(self, ac: AsyncClient, authenticated_superuser_cookie: dict) -> None:
        response = await ac.patch(f"/currency/update/{self.currency_id}", json={"name": "UAH"}, cookies=authenticated_superuser_cookie)

        assert response.status_code == 200
        assert response.json()["name"] == "UAH"

    async def test_delete_currency(self, ac: AsyncClient, authenticated_superuser_cookie: dict) -> None:
        response = await ac.delete(f"/currency/delete/{self.currency_id}", cookies=authenticated_superuser_cookie)
        assert response.status_code == 200

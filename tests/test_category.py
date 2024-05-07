from httpx import AsyncClient


class TestCategory:
    category_id = None

    async def test_category_create(self, ac: AsyncClient, authenticated_user_cookie: dict, get_or_create_currency_id: int) -> None:
        response = await ac.post(
            "/category/create",
            json={"name": "Приват", "fk_currency_id": get_or_create_currency_id},
            cookies=authenticated_user_cookie
        )

        assert response.status_code == 201
        TestCategory.category_id = response.json()["id"]

    async def test_get_category(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.get("/category/list", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_get_category_by_id(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.get(f"/category/{self.category_id}", cookies=authenticated_user_cookie)

        assert response.status_code == 200
        assert response.json()["name"] == "Приват"

    async def test_update_category(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.patch(f"/category/update/{self.category_id}", json={"name": "UAH"}, cookies=authenticated_user_cookie)

        assert response.status_code == 200
        assert response.json()["name"] == "UAH"

    async def test_delete_category(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.delete(f"/category/delete/{self.category_id}", cookies=authenticated_user_cookie)
        assert response.status_code == 200

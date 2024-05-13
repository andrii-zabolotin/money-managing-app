from httpx import AsyncClient


class TestAccount:
    account_id = None

    async def test_create_account(
            self,
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
        TestAccount.account_id = response.json()["id"]

    async def test_list_account(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.get("/account/list", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_get_account(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.get(f"/account/{self.account_id}", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_update_account(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.patch(
            f"/account/update/{self.account_id}",
            cookies=authenticated_user_cookie,
            json={
                "name": "Jank",
            }
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Jank"

    async def test_delete_account(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.delete(f"/account/delete/{self.account_id}", cookies=authenticated_user_cookie)

        assert response.status_code == 200

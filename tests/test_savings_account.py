from httpx import AsyncClient


class TestSavingsAccount:
    savings_account_id: None

    async def test_create_savings_account(
            self,
            ac: AsyncClient,
            get_or_create_currency_id: int,
            authenticated_user_cookie: dict,
    ):
        response = await ac.post("/account/savings/create", cookies=authenticated_user_cookie, json={
            "account": {
                "name": "string",
                "note": "string",
                "summ": 0,
                "is_savings_account": False,
                "image_url": "string",
                "fk_currency_id": get_or_create_currency_id
            },
            "target": 0
        })

        assert response.status_code == 201
        TestSavingsAccount.savings_account_id = response.json()["id"]

    async def test_list_savings_account(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
    ):
        response = await ac.get("/account/savings/list", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_get_savings_account(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
    ):
        response = await ac.get(f"/account/savings/{self.savings_account_id}", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_update_savings_account(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
    ):
        response = await ac.patch(
            f"/account/savings/update/{self.savings_account_id}",
            cookies=authenticated_user_cookie,
            json={
                "target": 2000
            }
        )

        assert response.status_code == 200
        assert response.json()["target"] == 2000

    async def test_delete_savings_account(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
    ):
        response = await ac.delete(
            f"/account/savings/delete/{self.savings_account_id}",
            cookies=authenticated_user_cookie
        )

        assert response.status_code == 204

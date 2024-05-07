from httpx import AsyncClient


class TestOperation:
    operation_id = None

    async def test_create_operation(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
            get_or_create_category_id: int,
            get_or_create_account_id: int,
    ) -> None:
        response = await ac.post(
            "/operation/create",
            cookies=authenticated_user_cookie,
            json={
                "summ": 800,
                "type": True,
                "fk_account_id": get_or_create_account_id,
                "fk_category_id": get_or_create_category_id,
            }
        )

        assert response.status_code == 201
        TestOperation.operation_id = response.json()["id"]

    async def test_list_operation(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.get("/operation/list", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_get_operation(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.get(f"/operation/{self.operation_id}", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_update_operation(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.patch(
            f"/operation/update/{self.operation_id}",
            cookies=authenticated_user_cookie,
            json={
                "summ": 1000,
            }
        )

        assert response.status_code == 200
        assert response.json()["summ"] == 1000

    async def test_delete_operation(self, ac: AsyncClient, authenticated_user_cookie: dict) -> None:
        response = await ac.delete(f"/operation/delete/{self.operation_id}", cookies=authenticated_user_cookie)

        assert response.status_code == 200

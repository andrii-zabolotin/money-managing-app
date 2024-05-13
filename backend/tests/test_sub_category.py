from httpx import AsyncClient


class TestSubCategory:
    sub_category_id: None

    async def test_create_sub_category(
            self,
            ac: AsyncClient,
            get_or_create_category_id: int,
            authenticated_user_cookie: dict,
    ):
        response = await ac.post(
            "/sub-category/create",
            cookies=authenticated_user_cookie,
            json={
                "name": "Gym",
                "fk_category_id": get_or_create_category_id,
            }
        )

        assert response.status_code == 201
        TestSubCategory.sub_category_id = response.json()["id"]

    async def test_get_sub_category_list(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
    ):
        response = await ac.get("/sub-category/list", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_get_sub_category(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
    ):
        response = await ac.get(f"/sub-category/{self.sub_category_id}", cookies=authenticated_user_cookie)

        assert response.status_code == 200

    async def test_update_sub_category(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
    ):
        response = await ac.patch(
            f"/sub-category/update/{self.sub_category_id}",
            cookies=authenticated_user_cookie,
            json={
                "name": "Apolo"
            }
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Apolo"

    async def test_delete_sub_category(
            self,
            ac: AsyncClient,
            authenticated_user_cookie: dict,
    ):
        response = await ac.delete(
            f"/sub-category/delete/{self.sub_category_id}",
            cookies=authenticated_user_cookie
        )

        assert response.status_code == 204

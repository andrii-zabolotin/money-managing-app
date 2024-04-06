from httpx import AsyncClient


async def test_get_currency(ac: AsyncClient) -> None:
    response = await ac.get("/currency/list")

    assert response.status_code == 200

import asyncio
import logging

import httpx

from bot.core.config import settings
from bot.schemas.user import PaginatedUsersResponseDTO, UserCreateDTO, UserResponseDTO

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self) -> None:
        limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)

        self.client = httpx.AsyncClient(base_url=settings.API_BASE_URL, limits=limits, timeout=httpx.Timeout(15.0))

    async def close(self) -> None:
        await self.client.aclose()

    async def _request(self, method: str, url: str, retries: int = 3, **kwargs) -> httpx.Response:
        for attempt in range(1, retries + 1):
            try:
                response = await self.client.request(method, url, **kwargs)

                if response.status_code >= 500:
                    raise httpx.HTTPStatusError("Server error", request=response.request, response=response)

                return response
            except (httpx.ConnectError, httpx.ReadTimeout, httpx.HTTPStatusError) as e:
                if attempt == retries:
                    logger.error(f"API CLIENT ERROR: Запрос к {url} провалился, попытки: {retries}")
                    raise e

                wait_time = 2**attempt
                logger.warning(f"Ошибка сети. Попытка {attempt}/{retries}. Ждем {wait_time}с.")
                await asyncio.sleep(wait_time)

    async def list_users(self, cursor: int | None = None, limit: int = 100) -> PaginatedUsersResponseDTO:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        response = await self._request("GET", "/users/", params=params)
        response.raise_for_status()
        return PaginatedUsersResponseDTO(**response.json())

    async def create_user(self, payload: UserCreateDTO) -> UserResponseDTO:
        response = await self._request("POST", "/users/", json=payload.model_dump())
        if response.status_code == 409:
            raise ValueError("Пользователь с данным email уже существует")

        response.raise_for_status()
        return UserResponseDTO(**response.json())

    async def delete_user(self, user_id: int) -> bool:
        response = await self._request("DELETE", f"/users/{user_id}")
        if response.status_code == 404:
            raise ValueError(f"Пользователь с ID {user_id} не найден.")
        response.raise_for_status()
        return True


api_client = APIClient()

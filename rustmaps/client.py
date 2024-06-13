# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from .errors import GeneralHTTPError
from .http import HTTPClient, Route

if TYPE_CHECKING:
    import aiohttp

__all__ = ("Client",)


class Client:
    """A client for interacting with the Rust Maps API."""

    def __init__(
        self,
        api_key: str,  # TODO: Add InvalidTokenError check to this.
        *,
        loop: asyncio.AbstractEventLoop | None = None,
        connector: aiohttp.BaseConnector | None = None,
    ) -> None:
        self.api_key = api_key

        if loop is None:
            self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        else:
            self.loop: asyncio.AbstractEventLoop = loop

        self.http = HTTPClient(connector, loop=self.loop)

    async def get_map(self, map_id: str) -> dict[str, Any] | None:
        """Get a map by its ID.

        Parameters
        ----------
        map_id : str
            The ID of the map to get.
        """
        route = Route("GET", f"/maps/{map_id}")
        try:
            response = await self.http.request(route, headers={"X-API-Key": self.api_key})
            if not isinstance(response, dict) or "data" not in response:
                return None
            return response["data"]
        except GeneralHTTPError:
            # Don't need to add anything here as the HTTPClient already handles the errors.
            return None

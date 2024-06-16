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
        api_key: str,
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

    @property
    async def limits(self) -> dict[str, Any] | None:
        """Get the current rate limits."""
        route = Route("GET", "/maps/limits")
        try:
            response = await self.http.request(route, headers={"X-API-Key": self.api_key})
            if not isinstance(response, dict) or "data" not in response:
                return None
            return response["data"]
        except GeneralHTTPError:
            # Don't need to add anything here as the HTTPClient already handles the errors.
            return None

    async def get_map(self, map_id: str, *, staging: bool = False) -> dict[str, Any] | None:
        """Get a map by its ID.

        Parameters
        ----------
        map_id : str
            The ID of the map to get.
        """
        route = Route("GET", f"/maps/{map_id}", staging=str(staging).lower())
        try:
            response = await self.http.request(route, headers={"X-API-Key": self.api_key})
            if not isinstance(response, dict) or "data" not in response:
                return None
            return response["data"]
        except GeneralHTTPError:
            # Don't need to add anything here as the HTTPClient already handles the errors.
            return None

    async def get_map_ss(
        self,
        seed: int,
        size: int,
        *,
        staging: bool = False,
    ) -> dict[str, Any] | None:
        """Get a map by its seed and size.

        Parameters
        ----------
        seed : int
            The seed of the map to get.
        size : int
            The size of the map to get.
        """
        route = Route("GET", f"/maps/{size}/{seed}", staging=str(staging).lower())
        try:
            response = await self.http.request(route, headers={"X-API-Key": self.api_key})
            if not isinstance(response, dict) or "data" not in response:
                return None
            return response["data"]
        except GeneralHTTPError:
            # Don't need to add anything here as the HTTPClient already handles the errors.
            return None

    async def create_map(self) -> dict[str, Any] | None:
        """Create a map with random seed and size."""
        route = Route("POST", "/maps")
        try:
            response = await self.http.request(route, headers={"X-API-Key": self.api_key})
            if not isinstance(response, dict) or "data" not in response:
                return None
            return response["data"]
        except GeneralHTTPError:
            # Don't need to add anything here as the HTTPClient already handles the errors.
            return None

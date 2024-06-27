# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import typing as t
from typing import Any, ClassVar

import aiohttp
import yarl

from .errors import (
    Forbidden,
    HTTPException,
    NotFinishedGenerating,
    NotFound,
    Unauthorized,
)

if t.TYPE_CHECKING:
    import asyncio

    from aiohttp import ClientSession

__all__ = (
    "Route",
    "HTTPClient",
    "json_or_text",
)

_log = logging.getLogger(__name__)


async def json_or_text(
    response: aiohttp.ClientResponse,
) -> dict[str, Any] | list[dict[str, Any]] | str:
    """
    Process an `aiohttp.ClientResponse` to return either a JSON object or raw tex.

    This function attempts to parse the response as JSON. If the content type of the response is not
    application/json or parsing fails, it falls back to returning the raw text of the response.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        The response object to process.

    Returns
    -------
    dict[str, Any] | list[dict[str, Any]] | str
        The parsed JSON object as a dictionary or list of dictionaries, or the raw response tex
    """
    try:
        if "application/json" in response.headers["content-type"].lower():
            return await response.json()
    except KeyError:
        # Thanks Cloudflare
        pass

    return await response.text(encoding="utf-8")


class Route:
    """Handle route construction for HTTP requests."""

    BASE: ClassVar[str] = "https://api.rustmaps.com/v4"

    def __init__(self, method: str, path: str, **parameters: int | str | bool) -> None:
        self.method = method
        self.path = path
        self.parameters = parameters

        url = self.BASE + self.path
        if parameters:
            url = yarl.URL(url).with_query(parameters).human_repr()
        self.url: str = url


class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the Rustmaps API."""

    def __init__(
        self,
        connector: aiohttp.BaseConnector | None = None,
        *,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self.loop: asyncio.AbstractEventLoop = loop
        self.connector = connector
        self.__session: ClientSession = aiohttp.ClientSession()

    def ensure_session(self) -> None:
        """
        Ensure that an aiohttp.ClientSession is created and open.

        If a session does not exist or is closed, this method creates a new aiohttp.ClientSession
        using the provided connector and loop.
        """
        if not self.__session or self.__session.closed:
            self.__session = aiohttp.ClientSession(connector=self.connector, loop=self.loop)

    async def close(self) -> None:
        """Close the aiohttp.ClientSession."""
        if self.__session and not self.__session.closed:
            await self.__session.close()

    async def request(
        self,
        route: Route,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]] | str:
        """
        Send a request to the specified route and returns the response.

        This method constructs and sends an HTTP request based on the specified route and headers.
        It processes the response to return JSON data or raw text, handling errors as needed.

        Parameters
        ----------
        route : Route
            The route object containing the method and URL for the reques
        headers : dict[str, str] | None, optional
            Optional headers to include with the reques Defaults to None.

        Returns
        -------
        dict[str, Any] | list[dict[str, Any]] | str
            The response data as a parsed JSON object or list, or raw text if JSON parsing is
            not applicable.

        Raises
        ------
        GeneralHTTPError
            Will raise if the request fails or the response indicates an error.
        """
        self.ensure_session()

        method = route.method
        url = route.url

        _headers = {"Accept": "application/json"}

        if headers:
            headers.update(**_headers)
        else:
            headers = _headers

        async with self.__session.request(method, url, headers=headers) as response:
            _log.debug(f"{method} {url} returned {response.status}")

            # errors typically have text involved, so this should be safe 99.5% of the time.
            data = await json_or_text(response)
            _log.debug(f"{method} {url} received {data}")

            # I do it this way because some endpoints can return 201.
            if response.status in [200, 201]:
                return data

            if response.status == 401:
                await self.close()
                raise Unauthorized(response, data)
            if response.status == 403:
                raise Forbidden(response, data)
            if response.status == 404:
                raise NotFound(response, data)
            if response.status == 409:
                raise NotFinishedGenerating(response, data)

            raise HTTPException(response, data)

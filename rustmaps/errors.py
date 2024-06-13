# SPDX-License-Identifier: MIT

import logging

_log = logging.getLogger(__name__)

__all__ = (
    "BaseBotError",
    "GeneralHTTPError",
)


class BaseBotError(Exception):
    """Base bot error all custom errors inherit from."""


class GeneralHTTPError(Exception):
    """General HTTP error."""

    def __init__(self, method: str, url: str, status: int) -> None:
        msg = f"{method} request to {url} failed - {status}"
        _log.error(msg)

        super().__init__(f"Request to {url} failed - {status}")
        self.status = status


class InvalidTokenError(Exception):
    """Raised when an invalid token is passed to the client."""

    def __init__(self, token: str) -> None:
        msg = f"Invalid token: {token}"
        _log.error(msg)

        super().__init__(msg)

# SPDX-License-Identifier: MIT
from __future__ import annotations

import logging
import typing as t

if t.TYPE_CHECKING:
    from typing import Any

    from aiohttp import ClientResponse

_log = logging.getLogger(__name__)

__all__ = (
    "HTTPException",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "NotFinishedGenerating",
)


def _flatten_error_dict(d: dict[str, Any], key: str = "") -> dict[str, str]:
    items: list[tuple[str, str]] = []
    for k, v in d.items():
        new_key = f"{key}.{k}" if key else k

        if isinstance(v, dict):
            try:
                _errors: list[dict[str, Any]] = v["_errors"]
            except KeyError:
                items.extend(_flatten_error_dict(v, new_key).items())
            else:
                items.append((new_key, " ".join(x.get("message", "") for x in _errors)))
        else:
            items.append((new_key, v))

    return dict(items)


class HTTPException(Exception):
    """Base exception for all HTTP exceptions."""

    def __init__(self, response: ClientResponse, message: str | dict[str, Any]) -> None:
        self.response = response
        self.status = response.status
        self.message = message

        self.code: int
        self.text: str
        if isinstance(message, dict):
            self.code = message.get("code", 0)
            base = message.get("message", "")
            errors = message.get("errors")
            if errors:
                errors = _flatten_error_dict(errors)
                helpful = "\n".join(f"In {k}: {m}" for k, m in errors.items())
                self.text = base + "\n" + helpful
            else:
                self.text = base
        else:
            self.text = message or ""
            self.code = 0

        fmt = "{0.status} {0.reason} (error code: {1})"
        if len(self.text):
            fmt += ": {2}"
        super().__init__(fmt.format(self.response, self.code, self.text))


class Unauthorized(HTTPException):
    """Raised when a 401 status code is returned from the API."""


class Forbidden(HTTPException):
    """Raised when a 403 status code is returned from the API."""


class NotFound(HTTPException):
    """Raised when a 404 status code is returned from the API."""


class NotFinishedGenerating(HTTPException):
    """Raised when a 409 status code is returned from the API."""

# SPDX-License-Identifier: MIT

import asyncio
import logging

from rich import print

from rustmaps import Client


async def main() -> None:
    """Run main."""
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("rustmaps").setLevel(logging.DEBUG)

    client = Client("f808bde9d91244b788ea145eff54497f")

    saved_configs = await client.saved_configs
    print(saved_configs)
    await client.http.close()


if __name__ == "__main__":
    asyncio.run(main())

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

    map_seed = input("Enter a map seed: ")
    map_size = input("Enter a map size: ")
    found_map = await client.get_map_ss(int(map_seed), int(map_size))
    print(found_map)
    await client.http.close()


if __name__ == "__main__":
    asyncio.run(main())

# SPDX-License-Identifier: MIT

import asyncio

from rich import print

from rustmaps import Client


async def main() -> None:
    """Run main."""
    client = Client("f808bde9d91244b788ea145eff54497f")

    map_id = input("Enter a map ID: ")
    found_map = await client.get_map(map_id)
    print(found_map)
    await client.http.close()


if __name__ == "__main__":
    asyncio.run(main())

import sys
import asyncio

from infra.http.http_server import start_http_server


async def start() -> None:
    try:
        await asyncio.gather(
            start_http_server(),
        )

        await asyncio.Event().wait()

    except (Exception, asyncio.CancelledError) as error:
        print(f"Error on trying to start server: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass
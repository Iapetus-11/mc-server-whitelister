import asyncio
from bot.whitelister import Whitelister


async def main():
    bot = Whitelister()

    async with bot:
        await bot.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

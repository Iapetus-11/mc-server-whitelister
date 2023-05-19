import io
from typing import Any
from urllib.parse import quote as urlquote

import aiohttp
import aiomcrcon
import discord

from bot import settings


def text_to_discord_file(text: str, *, file_name: str | None = None) -> discord.File:
    file_data = io.BytesIO(text.encode(encoding="utf8"))
    file_data.seek(0)

    return discord.File(file_data, filename=file_name)


def get_rcon_client() -> aiomcrcon.Client:
    return aiomcrcon.Client(
        settings.RCON_HOST,
        settings.RCON_PORT,
        settings.RCON_PASSWORD,
    )


def xuid_to_uuid(xuid: str) -> str:
    return f'{"0" * 8}-{"0000-" * 3}{hex(int(xuid)).strip("0x")}'

import asyncio
import json

import discord
from discord import app_commands
from discord.ext import commands

from bot import settings
from bot.utils.ftp import SFTPClient
from bot.utils.misc import search_xbl_users, get_rcon_client, xuid_to_uuid
from bot.whitelister import Whitelister


class WhitelistCommands(commands.Cog):
    def __init__(self, bot: Whitelister):
        self.bot = bot

        self.ftp_whitelist_lock = asyncio.Lock()

    async def check_permissions(self, inter: discord.Interaction) -> bool:
        if inter.user.id not in settings.DISCORD_ALLOWED_USER:
            embed = self.bot.default_embed()

            embed.title = 'Permission Denied'
            embed.description = 'Imagine thinking you have the permissions to execute this command'

            await inter.response.send_message(embed=embed)

            return False

        return True

    @app_commands.command(
        name="whitelist_add",
        description="Whitelist a Java Edition player on the server",
    )
    async def whitelist_add(self, inter: discord.Interaction, username: str):
        if not await self.check_permissions(inter):
            return

        await inter.response.defer()

        async with get_rcon_client() as rcon_client:
            await rcon_client.send_cmd(f'whitelist add {username}')

        embed = self.bot.default_embed()
        embed.title = f'Successfully whitelisted user `{username}`'

        await inter.edit_original_response(embed=embed)

    @app_commands.command(
        name="whitelist_remove",
        description="Remove a Java Edition player from the server's whitelist",
    )
    async def whitelist_remove(self, inter: discord.Interaction, username: str):
        if not await self.check_permissions(inter):
            return

        await inter.response.defer()

        async with get_rcon_client() as rcon_client:
            await rcon_client.send_cmd(f'whitelist remove {username}')

        embed = self.bot.default_embed()
        embed.title = f'Successfully removed user `{username}` from the whitelist'

        await inter.edit_original_response(embed=embed)

    @app_commands.command(
        name='whitelistbe_add',
        description="Whitelist a Bedrock Edition player on the server",
    )
    async def whitelistbe_add(self, inter: discord.Interaction, username: str):
        if not await self.check_permissions(inter):
            return

        await inter.response.defer()

        user_info = await search_xbl_users(username)

        if user_info is None:
            await inter.edit_original_response(content='No user exists with that gamertag.')
            return

        async with SFTPClient() as ftp_client, self.ftp_whitelist_lock:
            whitelist = json.loads(await ftp_client.read_file('whitelist.json'))

            whitelist.append({'uuid': xuid_to_uuid(user_info['xuid']), 'name': username})

            await ftp_client.write_file('whitelist.json', json.dumps(whitelist).encode())

        async with get_rcon_client() as rcon_client:
            await rcon_client.send_cmd('whitelist reload')

        embed = self.bot.default_embed()
        embed.title = f'Successfully whitelisted user `{username}`'

        await inter.edit_original_response(embed=embed)

    @app_commands.command(
        name="whitelistbe_remove",
        description="Remove a Java Edition player from the server's whitelist",
    )
    async def whitelistbe_remove(self, inter: discord.Interaction, username: str):
        if not await self.check_permissions(inter):
            return

        await inter.response.defer()

        user_info = await search_xbl_users(username)

        if user_info is None:
            await inter.edit_original_response(content='No user exists with that gamertag.')
            return

        user_xuid = xuid_to_uuid(user_info['xuid'])

        async with SFTPClient() as ftp_client, self.ftp_whitelist_lock:
            whitelist = json.loads(await ftp_client.read_file('whitelist.json'))

            whitelist = [player for player in whitelist if player['uuid'] != user_xuid]

            await ftp_client.write_file('whitelist.json', json.dumps(whitelist).encode())

        async with get_rcon_client() as rcon_client:
            await rcon_client.send_cmd('whitelist reload')

        embed = self.bot.default_embed()
        embed.title = f'Successfully removed user `{username}` from the whitelist'

        await inter.edit_original_response(embed=embed)

async def setup(bot: Whitelister):
    await bot.add_cog(WhitelistCommands(bot))

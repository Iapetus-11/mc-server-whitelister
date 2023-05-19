import arrow
import discord
from discord.ext import commands

from bot.utils.setup import setup_logging
from bot import settings


class Whitelister(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default(),
            command_prefix=commands.when_mentioned,
            help_command=None,
        )

        self.logger = setup_logging()

        self.cog_list = [
            "core.events",
            "commands.whitelist",
        ]

    # noinspection PyMethodOverriding
    async def start(self) -> None:
        # load all the cogs
        for cog in self.cog_list:
            await self.load_extension(f"bot.cogs.{cog}")

        await super().start(settings.DISCORD_BOT_TOKEN)

    async def on_ready(self) -> None:
        self.logger.info("Syncing slash commands...")
        self.tree.copy_global_to(guild=self.get_guild(settings.DISCORD_GUILD))
        await self.tree.sync()
        self.logger.info("Synced slash commands!")

    async def get_logging_channel(self) -> discord.TextChannel:
        channel = self.get_channel(settings.DISCORD_LOGGING_CHANNEL)

        if channel is None:
            await self.wait_until_ready()
            channel = await self.fetch_channel(settings.DISCORD_LOGGING_CHANNEL)

        return channel

    def default_embed(self) -> discord.Embed:
        embed = discord.Embed(color=discord.Color.green())

        embed.timestamp = arrow.utcnow().datetime

        # embed.set_footer(text="Bedrock Whitelister", icon_url=self.user.avatar.url)

        return embed

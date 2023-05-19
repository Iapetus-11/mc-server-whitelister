import time
import traceback

import discord
from discord.ext import commands

from bot.utils.code import format_exception
from bot.whitelister import Whitelister
from bot.utils.misc import text_to_discord_file


class Events(commands.Cog):
    def __init__(self, bot: Whitelister):
        self.bot = bot

        # Register event listeners
        bot.event(self.on_event_error)
        bot.tree.on_error = self.on_slash_command_error

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info("Bot is connected and ready!")

    async def on_event_error(
        self, event, *args, **kwargs
    ):
        # logs errors in events, such as on_message
        event_args_repr = list(map(repr, args)) + [f'{k}={repr(v)}' for k, v in kwargs.items()]
        event_call_repr = f"{event}({',  '.join(event_args_repr)})"

        self.bot.logger.error(
            f"An exception occurred in this event call:\n{event_call_repr}", exc_info=True
        )

        await self.bot.wait_until_ready()

        logging_channel = await self.bot.get_logging_channel()
        await logging_channel.send(
            f"```py\n{event_call_repr[:1920]}```",
            file=text_to_discord_file(
                traceback.format_exc(),
                file_name=f"error_tb_ev_{time.time():0.0f}.txt",
            ),
        )

    async def on_slash_command_error(self, inter: discord.Interaction, error: Exception):
        self.bot.logger.error(
            f"An exception occurred in the /{inter.command} command", exc_info=True
        )

        cmd_call_repr = (
            f"```\n{inter.user} (user_id={inter.user.id}) "
            f"(guild_id={inter.guild_id}): {inter.data}```"
        )

        logging_channel = await self.bot.get_logging_channel()
        await logging_channel.send(
            cmd_call_repr,
            file=text_to_discord_file(
                format_exception(error),
                file_name=f"error_tb_cmd_{time.time():0.0f}.txt",
            ),
        )


async def setup(bot: Whitelister):
    await bot.add_cog(Events(bot))

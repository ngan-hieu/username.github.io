from discord.ext import commands
from discord import app_commands
import discord


class Say(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="say",
        description="Bot nói hộ"
    )
    async def say(
        self,
        interaction: discord.Interaction,
        text: str
    ):
        await interaction.response.send_message(text)


async def setup(bot):
    await bot.add_cog(Say(bot))
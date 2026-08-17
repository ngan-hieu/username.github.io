from discord.ext import commands
from discord import app_commands
import discord


class Hello(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="hello",
        description="Chào người dùng"
    )
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Xin chào {interaction.user.mention}!"
        )


async def setup(bot):
    await bot.add_cog(Hello(bot))
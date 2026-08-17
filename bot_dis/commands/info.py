from discord.ext import commands
from discord import app_commands
import discord


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="info",
        description="Thông tin bot"
    )
    async def info(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="Thông tin Bot",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Tên",
            value=self.bot.user.name,
            inline=False
        )

        embed.add_field(
            name="Ping",
            value=f"{round(self.bot.latency*1000)} ms",
            inline=False
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
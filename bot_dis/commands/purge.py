from discord.ext import commands
from discord import app_commands
import discord

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="purge",
        description="Xóa nhiều tin nhắn"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1, 100]
    ):
        await interaction.response.defer(ephemeral=True)

        deleted = await interaction.channel.purge(limit=amount)

        await interaction.followup.send(
            f"🗑️ Đã xóa {len(deleted)} tin nhắn.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Purge(bot))
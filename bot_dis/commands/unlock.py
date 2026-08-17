from discord.ext import commands
from discord import app_commands
import discord

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="unlock",
        description="Mở khóa kênh hiện tại"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(
            interaction.guild.default_role
        )
        overwrite.send_messages = None

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            overwrite=overwrite
        )

        await interaction.response.send_message("🔓 Đã mở khóa kênh.")

async def setup(bot):
    await bot.add_cog(Unlock(bot))
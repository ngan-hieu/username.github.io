from discord.ext import commands
from discord import app_commands
import discord

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="lock",
        description="Khóa kênh hiện tại"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(
            interaction.guild.default_role
        )
        overwrite.send_messages = False

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            overwrite=overwrite
        )

        await interaction.response.send_message("🔒 Đã khóa kênh.")

async def setup(bot):
    await bot.add_cog(Lock(bot))
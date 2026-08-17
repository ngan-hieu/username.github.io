from discord.ext import commands
from discord import app_commands
import discord

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="leave",
        description="Bot rời voice"
    )
    async def leave(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client

        if vc is None:
            await interaction.response.send_message(
                "Bot không ở voice.",
                ephemeral=True
            )
            return

        await vc.disconnect()
        await interaction.response.send_message("👋 Đã rời voice.")

async def setup(bot):
    await bot.add_cog(Leave(bot))
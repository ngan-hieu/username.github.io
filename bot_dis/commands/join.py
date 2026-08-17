from discord.ext import commands
from discord import app_commands
import discord

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="join",
        description="Bot vào voice"
    )
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message(
                "Bạn chưa ở voice.",
                ephemeral=True
            )
            return

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()

        await interaction.response.send_message(
            f"🎤 Đã vào {channel.mention}"
        )

async def setup(bot):
    await bot.add_cog(Join(bot))
from discord.ext import commands
from discord import app_commands
import discord
import asyncio

class VoiceIdle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = False

    @app_commands.command(
        name="voiceidle",
        description="Bật/tắt tự rời voice khi không còn người"
    )
    async def voiceidle(self, interaction: discord.Interaction):
        self.enabled = not self.enabled

        await interaction.response.send_message(
            f"🎧 Voice Idle: {'Bật' if self.enabled else 'Tắt'}"
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not self.enabled:
            return

        vc = member.guild.voice_client

        if vc is None or not vc.is_connected():
            return

        humans = [m for m in vc.channel.members if not m.bot]

        if len(humans) == 0:
            await asyncio.sleep(30)

            if not vc.is_connected():
                return

            humans = [m for m in vc.channel.members if not m.bot]

            if len(humans) == 0:
                await vc.disconnect()

async def setup(bot):
    await bot.add_cog(VoiceIdle(bot))
from discord.ext import commands
from discord import app_commands
import discord

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="kick",
        description="Kick một thành viên khỏi server"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "Không có lý do"
    ):
        if member == interaction.user:
            await interaction.response.send_message(
                "Bạn không thể tự kick chính mình.",
                ephemeral=True
            )
            return

        try:
            await member.kick(reason=f"{interaction.user}: {reason}")
            await interaction.response.send_message(
                f"✅ Đã kick {member.mention}\nLý do: {reason}"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Bot không đủ quyền để kick thành viên này.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Kick(bot))
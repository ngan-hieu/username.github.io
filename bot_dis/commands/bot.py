from discord.ext import commands
from discord import app_commands
import discord

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ban",
        description="Ban một thành viên"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "Không có lý do"
    ):
        if member == interaction.user:
            await interaction.response.send_message(
                "Bạn không thể tự ban chính mình.",
                ephemeral=True
            )
            return

        try:
            await member.ban(reason=f"{interaction.user}: {reason}")
            await interaction.response.send_message(
                f"🔨 Đã ban {member.mention}\nLý do: {reason}"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Bot không đủ quyền để ban thành viên này.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Ban(bot))
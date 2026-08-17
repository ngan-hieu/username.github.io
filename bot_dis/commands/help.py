import discord
from discord import app_commands
from discord.ext import commands


class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help", description="Hiển thị tất cả lệnh hiện có của bot"
    )
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Danh sách lệnh của Bot", color=discord.Color.blue()
        )

        # Lấy toàn bộ danh sách slash command đã đăng ký trong bot tree
        slash_commands = self.bot.tree.get_commands()

        if not slash_commands:
            embed.description = "Hiện chưa có lệnh nào được đăng ký."
        else:
            for cmd in slash_commands:
                # Tên lệnh kèm dấu / và mô tả của lệnh
                name = f"/{cmd.name}"
                description = cmd.description or "Không có mô tả"
                embed.add_field(name=name, value=description, inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))

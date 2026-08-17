from discord.ext import commands
from discord import app_commands
import discord


class Dem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="dem",
        description="Đếm từ 1 đến số chỉ định."
    )
    @app_commands.describe(
        so="Số cần đếm đến",
        chu="Chuỗi thêm sau mỗi số"
    )
    async def dem(
        self,
        interaction: discord.Interaction,
        so: app_commands.Range[int, 1, 1000],
        chu: str
    ):
        # Tạo nội dung: 1hello, 2hello, 3hello...
        lines = [f"{i}{chu}" for i in range(1, so + 1)]

        # Nếu vừa 1 tin nhắn
        if len("\n".join(lines)) <= 2000:
            await interaction.response.send_message("\n".join(lines))
            return

        # Nếu quá 2000 ký tự thì chia nhiều tin nhắn
        await interaction.response.defer()

        message = ""

        for line in lines:
            if len(message) + len(line) + 1 > 2000:
                await interaction.followup.send(message)
                message = line
            else:
                if message:
                    message += "\n"
                message += line

        if message:
            await interaction.followup.send(message)


async def setup(bot):
    await bot.add_cog(Dem(bot))
import discord
from discord import app_commands
from discord.ext import commands


class SnipeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sniped_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        self.sniped_messages[message.channel.id] = message

    @app_commands.command(
        name="thuhoianh", description="Xem lại tin nhắn, ảnh, video vừa bị thu hồi/xóa gần nhất"
    )
    async def thuhoianh(self, interaction: discord.Interaction):
        message = self.sniped_messages.get(interaction.channel_id)

        if not message:
            await interaction.response.send_message(
                "❌ Không có tin nhắn nào vừa bị xóa trong kênh này."
            )
            return

        embed = discord.Embed(
            title="Xem lại tin nhắn vừa bị thu hồi/xóa gần nhất",
            color=discord.Color.red(),
            timestamp=message.created_at,
        )
        embed.add_field(name="User", value=message.author.mention, inline=True)
        embed.add_field(name="Kênh", value=message.channel.mention, inline=True)

        content_value = message.content if message.content else "*Không có nội dung chữ*"
        embed.add_field(name="Nội dung", value=content_value, inline=False)

        if message.attachments:
            first_attachment = message.attachments[0]
            if first_attachment.content_type and first_attachment.content_type.startswith("image/"):
                embed.set_image(url=first_attachment.url)

            links = [f"[{att.filename}]({att.url})" for att in message.attachments]
            embed.add_field(
                name="Tệp đính kèm (Ảnh/Video/File)",
                value="\n".join(links),
                inline=False
            )

        embed.set_footer(text=f"ID Người dùng: {message.author.id}")
        await interaction.response.send_message(embed=embed)


# HÀM BẮT BUỘC ĐỂ DISCORD.PY KHÔNG BÁO LỖI MISSING SETUP
async def setup(bot):
    await bot.add_cog(SnipeCog(bot))
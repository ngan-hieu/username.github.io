import discord
from discord import app_commands
from discord.ext import commands


class SnipeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # Lưu danh sách tin nhắn bị xóa theo channel_id: {channel_id: [message1, message2, ...]}
        self.sniped_messages = {}
        # Giới hạn số lượng tin nhắn lưu lại tối đa trong mỗi kênh để tránh ngốn RAM
        self.max_history = 10

    # 1. Tự động lưu tin nhắn vừa bị gỡ/xóa vào danh sách
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return

        channel_id = message.channel.id
        if channel_id not in self.sniped_messages:
            self.sniped_messages[channel_id] = []

        # Thêm tin nhắn mới vào đầu danh sách (tin nhắn mới nhất nằm ở chỉ số 0)
        self.sniped_messages[channel_id].insert(0, message)

        # Giữ số lượng tin nhắn không vượt quá max_history
        if len(self.sniped_messages[channel_id]) > self.max_history:
            self.sniped_messages[channel_id].pop()

    # 2. Slash Command: /thuhoi - Hiển thị danh sách các tin nhắn đã thu hồi
    @app_commands.command(
        name="thuhoi", description="Xem danh sách các tin nhắn đã bị thu hồi/xóa gần đây"
    )
    async def thuhoi(self, interaction: discord.Interaction):
        messages = self.sniped_messages.get(interaction.channel_id, [])

        if not messages:
            await interaction.response.send_message(
                "❌ Không có tin nhắn nào bị xóa gần đây trong kênh này.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📜 Danh sách tin nhắn bị thu hồi gần nhất",
            color=discord.Color.red(),
            description=f"Hiển thị {len(messages)} tin nhắn đã bị xóa gần nhất:"
        )

        for i, msg in enumerate(messages, 1):
            content = msg.content if msg.content else "*(Hình ảnh / Đính kèm / Sticker)*"
            # Giới hạn độ dài nội dung để tránh vượt giới hạn ký tự Embed
            if len(content) > 200:
                content = content[:200] + "..."

            time_str = msg.created_at.strftime("%H:%M:%S - %d/%m/%Y")

            embed.add_field(
                name=f"#{i} | {msg.author.display_name} (`{msg.author.id}`)",
                value=f"**Nội dung:** {content}\n**Gửi lúc:** {time_str}",
                inline=False
            )

        embed.set_footer(text=f"Xem Bởi {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SnipeCog(bot))
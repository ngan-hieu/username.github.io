import asyncio
import logging
import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("bot")

# ID người dùng được phép
ALLOWED_USERS = {1502266917677957240, 1209809514912550914, 1519266947051688058}

# Tên các Role được phép sử dụng lệnh
ALLOWED_ROLE_NAMES = {
    "ADMIN👑🤴"
}


def is_allowed():
    """Hàm kiểm tra người dùng có nằm trong ALLOWED_USERS hoặc sở hữu Role hợp lệ không"""
    async def predicate(interaction: discord.Interaction) -> bool:
        # 1. Kiểm tra ID người dùng
        if interaction.user.id in ALLOWED_USERS:
            return True

        # 2. Kiểm tra Tên Role của người dùng trong Server
        if isinstance(interaction.user, discord.Member):
            user_role_names = {role.name for role in interaction.user.roles}
            if any(role_name in ALLOWED_ROLE_NAMES for role_name in user_role_names):
                return True

        # Gửi thông báo công khai trong kênh (đã bỏ ephemeral=True)
        await interaction.response.send_message(
            "❌ Mày Đéo Có Role Vip Để Dùng(Thằng Hoặc Con) Ngu Như Chó Đẻ"
       )
        return False

    return app_commands.check(predicate)


class Spam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.active_spams = {}

    async def send_dm_loop(
        self, user: discord.User, content: str, tag: bool, interval: float
    ):
        message_content = f"{user.mention} {content}" if tag else content
        logger.info(f"Bắt đầu spam DM cho {user} (ID: {user.id}) mỗi {interval}s")

        while True:
            try:
                await user.send(message_content)
                logger.info(f"Đã gửi DM thành công cho {user.name}")
                await asyncio.sleep(interval)
            except discord.Forbidden:
                logger.warning(
                    f"Không thể gửi DM cho {user} (ID: {user.id}) - Bot bị chặn hoặc người dùng đóng DM."
                )
                break
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = getattr(e, "retry_after", 5.0)
                    logger.warning(
                        f"Bị giới hạn tốc độ (Rate Limit). Thử lại sau {retry_after}s."
                    )
                    await asyncio.sleep(retry_after)
                else:
                    logger.error(f"Lỗi HTTPException khi gửi DM cho {user}: {e}")
                    await asyncio.sleep(interval)
            except asyncio.CancelledError:
                logger.info(f"Task spam cho {user} (ID: {user.id}) đã bị hủy.")
                raise
            except Exception as e:
                logger.error(f"Lỗi không xác định khi gửi DM cho {user}: {e}")
                break

        if user.id in self.active_spams:
            del self.active_spams[user.id]

    @app_commands.command(
        name="spamchat",
        description="Tự động gửi tin nhắn DM lặp lại cho một người dùng"
    )
    @app_commands.describe(
        nguoi_nhan="Người nhận tin nhắn",
        noi_dung="Nội dung tin nhắn cần gửi",
        tag="Có tag người nhận trong DM không (True/False)",
        thoi_gian="Khoảng cách thời gian giữa mỗi lần gửi, tối thiểu 0.001 giây"
    )
    @is_allowed()
    async def dm(
        self,
        interaction: discord.Interaction,
        nguoi_nhan: discord.User,
        noi_dung: str,
        tag: bool,
        thoi_gian: float,
    ):
        if thoi_gian < 0.001:
            await interaction.response.send_message(
                "❌ Tối Đa Là 0.01s",
                ephemeral=True,
            )
            return

        user_id = nguoi_nhan.id

        if user_id in self.active_spams:
            self.active_spams[user_id].cancel()
            logger.info(
                f"Đã Dừng Spam Chat  {nguoi_nhan} (ID: {user_id})"
            )

        task = asyncio.create_task(
            self.send_dm_loop(nguoi_nhan, noi_dung, tag, thoi_gian)
        )
        self.active_spams[user_id] = task

        await interaction.response.send_message(
            f"✅ Auto Spam Chat Cho {nguoi_nhan.mention} mỗi {thoi_gian}s."
        )

    @app_commands.command(
        name="dungspam",
        description="Dừng gửi tin nhắn lặp lại và xóa toàn bộ tin nhắn bot đã gửi trong DM"
    )
    @app_commands.describe(
        nguoi_nhan="Người nhận cần dừng gửi và dọn dẹp tin nhắn"
    )
    @is_allowed()
    async def dm_stop(
        self, interaction: discord.Interaction, nguoi_nhan: discord.User
    ):
        await interaction.response.defer(ephemeral=False)

        user_id = nguoi_nhan.id
        stopped_spam = False

        if user_id in self.active_spams:
            self.active_spams[user_id].cancel()
            del self.active_spams[user_id]
            logger.info(f"Đã Dừng Spam Chat Cho {nguoi_nhan}")
            stopped_spam = True

        deleted_count = 0
        try:
            dm_channel = nguoi_nhan.dm_channel
            if dm_channel is None:
                dm_channel = await nguoi_nhan.create_dm()

            async for message in dm_channel.history(limit=100):
                if message.author == self.bot.user:
                    try:
                        await message.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.2)
                    except discord.HTTPException as e:
                        logger.error(f"Không thể xóa tin nhắn {message.id}: {e}")
        except Exception as e:
            logger.error(f"Lỗi khi dọn dẹp tin nhắn DM cho {nguoi_nhan}: {e}")

        status_msg = (
            f"🛑 Xóa Tin Nhắn Spam Chat cho {nguoi_nhan.mention}."
            if stopped_spam
            else f"Dọn dẹp Tin Nhắn Đã Spam cho {nguoi_nhan.mention}."
        )
        if deleted_count > 0:
            await interaction.followup.send(
                f"{status_msg} Đã xóa thành công **{deleted_count}**"
            )
        else:
            await interaction.followup.send(
                f"{status_msg} Không Có Spam Chat Nào đã Spam."
            )


async def setup(bot):
    await bot.add_cog(Spam(bot))
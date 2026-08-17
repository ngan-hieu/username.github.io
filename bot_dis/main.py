import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("bot")

TOKEN = os.getenv("TOKEN")


class MyBot(commands.Bot):
    def __init__(self):
        # Bật intents để đọc nội dung tin nhắn
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        # Tải toàn bộ cogs từ thư mục commands
        for file in os.listdir("./commands"):
            if file.endswith(".py"):
                try:
                    await self.load_extension(f"commands.{file[:-3]}")
                    print(f"Đã load thành công {file}")
                except Exception as e:
                    print(f"Lỗi khi load {file}: {e}")


bot = MyBot()


@bot.event
async def on_ready():
    logger.info(f"Đăng nhập thành công với tên: {bot.user} (ID: {bot.user.id})")
    logger.info("Bắt đầu tự động đồng bộ lệnh đến toàn bộ server...")
    
    for guild in bot.guilds:
        try:
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            logger.info(f"✅ Đã đồng bộ lệnh thành công cho server: {guild.name} (ID: {guild.id})")
        except Exception as e:
            logger.error(f"❌ Không thể đồng bộ lệnh cho server {guild.name} (ID: {guild.id}): {e}")
            
    logger.info("Hoàn tất đồng bộ tất cả server!")


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    logger.exception(error)

    if interaction.response.is_done():
        await interaction.followup.send("❌ Có lỗi xảy ra.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Có lỗi xảy ra.", ephemeral=True)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    logger.info(
        f"[MESSAGE] "
        f"{message.author} | "
        f"{message.guild.name if message.guild else 'DM'} | "
        f"#{message.channel} | "
        f"{message.content}"
    )


# Bắt sự kiện người dùng thu hồi/xóa tin nhắn
@bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot:
        return

    content = message.content if message.content else "<Tin nhắn không có văn bản (chỉ có ảnh/file/embed)>"
    
    logger.info(
        f"[THU HỒI / XÓA TIN NHẮN] "
        f"Tác giả: {message.author} | "
        f"Server: {message.guild.name if message.guild else 'DM'} | "
        f"Kênh: #{message.channel} | "
        f"Nội dung bị xóa: {content}"
    )


async def main():
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
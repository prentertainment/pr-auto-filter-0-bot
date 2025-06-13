import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import Config
from database.db import Database
from Script import script
from utils import get_size

# লগিং সেটআপ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Client(
    "auto-filter-bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

db = Database()

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        text=script.START_TXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("সাপোর্ট", url="https://t.me/vj_bots")]
        ]),
        disable_web_page_preview=True
    )

@app.on_message(filters.command("help"))
async def help(client, message: Message):
    await message.reply_text(
        text=script.HELP_TXT,
        disable_web_page_preview=True
    )

@app.on_message(filters.command("about"))
async def about(client, message: Message):
    await message.reply_text(
        text=script.ABOUT_TXT,
        disable_web_page_preview=True
    )

@app.on_message(filters.command("search"))
async def search_files(client, message: Message):
    query = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if not query:
        return await message.reply("সার্চ টার্ম দিন। উদাহরণ: `/search Titanic`")
    
    files = await db.get_search_results(query)
    if not files:
        return await message.reply("😢 কোনো ফলাফল পাওয়া যায়নি!")
    
    await message.reply(f"🔍 {len(files)} টি ফলাফল পাওয়া গেছে:")
    
    for file in files[:10]:  # সর্বোচ্চ ১০টি ফলাফল দেখাও
        caption = file.get("caption", file["file_name"])
        await message.reply_text(
            f"📁 ফাইল: {file['file_name']}\n"
            f"ℹ️ বিস্তারিত: {caption[:50]}...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ডাউনলোড", callback_data=f"dl_{file['file_id']}")]
            ])
        )

@app.on_callback_query(filters.regex(r"^dl_"))
async def send_file(client, callback_query):
    file_id = callback_query.data.split("_", 1)[1]
    file_data = await db.get_file(file_id)
    
    if not file_data:
        return await callback_query.answer("ফাইলটি পাওয়া যায়নি", show_alert=True)
    
    await callback_query.message.reply_document(
        document=file_id,
        caption=f"📥 {file_data['file_name']}"
    )
    await callback_query.answer()

if __name__ == "__main__":
    logger.info("বট চালু হচ্ছে...")
    app.run()

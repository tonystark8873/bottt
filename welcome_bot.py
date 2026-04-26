import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import os

# Bot Token - Environment variable se lega ya seedha likho
BOT_TOKEN = os.environ.get("8772470673:AAFn2Wu-IkN4RjXWVYwqlQJfHIX-qHfUD8A", "8772470673:AAFn2Wu-IkN4RjXWVYwqlQJfHIX-qHfUD8A")

# Flask app
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Setty Brother Welcome Bot chal raha hai!"

# /start command handler - test ke liye
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot chal raha hai!\n\n"
        "Main group mein naye members ko welcome karta hun."
    )

# Welcome message jab koi join kare
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        for member in update.message.new_chat_members:
            if member.is_bot:
                continue

            name = member.first_name
            user_id = member.id
            username = f"@{member.username}" if member.username else "username nahi hai"

            message = (
                f"🎉 *Welcome to Setty Brother, {name}!*\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📚 *UPSC Classes — Premium Content*\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
                f"✅ *Verify karne ke liye yeh details use karo:*\n\n"
                f"🆔 *Tumhara Numeric User ID:*\n"
                f"`{user_id}`\n\n"
                f"👤 *Tumhara Username:* {username}\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🔐 *Verify kaise karein?*\n"
                f"1️⃣ Website kholo\n"
                f"2️⃣ Apna User ID `{user_id}` daalo\n"
                f"3️⃣ Verify dabao — Access milega! 🚀\n\n"
                f"❓ *Koi problem?* @Udaysetty se contact karo"
            )

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode="Markdown"
            )
            print(f"✅ Welcome message bheja: {name} ({user_id})")
    except Exception as e:
        print(f"❌ Error: {e}")

async def run_bot():
    bot_app = Application.builder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    print("✅ Bot polling shuru...")
    async with bot_app:
        await bot_app.start()
        await bot_app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await asyncio.Event().wait()

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    flask_app.run(host="0.0.0.0", port=10000)

import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ✅ Apna Bot Token yahan daalo
BOT_TOKEN = "APNA_BOT_TOKEN_YAHAN_DAALO"

# Flask app — Render ke liye
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Setty Brother Welcome Bot chal raha hai!"

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

def run_bot():
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    bot_app = Application.builder().token(BOT_TOKEN).build()
    bot_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    print("✅ Bot chal raha hai...")
    bot_app.run_polling()

if __name__ == "__main__":
    # Bot alag thread mein chalao
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Flask web server chalao
    app.run(host="0.0.0.0", port=10000)

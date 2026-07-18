from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import yt_dlp

TOKEN = "8764326925:AAGb4XVheYqu47TmPqHAT5ebqcLEEMjnDpg"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🎵 Qo'shiq qidirish"],
        ["🖼️ Rasm"],
        ["ℹ️ Yordam"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    context.user_data["music_search"] = False

    await update.message.reply_text(
        "Assalomu alaykum!\nKerakli bo'limni tanlang.",
        reply_markup=reply_markup
    )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🎵 Qo'shiq qidirish":
        context.user_data["music_search"] = True
        await update.message.reply_text(
            "🎵 Qo'shiq nomini yuboring."
        )

    elif context.user_data.get("music_search"):

        await update.message.reply_text("🔍 YouTube'dan qidirilmoqda...")

        try:
            ydl_opts = {
                "quiet": True,
                "default_search": "ytsearch1"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=False)

            video = info["entries"][0]

            await update.message.reply_text(
                f"✅ Topildi!\n\n"
                f"🎵 {video['title']}\n\n"
                f"🔗 {video['webpage_url']}"
            )

        except Exception:
            await update.message.reply_text(
                "❌ Qo'shiq topilmadi."
            )

        context.user_data["music_search"] = False

    elif text == "🖼️ Rasm":
        await update.message.reply_text(
            "🖼️ Rasm funksiyasi hali tayyor emas."
        )

    elif text == "ℹ️ Yordam":
        await update.message.reply_text(
            "Qo'shiq nomini yoki YouTube/Instagram linkini yuboring."
        )

    else:
        await update.message.reply_text(
            "Noma'lum buyruq."
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

from flask import Flask
from threading import Thread

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot ishlayapti!"

def run_web():
    web_app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

print("Bot ishga tushdi...")
app.run_polling()

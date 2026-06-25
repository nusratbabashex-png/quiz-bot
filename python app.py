import os
import logging
import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سڵاو 👋\n"
        "پرسیار یان وێنە بنێرە بۆ گۆڕینی بۆ Quiz."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        await update.message.reply_text("⏳ Processing...")

        prompt = f"""
Convert this into a multiple-choice quiz.

{text}

Format:
Question:
A)
B)
C)
D)
Correct answer:
"""

        response = model.generate_content(prompt)

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(str(e))


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

print("Bot started...")

app.run_polling()

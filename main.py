import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Taksi chaqirish 🚖")],
        [KeyboardButton("Biz haqimizda ℹ️"), KeyboardButton("Bog'lanish 📞")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Xush kelibsiz! Taksi buyurtma qilish uchun tugmani bosing:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Taksi chaqirish 🚖":
        location_button = KeyboardButton("Joylashuvni yuborish 📍", request_location=True)
        reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("Iltimos, joylashuvingizni yuboring:", reply_markup=reply_markup)
    elif text == "Biz haqimizda ℹ️":
        await update.message.reply_text("Oybek Taxi - tez va xavfsiz xizmat!")
    elif text == "Bog'lanish 📞":
        await update.message.reply_text("Aloqa uchun: +998901234567")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    await update.message.reply_text(
        f"Rahmat! Joylashuvingiz qabul qilindi.\n"
        f"Kenglik: {location.latitude}\n"
        f"Uzunlik: {location.longitude}\n"
        f"Haydovchi tez orada siz bilan bog'lanadi."
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    print("Bot ishga tushdi...")
    app.run_polling(drop_pending_updates=True)


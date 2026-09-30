import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# -------------------------------------------------------------
# ADMIN MA'LUMOTLARI
# Telegram ID'ingizni @userinfobot orqali bilib, shu yerga yozing:
ADMIN_ID = 123456789  
ADMIN_USERNAME = "@Asqarovich2006"
# -------------------------------------------------------------

# Asosiy menyu
main_keyboard = [
    [KeyboardButton("🚖 Taksi chaqirish")],
    [KeyboardButton("ℹ️ Biz haqimizda"), KeyboardButton("📞 Bog'lanish")]
]
markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

# /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🚖 **Oybek Taxi xizmatiga xush kelibsiz!**\n\n"
        "Taksi buyurtma qilish uchun quyidagi tugmani bosing:"
    )
    await update.message.reply_text(welcome_text, reply_markup=markup, parse_mode="Markdown")

# Matnli xabarlar
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚖 Taksi chaqirish":
        # 1-qadam: Joylashuv so'rash
        loc_keyboard = [[KeyboardButton("📍 Joylashuvni yuborish", request_location=True)]]
        loc_markup = ReplyKeyboardMarkup(loc_keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "Iltimos, taksi borishi kerak bo'lgan joylashuvni yuboring:",
            reply_markup=loc_markup
        )

    elif text == "ℹ️ Biz haqimizda":
        about_text = (
            "🚖 **Oybek Taxi**\n\n"
            "24/7 qulay, tezkor va arzon taksi xizmati!\n"
            "Sizning xavfsizligingiz — bizning ustuvor vazifamiz."
        )
        await update.message.reply_text(about_text, reply_markup=markup, parse_mode="Markdown")

    elif text == "📞 Bog'lanish":
        contact_text = f"📞 **Dispetcher:** +998 90 123 45 67\n💬 **Telegram:** {ADMIN_USERNAME}"
        await update.message.reply_text(contact_text, reply_markup=markup, parse_mode="Markdown")

# Joylashuv kelganda
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Joylashuvni saqlaymiz
    context.user_data['latitude'] = update.message.location.latitude
    context.user_data['longitude'] = update.message.location.longitude

    # 2-qadam: Telefon raqam so'rash
    phone_keyboard = [[KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)]]
    phone_markup = ReplyKeyboardMarkup(phone_keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "✅ Joylashuv qabul qilindi!\n\nEndi siz bilan bog'lanishimiz uchun **Telefon raqamni yuborish** tugmasini bosing:",
        reply_markup=phone_markup
    )

# Kontakt kelganda
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_phone = update.message.contact.phone_number
    user_name = update.message.from_user.full_name
    username = f"@{update.message.from_user.username}" if update.message.from_user.username else "Mavjud emas"
    
    lat = context.user_data.get('latitude')
    lon = context.user_data.get('longitude')

    # 1. Mijozga minnatdorchilik bildirish va tasdiqlash
    await update.message.reply_text(
        f"🎉 **Buyurtmangiz uchun rahmat!**\n\n"
        f"Telefon raqamingiz: `{user_phone}`\n\n"
        f"Haydovchi tez orada siz bilan bog'lanadi va belgilangan manzilingizga yetib boradi!",
        reply_markup=markup,
        parse_mode="Markdown"
    )

    # 2. Adminga yangi zakaz haqida xabar yuborish
    admin_message = (
        f"🚨 **Yangi taksi buyurtmasi qabul qilindi!**\n\n"
        f"👤 **Mijoz:** {user_name} ({username})\n"
        f"📞 **Tel:** `{user_phone}`"
    )
    
    try:
        # Adminga matn va geolokatsiyani yuborish
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")
        if lat and lon:
            await context.bot.send_location(chat_id=ADMIN_ID, latitude=lat, longitude=lon)
    except Exception as e:
        logging.error(f"Adminga xabar yuborishda xatolik: {e}")

if __name__ == '__main__':
    # Bot tokeningizni kiriting
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Bot ishga tushdi...")
    app.run_polling()

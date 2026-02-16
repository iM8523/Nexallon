import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ملاحظة: سيتم جلب التوكن من إعدادات السيرفر للحماية
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر البداية للترحيب بالمستخدم"""
    user_name = update.effective_user.first_name
    welcome_msg = (
        f"Welcome {user_name} to Nexallon (NXN) AI Bot! 🚀\n\n"
        "I am your AI Business Assistant. Currently in Beta.\n"
        "Type /info to learn more about our services."
    )
    await update.message.reply_text(welcome_msg)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تقديم معلومات عن المشروع"""
    info_msg = (
        "🌐 Project: Nexallon (NXN)\n"
        "🤖 Service: AI-Driven Business Automation\n"
        "🔗 Network: Solana Blockchain\n\n"
        "Stay tuned for the $NXN Token launch!"
    )
    await update.message.reply_text(info_msg)

if __name__ == '__main__':
    # بناء البوت
    application = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة الأوامر
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    
    application.add_handler(start_handler)
    application.add_handler(info_handler)
    
    print("Nexallon Bot is running...")
    application.run_polling()


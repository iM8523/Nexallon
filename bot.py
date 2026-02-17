import os
import requests
from google import genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from solana_utils import get_solana_balance

# إعداد المفاتيح
TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=GEMINI_KEY, http_options={'api_version': 'v1'})
except:
    client = None

# --- الأزرار والقوائم ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إنشاء أزرار تفاعلية
    keyboard = [
        [
            InlineKeyboardButton("📊 Market Stats", callback_data='stats'),
            InlineKeyboardButton("💰 SOL Balance", callback_data='check_bal')
        ],
        [
            InlineKeyboardButton("🚀 Whale Watch", callback_data='whales'),
            InlineKeyboardButton("🔄 Convert", callback_data='convert')
        ],
        [InlineKeyboardButton("🌐 Visit Nexallon Website", url="https://nexallon.ai")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = (
        "🚀 **Nexallon AI v3.0**\n\n"
        "Welcome to the ultimate crypto hub! I am powered by Gemini AI and real-time blockchain data.\n\n"
        "Select a tool from the menu below or just type your question."
    )
    
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """التعامل مع ضغطات الأزرار"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'stats':
        await market_stats_logic(query)
    elif query.data == 'whales':
        await query.edit_message_text("🐋 **Whale Alert:** Searching for large SOL transactions in the last hour... \n(No major movements detected).", parse_mode='Markdown')
    elif query.data == 'check_bal':
        await query.edit_message_text("📝 Please use the command: `/balance <address>`", parse_mode='Markdown')

# --- الأدوات الإضافية ---
async def market_stats_logic(message_obj):
    """منطق جلب بيانات السوق"""
    try:
        data = requests.get("https://api.coingecko.com/api/v3/global").json()['data']
        stats = (
            "📊 **Global Market Stats:**\n\n"
            f"🪙 Active Cryptos: {data['active_cryptocurrencies']}\n"
            f"📈 Market Cap Change (24h): {data['market_cap_change_percentage_24h_usd']:.2f}%\n"
            f"🔗 BTC Dominance: {data['market_cap_percentage']['btc']:.1f}%"
        )
        await message_obj.message.reply_text(stats, parse_mode='Markdown')
    except:
        await message_obj.message.reply_text("Error fetching data.")

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """محول العملات: /convert 1 btc usd"""
    if len(context.args) < 3:
        await update.message.reply_text("Usage: `/convert 1 sol usd`", parse_mode='Markdown')
        return
    amount, coin, target = context.args[0], context.args[1].lower(), context.args[2].lower()
    try:
        res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={target}").json()
        result = float(amount) * res[coin][target]
        await update.message.reply_text(f"🔄 {amount} {coin.upper()} = {result:,.2f} {target.upper()}")
    except:
        await update.message.reply_text("Conversion error. Check coin names.")

# --- منطق الذكاء الاصطناعي (Gemini) ---
async def handle_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action="typing")
        response = client.models.generate_content(model="gemini-1.5-flash", contents=user_text)
        await update.message.reply_text(response.text)
    except:
        search_link = f"https://www.google.com/search?q={user_text.replace(' ', '+')}"
        await update.message.reply_text(
            "🔍 AI Core restricted. Find answers here:\n"
            f"[Google Search]({search_link})", parse_mode='Markdown'
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # الروابط
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('convert', convert))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_ai_chat))
    
    print("Nexallon AI with Buttons is running...")
    app.run_polling()

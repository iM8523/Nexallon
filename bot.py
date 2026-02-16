import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from solana_utils import get_solana_balance

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        f"Welcome {update.effective_user.first_name} to Nexallon (NXN)!\n"
        "I can now interact with the Solana Blockchain.\n"
        "Use /balance <wallet_address> to check SOL balance."
    )
    await update.message.reply_text(welcome_msg)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a wallet address.")
        return
    
    address = context.args[0]
    result = await get_solana_balance(address)
    
    if result is not None:
        await update.message.reply_text(f"Wallet Balance: {result} SOL")
    else:
        await update.message.reply_text("Invalid wallet address or network error.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('balance', balance))
    
    application.run_polling()
    

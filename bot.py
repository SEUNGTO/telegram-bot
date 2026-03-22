import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 로그 설정
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Koyeb에서 작동 중인 봇입니다!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"전달받은 메시지: {update.message.text}")

if __name__ == '__main__':
    # 환경 변수에서 토큰을 가져옵니다 (보안 유지)
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("에러: TELEGRAM_BOT_TOKEN 환경 변수가 설정되지 않았습니다.")
        exit(1)

    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    application.run_polling()


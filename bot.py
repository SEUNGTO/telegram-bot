import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. 환경 변수 읽기 (Koyeb 설정 창에서 넣어줄 값들)
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

app = FastAPI()
# 봇 객체 생성 (실행 X, 초기화만)
tg_app = ApplicationBuilder().token(TOKEN).build()

# 2. 봇 명령어 핸들러 (어제와 동일)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("웹훅으로 다시 태어난 봇입니다! 🚀")

tg_app.add_handler(CommandHandler("start", start))

# 3. 텔레그램 서버가 호출할 'Webhook' 경로
@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    
    # 봇 로직 처리 (비동기)
    async with tg_app:
        await tg_app.process_update(update)
    return {"status": "ok"}

# 4. 앱 시작 시 텔레그램에 "내 주소는 여기야!"라고 알림 (웹훅 등록)
@app.on_event("startup")
async def on_startup():
    await tg_app.initialize()
    # 주의: WEBHOOK_URL 끝에 /webhook 경로를 붙여서 등록합니다.
    await tg_app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    print(f"웹훅이 등록되었습니다: {WEBHOOK_URL}/webhook")

@app.get("/")
def health_check():
    return "Bot is alive!"
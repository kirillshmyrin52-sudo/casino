import os, random, logging, asyncio, sqlite3, time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

BOT_TOKEN = "8249134835:AAHCRCY9FUJIRFtf5nG_xC6MH7_RooMUW7U"
DB_FILE = "casino_ultimate.db"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db_lock = asyncio.Lock()
ROULETTE_NUMBERS = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 500)')
    conn.commit()
    conn.close()
init_db()

@app.get("/api/user/{user_id}")
async def get_profile(user_id: int):
    async with db_lock:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        res = c.fetchone()
        if not res:
            c.execute("INSERT INTO users(user_id) VALUES(?)", (user_id,))
            conn.commit()
            res = (500,)
        conn.close()
    return {"balance": res[0]}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Играть в Казино", web_app_url=WebAppInfo(url="https://vercel.app"))]
    ])
    await message.reply("🎰 **Добро пожаловать в VIP Звёздное Казино!**\n\nБэкенд успешно запущен и защищён базами данных SQL!", reply_markup=kb)

async def main_bot_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main_bot_polling())
  

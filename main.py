import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token="")
dp = Dispatcher()

memes = [
    {"id": 1, "title": "Meme 1", "image_url": "https://example.com/meme1.jpg"},
    {"id": 2, "title": "Meme 2", "image_url": "https://example.com/meme2.jpg"},
    {"id": 3, "title": "Meme 3", "image_url": "https://example.com/meme3.jpg"},
]

@dp.message(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот с мемами. Нажмите /mem для получения мема!")

@dp.message(commands=['mem'])
async def send_meme(message: types.Message):
    meme = random.choice(memes)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("👍", callback_data=f"like_{meme['id']}"))
    keyboard.add(InlineKeyboardButton("👎", callback_data=f"dislike_{meme['id']}"))

    await bot.send_photo(message.chat.id, photo=meme['image_url'], caption=meme['title'], reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('like_') or callback_query.data.startswith('dislike_'))
async def rate_meme(callback_query: types.CallbackQuery):
    await callback_query.answer("Спасибо за вашу оценку!")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(dp.start_polling())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()

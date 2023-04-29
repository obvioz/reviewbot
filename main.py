import logging
from aiogram import Bot, Dispatcher, executor, types, filters

from config import API

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot)
REVIEWERS = []

WELCOME_MESSAGE = """Здравствуйте, вас приветствует бот из Атлашево!
Будем рады вашему отзыву о нашей продукции!
Для этого нужно нажать кнопку *Оставить отзыв*"""

BUTTON1_TEXT = "🐄Оставить отзыв"


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    kb = [
        [types.KeyboardButton(text=BUTTON1_TEXT)],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(WELCOME_MESSAGE, parse_mode="markdown", reply_markup=keyboard)


@dp.message_handler(filters.Text(BUTTON1_TEXT))
async def review(message: types.Message):
    keyboard_remove = types.ReplyKeyboardRemove()
    await message.answer("Пожалуйста введите отзыв:", reply_markup=keyboard_remove)
    reviews = {"user_id": message.from_user.id, "review_start": True, "review": None}
    REVIEWERS.append(reviews)


@dp.message_handler(content_types=["text"])
async def review_message(message: types.Message):
    # for i in REVIEWERS:
    #     if i.get(message.from_user.id):
    #         if i.get("review_start"):
    #             i[review] = message.text
    #             i["review_start"] = False
    REVIEWERS[-1]["review"] = message.text
    await message.answer("спасибо за отзыв!")
    with open("REVIEWS.txt", "a", encoding="utf-8") as f:
        f.write(REVIEWERS[-1].get("review"))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

import logging
from dataclasses import dataclass
from typing import Optional

from aiogram import Bot, Dispatcher, executor, filters, types

from config import API

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot)


WELCOME_MESSAGE = """Здравствуйте, вас приветствует бот из Атлашево!
Будем рады вашему отзыву о нашей продукции!
Для этого нужно нажать кнопку *Оставить отзыв*"""

BUTTON1_TEXT = "🐄Оставить отзыв"

@dataclass
class Review:
    user_id: int
    images: Optional[list[types.PhotoSize]] = None
    message: Optional[str] = None

    @property
    def published(self):
        return self.message is not None

REVIEWERS: list[Review] = []

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
    REVIEWERS.append(Review(message.from_user.id))


@dp.message_handler(content_types=["text"])
async def review_message(message: types.Message):
    user_review = [
        i
        for i in REVIEWERS
        if not i.published
    ]
    if len(user_review) == 1:
        user_review[0].message = message.text
        
        await message.answer("спасибо за отзыв!")

        with open("REVIEWS.txt", "a", encoding="utf-8") as f:
            f.write(str(user_review))
            f.write("\n")
    else:
        await send_welcome(message)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def review_photo(message: types.Message):
    #TODO: Xryak from Cheboksary should to fix it today! 
    user_review = [
        i
        for i in REVIEWERS
        if not i.published
    ]
    if len(user_review) == 1:
        user_review[0].images = message.photo
        
        await message.answer("А теперь текста добавь епта!")
    else:
        await message.answer("НАХЕР МНЕ ТВОЯ ФОТКА!?")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

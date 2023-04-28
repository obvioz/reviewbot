from aiogram import Bot, Dispatcher, executor, types
from config import API

import logging


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    invite_message = "Здравствуйте, вас приветствует бот из Атлашево!\nБудем рады вашему отзыву о нашей продукции!\nДля этого нужно нажать кнопку *Оставить отзыв*"
    await message.answer(
        invite_message, parse_mode="markdown"
    )  # отвечает без комментария


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot)

WELCOME_MESSAGE = """Здравствуйте, вас приветствует бот из Атлашево!
Будем рады вашему отзыву о нашей продукции!
Для этого нужно нажать кнопку *Оставить отзыв*"""


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer(WELCOME_MESSAGE, parse_mode="markdown")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

import logging

from aiogram import Bot, Dispatcher, executor, filters, types

from config import API
from database import DBCtrl

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot)


WELCOME_MESSAGE = """Здравствуйте, вас приветствует бот из Атлашево!
Будем рады вашему отзыву о нашей продукции!
Для этого нужно нажать кнопку *Оставить отзыв*"""

BUTTON1_TEXT = "🐄Оставить отзыв"
BUTTON_ADMIN_KEY = "👨🏿‍🦳Получить отзыв👨🏿‍🦳"
ADMINS = [243568054, 427018143]
# TODO: добавить админскую кнопку


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if message.from_user.id in ADMINS:
        kb = [
            [types.KeyboardButton(text=BUTTON_ADMIN_KEY)],
            [types.KeyboardButton(text=BUTTON1_TEXT)],
        ]
    else:
        kb = [
            [types.KeyboardButton(text=BUTTON1_TEXT)],
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(WELCOME_MESSAGE, parse_mode="markdown", reply_markup=keyboard)


@dp.message_handler(filters.Text(BUTTON1_TEXT))
async def review(message: types.Message):
    keyboard_remove = types.ReplyKeyboardRemove()
    await message.answer("Пожалуйста введите отзыв:", reply_markup=keyboard_remove)
    DBCtrl.create_review_record(message.from_user.id)


@dp.message_handler(content_types=["text"])
async def review_message(message: types.Message):
    # TODO: сделать FSM
    if DBCtrl.get_review_without_message(message.from_user.id):
        DBCtrl.update_review_message(message.from_user.id, message.text)
        await message.answer("Cпасибо за отзыв!")
    else:
        await send_welcome(message)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def review_photo(message: types.Message):
    if user_review := DBCtrl.get_review_without_message(message.from_user.id):
        DBCtrl.create_photo(
            photo_data=message.photo[-1].file_id, review_id=user_review.key_id
        )
        # TODO: выводится столько же раз сколько добавлено фото, нужно только 1 вывод!
        await message.answer("фото добавлено")
    else:
        await message.answer("НАХЕР МНЕ ТВОЯ ФОТКА!?")


# TODO: добавить хендлер который будет обрабатывать фото + текст как отзыв
if __name__ == "__main__":
    DBCtrl.create_tables()
    executor.start_polling(dp, skip_updates=True)

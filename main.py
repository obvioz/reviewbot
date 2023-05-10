import logging
from collections.abc import Iterable

from aiogram import Bot, Dispatcher, executor, filters, types

from config import ADMINS, API
from database import DB
from helpers import get_review_photos

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot)


WELCOME_MESSAGE = """Здравствуйте, вас приветствует бот из Атлашево!
Будем рады вашему отзыву о нашей продукции!
Для этого нужно нажать кнопку *Оставить отзыв*"""

BUTTON1_TEXT = "🐄Оставить отзыв"
BUTTON_ADMIN_KEY = "👨🏿‍🦳Получить отзыв👨🏿‍🦳"
BUTTON_LAST_REVIEW = "Последний отзыв"
BUTTON_LAST_WEEK_REVIEW = "Отзывы за неделю"


def keyboard_generator(*keys: Iterable[str]):
    return [[types.KeyboardButton(text=key)] for key in keys]


def is_admin(user_id: int):
    return user_id in ADMINS


def admin_only(func):
    async def wrapper(message):
        if is_admin(message.from_user.id):
            return await func(message)

    return wrapper


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if message.from_user.id in ADMINS:
        kb = keyboard_generator(BUTTON_ADMIN_KEY, BUTTON1_TEXT)
    else:
        kb = keyboard_generator(BUTTON1_TEXT)
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(WELCOME_MESSAGE, parse_mode="markdown", reply_markup=keyboard)


@dp.message_handler(filters.Text(BUTTON1_TEXT))
async def review(message: types.Message):
    keyboard_remove = types.ReplyKeyboardRemove()
    await message.answer("Пожалуйста введите отзыв:", reply_markup=keyboard_remove)
    DB.create_review_record(message.from_user.id)


@dp.message_handler(filters.Text(BUTTON_ADMIN_KEY))
@admin_only
async def admin_dialog(message: types.Message):
    kb = keyboard_generator(BUTTON_LAST_REVIEW, BUTTON_LAST_WEEK_REVIEW)
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_sticker(
        message.from_user.id,
        sticker="CAACAgIAAxkBAAEIzoJkT7HCr9kC_C3VItfXvyEg6Pdt0AACOQMAArVx2gYjUGZnvEY4rS8E",
        reply_markup=keyboard,
    )


@dp.message_handler(filters.Text(BUTTON_LAST_REVIEW))
@admin_only
async def get_last_review(message: types.Message):
    keyboard_remove = types.ReplyKeyboardRemove()
    review = DB.get_last_review()
    await message.answer(
        f"Последний отзыв от {review.user_id}:", reply_markup=keyboard_remove
    )
    photos = await get_review_photos(review.key_id)
    await message.answer(review.message)
    if photos:
        for photo in photos:
            await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(filters.Text(BUTTON_LAST_WEEK_REVIEW))
@admin_only
async def get_last_week_reviews(message: types.Message):
    keyboard_remove = types.ReplyKeyboardRemove()
    reviews = DB.get_last_week_reviews()
    await message.answer(f"Время почитать отзывы:", reply_markup=keyboard_remove)
    delimiter = "-" * 3
    for review in reviews:
        await message.answer(
            f"{delimiter} CREATED: {review.created_at} USER_ID: {review.user_id} {delimiter}"
        )
        photos = await get_review_photos(int(review.key_id))
        await message.answer(f"{review.message}")
        if photos:
            for photo in photos:
                await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(content_types=["text"])
async def review_message(message: types.Message):
    if DB.get_unpublished_review(message.from_user.id):
        DB.update_review_message(message.from_user.id, message.text)
        await message.answer("Cпасибо за отзыв!")
        DB.publish_review(message.from_user.id)
    else:
        await send_welcome(message)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def review_photo(message: types.Message):
    if user_review := DB.get_unpublished_review(message.from_user.id):
        DB.create_photo(
            photo_data=message.photo[-1].file_id, review_id=user_review.key_id
        )
        if message.caption:
            message.text = message.caption
            await review_message(message)
    else:
        await message.answer("НАХЕР МНЕ ТВОЯ ФОТКА!?")


if __name__ == "__main__":
    DB.create_tables()
    executor.start_polling(dp, skip_updates=True)

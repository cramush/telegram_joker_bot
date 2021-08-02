from aiogram import Bot, Dispatcher, executor, types
from config import telegram_token
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import pymongo
import config
from loguru import logger

client = pymongo.MongoClient(f"mongodb://{config.login}:{config.password}@{config.host}/{config.db_name}")
db = client["my_mongo"]
jokes_collection = db["jokes"]
info_collection = db["info"]

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

random_joke_button = KeyboardButton('Пошути')  # create button

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # create keyboard for button
keyboard.add(random_joke_button)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Жми на кнопку, шутить буду.", reply_markup=keyboard)


@dp.message_handler()
async def get_random_joke(message: types.Message):
    random_joke = jokes_collection.aggregate([{"$sample": {"size": 1}}])
    random_joke = {"content": el["content"] for el in random_joke}
    random_joke = random_joke["content"]

    user_info(message)

    if len(random_joke) > 4096:
        trim_joke = (random_joke[0+i:4096+i] for i in range(0, len(random_joke), 4096))
        for element in trim_joke:
            await bot.send_message(message.from_user.id, element)
    else:
        await bot.send_message(message.from_user.id, random_joke)


def user_info(message):
    info_from = message["from"]

    info_id = info_from["id"]
    info_first_name = info_from["first_name"]
    info_username = info_from["username"]
    info_date = message["date"]
    info_text = message["text"]

    user_info_container = {
        "user_id": info_id,
        "first_name": info_first_name,
        "username": info_username,
        "date": info_date,
        "content": info_text
    }
    info_collection.insert_one(user_info_container)

    for_logger = {
        "first_name": info_first_name,
        "username": info_username
    }
    logger.info(for_logger)


if __name__ == '__main__':
    executor.start_polling(dp)

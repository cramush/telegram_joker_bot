from aiogram import Bot, Dispatcher, executor, types
from config import telegram_token
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import pymongo
import config

client = pymongo.MongoClient(f"mongodb://{config.login}:{config.password}@{config.host}/{config.db_name}")
db = client["jokes_db"]
collection = db["jokes"]

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
    random_joke = collection.aggregate([{"$sample": {"size": 1}}])
    random_joke = {"content": el["content"] for el in random_joke}
    random_joke = random_joke["content"]

    if len(random_joke) > 4096:
        # print(len(random_joke))
        trim_joke = (random_joke[0+i:4096+i] for i in range(0, len(random_joke), 4096))
        for element in trim_joke:
            await bot.send_message(message.from_user.id, element)
    else:
        # print(len(random_joke))
        await bot.send_message(message.from_user.id, random_joke)


if __name__ == '__main__':
    executor.start_polling(dp)

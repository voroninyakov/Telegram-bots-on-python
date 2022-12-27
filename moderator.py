import logging
from aiogram import *
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

TOKEN = '5528962277:AAGuY3KApYJijpYsWwes8SmnN0VgSQoU4K8'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

black_word = ['плохое слово']

@dp.message_handler()
async def send_banned(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    t = text.lower()
    for i in black_word:
        if i in t:
            await bot.kick_chat_member(chat_id, user_id)
    if t == "привет":
        await bot.send_message(chat_id, 'привет!')
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

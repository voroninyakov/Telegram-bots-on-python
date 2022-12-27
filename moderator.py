import logging
from aiogram import *
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# настройки бота
TOKEN = '5528962277:AAGuY3KApYJijpYsWwes8SmnN0VgSQoU4K8'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
black_word = ['плохое слово']

# обработка сообщений
@dp.message_handler()
async def send_banned(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    lower_text = text.lower()
    for i in black_word:
        if i in lower_text:
            await bot.kick_chat_member(chat_id, user_id)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

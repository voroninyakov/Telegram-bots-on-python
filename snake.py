import logging
from aiogram import *

API_TOKEN = '2078221579:AAFvzGYi3zVLGYij7Rn3Vm4VUNFn77cka0o'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def message_ask(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    t = text.lower()
    if t == 'мой id':
        await message.reply(message.from_user.id)
    elif t == 'id чата':
        await message.reply(chat_id)
    elif t == 'привет':
        await message.reply("привет")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import codecs
import os.path

TOKEN = ""  # ваш токен
bot = telebot.TeleBot(TOKEN)

number_of_warnings = 5  # количество предупреждений

make_new_word = [False, 0, 0]

your_id = ''  # id того, кто сможет управлять ботом

# daymaner

menu = InlineKeyboardMarkup()

quantity_warning = {}


def read(what, file):
    """
    :param what: Что мы считываем (слова или чаты).
    :param file: Какой файл считываем.
    :return: Либо список слов, либо словарь файлов {id_чата: имя_файла_слов_чата}.
    """
    if what == 'слова':
        if os.path.exists(file):
            with codecs.open(file, mode='r', encoding='utf-8') as f:
                ftext = f.read()
                splt_word = ftext.split('\r')
                for i in splt_word:
                    if i == '':
                        splt_word.remove('')
                return splt_word
        else:
            with open(file, mode='w+'):
                pass
            return []
    elif what == 'чаты':
        chats = {}
        with codecs.open('chats_id.txt', 'r', encoding='utf-8') as f:
            ftext = f.read()
            splt_id = ftext.split(' ')
            for i in splt_id:
                if i == '':
                    splt_id.remove('')
            for i in range(len(splt_id)):
                splt_id[i] = int(splt_id[i])
        with codecs.open('chats_name.txt', 'r', encoding='utf-8') as f:
            ftext = f.read()
            splt_name = ftext.split('\r')
            for i in splt_name:
                if i == '':
                    splt_name.remove('')
        for i in range(len(splt_id)):
            chats[str(splt_id[i])] = splt_name[i]
        return chats
    else:
        return {}


def write(what, listof, file):
    """

    :param what: То, что мы записываем.
    :param listof: Список того, что мы записываем.
    :param file: Какой файл мы откроем для записи.
    :return: None, мы нечего не возвращаем, а просто записываем всё в файлы.
    """
    if what == 'слова':
        with open(file, 'w+', encoding='utf-8') as f:
            words = ''
            for i in listof:
                words += f'{i}\r'
            f.write(words)
    elif what == 'чаты':
        with open('chats_name.txt', 'w', encoding='utf-8') as f:
            for chat_id in listof:
                f.write(f"{listof[chat_id]}\r")
        with open('chats_id.txt', 'w', encoding='utf-8') as f:
            for chat_id in listof:
                f.write(f"{chat_id} ")


@bot.message_handler(content_types=['new_chat_members'])
def delete_join_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except telebot.apihelper.ApiTelegramException:
        pass


@bot.message_handler(content_types=['left_chat_member'])
def delete_leave_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except telebot.apihelper.ApiTelegramException:
        pass


@bot.message_handler(commands=['run'])
def starts(message):
    if message.from_user.username == 'klliru' or message.from_user.username == 'i_in_telegram':
        chats_menu = InlineKeyboardMarkup()
        chats_where_user_is_admin = []
        chats = read('чаты', None)
        f = chats
        try:
            for chats_id in chats:
                chat_id = int(chats_id)
                try:
                    if bot.get_chat_member(chat_id, message.from_user.id).status == 'administrator' or \
                            bot.get_chat_member(chat_id, message.from_user.id).status == 'creator':
                        chats_menu.add(InlineKeyboardButton(str(read('чаты', None)[chats_id]),
                                                            callback_data=f'{chat_id} chats_menu'))
                        chats_where_user_is_admin.append(chat_id)
                except telebot.apihelper.ApiTelegramException:
                    del f[chats_id]
                    write('чаты', f, 'daymaner')
                    os.remove(f'{chats_id}.txt')
            if chats_where_user_is_admin:
                bot.send_message(message.from_user.id, f'Привет {message.from_user.username}!😁\n \
Выбери в какой группе хочешь настроить слова!', reply_markup=chats_menu)
            else:
                bot.send_message(message.from_user.id, f'Привет {message.from_user.username}!☹️😢🥺\n \
ты никуда меня не добавил!', reply_markup=chats_menu)
        except RuntimeError:
            bot.send_message(message.from_user.id, f'Привет {message.from_user.username}!\n \
Я не успел удалить группу😢 \n Отправь эту команду ещё раз', reply_markup=chats_menu)
        except telebot.apihelper.ApiTelegramException:
            bot.send_message(message.from_user.id, f'Привет {message.from_user.username}!\n \
            Я не удалил группу😢 \n Отправь эту команду ещё раз', reply_markup=chats_menu)


@bot.message_handler(commands=['help'])
def menu_chats(message):
    if message.from_user.username == 'klliru' or message.from_user.username == 'i_in_telegram':
        bot.send_message(message.from_user.id, f'Ты прислал команду помощь сейчас отвечу на возможные вопросы: \n \
Как добавить группу? \n \
\n \
Добавь в группу этого бота.Затем сделай его там администратором и напиши в чат который добавишь\
любое сообщение.Если группа не была добавлена, то бот добавит её.Соответственно для всех этих действий ты должен быть \
администратором.', reply_markup=menu)


@bot.callback_query_handler(func=lambda call: True)
def to_chat(call):
    menu_words = InlineKeyboardMarkup()
    call_data = call.data.split(' ')
    chat_id = call_data[0]
    if call_data[1] == 'chats_menu':
        menu_of_chats = InlineKeyboardMarkup()
        menu_of_chats.add(InlineKeyboardButton('Добавить слово', callback_data=f'{chat_id} создать'))
        if read('слова', f'{chat_id}.txt'):
            menu_of_chats.add(InlineKeyboardButton('Удалить слово', callback_data=f'{chat_id} удалить'))
        menu_of_chats.add(InlineKeyboardButton('Выйти', callback_data=f'выйти настройки {chat_id}'))
        bot.send_message(call.from_user.id, 'Так теперь выбери что будешь делать', reply_markup=menu_of_chats)
    elif call_data[1] == 'удалить':
        words_of_chat = read('слова', f'{chat_id}.txt')
        if words_of_chat:
            for word in words_of_chat:
                menu_words.add(InlineKeyboardButton(f'{word} ❌', callback_data=f'{chat_id} удалено {word}'))
            menu_words.add(InlineKeyboardButton('Выйти', callback_data=f'выйти слова {chat_id}'))
            bot.send_message(call.from_user.id, 'Выбери что хочешь удалить', reply_markup=menu_words)
    elif call_data[1] == 'удалено':
        word = call_data[2]
        words_of_chat = read('слова', f'{chat_id}.txt')
        words_of_chat.remove(word)
        write('слова', words_of_chat, f'{chat_id}.txt')
        words_of_chat = read('слова', f'{chat_id}.txt')
        if words_of_chat:
            for word in words_of_chat:
                menu_words.add(InlineKeyboardButton(f'{word} ❌', callback_data=f'{chat_id} удалено {word}'))
            menu_words.add(InlineKeyboardButton('Выйти', callback_data=f'выйти слова {chat_id}'))
            bot.send_message(call.from_user.id, 'В чате остались слова:', reply_markup=menu_words)
        else:
            menu_words.add(InlineKeyboardButton('Выйти', callback_data=f'выйти слова {chat_id}'))
            bot.send_message(call.from_user.id, 'В чате больше нет запрещённых слов!', reply_markup=menu_words)
    elif call_data[0] == 'выйти':
        chat_id = call_data[2]
        if call_data[1] == 'настройки':
            menu_of_chats = InlineKeyboardMarkup()
            for strind_id in read('чаты', None):
                chat_id = int(strind_id)
                if bot.get_chat_member(chat_id, call.from_user.id).status == 'creator':
                    menu_of_chats.add(
                        InlineKeyboardButton(read('чаты', None)[strind_id], callback_data=f'{chat_id} chats_menu'))
            bot.send_message(call.from_user.id, 'Вы вышли в меню чата\n \
Выбери в какой группе хочешь настроить слова!', reply_markup=menu_of_chats)
        elif call_data[1] == 'слова':
            menu_of_chats = InlineKeyboardMarkup()
            menu_of_chats.add(InlineKeyboardButton('Добавить слово', callback_data=f'{chat_id} создать'))
            if read('слова', f'{chat_id}.txt'):
                menu_of_chats.add(InlineKeyboardButton('Удалить слово', callback_data=f'{chat_id} удалить'))
            menu_of_chats.add(InlineKeyboardButton('Выйти', callback_data=f'выйти настройки {chat_id}'))
            bot.send_message(call.from_user.id, 'Вы вышли в меню группы\n \
Выбери в какой группе хочешь настроить слова!', reply_markup=menu_of_chats)
    elif call_data[1] == 'создать':
        bot.send_message(call.from_user.id, 'Присылай новые слова: каждое в отдельном сообщении.\n \
Напиши "всё", если закончил.')
        global make_new_word
        make_new_word = [True, chat_id, call_data[0]]


@bot.message_handler(content_types=['text'])
def moderator(message):
    global make_new_word
    chat_menu = InlineKeyboardMarkup()
    chat_menu.add(InlineKeyboardButton('Добавить слово', callback_data=f'{make_new_word[1]} создать'))
    if read('слова', f'{make_new_word[1]}.txt'):
        chat_menu.add(InlineKeyboardButton('Удалить слово', callback_data=f'{make_new_word[1]} удалить'))
    chat_menu.add(InlineKeyboardButton('Выйти', callback_data=f'выйти настройки {make_new_word[1]}'))
    text = message.text.lower()
    all_words = read('слова', f'{make_new_word[1]}.txt')
    all_chats = read('чаты', 'daymaner')
    all_chats_id = []
    text_list = text.split(' ')
    for i in read('слова', f'{message.chat.id}.txt'):
        word = i.split('\r')[0]
        for j in text_list:
            if word in str(j) and bot.get_chat_member(message.chat.id, message.from_user.id).status != 'creator' and \
                    bot.get_chat_member(message.chat.id, message.from_user.id).status != 'administrator':
                try:
                    if quantity_warning[str(message.from_user.id) + " " + str(message.chat.id)] < 4:
                        quantity_warning[str(message.from_user.id) + " " + str(message.chat.id)] += 1
                        if 4 - quantity_warning[str(message.from_user.id) + " " + str(message.chat.id)] == 1:
                            count = 'раз'
                        else:
                            count = 'раза'
                        bot.send_message(message.chat.id, f'Привет, {message.from_user.username}! \n \
@{message.from_user.username} получил предупреждение.@{message.from_user.username} отправил в чат({message.chat.title} \
) запрещённое слово. Если @{message.from_user.username} сделает так ещё \
{str(number_of_warnings - quantity_warning[str(message.from_user.id) + " " + str(message.chat.id)]) + " " + count},то \
тебя забанит в нём этот бот.')
                        bot.delete_message(message.chat.id, message.message_id)
                    elif quantity_warning[str(message.from_user.id) + " " + str(message.chat.id)] == 4:
                        try:
                            bot.kick_chat_member(message.chat.id, message.from_user.id)
                        except telebot.apihelper.ApiTelegramException:
                            pass
                except KeyError:
                    quantity_warning[str(message.from_user.id) + " " + str(message.chat.id)] = 1
                    bot.delete_message(message.chat.id, message.message_id)
            elif word in j and bot.get_chat_member(message.chat.id, message.from_user.id).status == 'creator' or \
                    bot.get_chat_member(message.chat.id, message.from_user.id).status == 'administrator':
                bot.delete_message(message.chat.id, message.message_id)
    for i in all_chats:
        all_chats_id.append(str(all_chats[i]))
    if text == 'всё':
        make_new_word[0] = False
        bot.send_message(message.from_user.id, 'Готово!Можешь продолжить управление.', reply_markup=chat_menu)
    elif str(message.chat.id) not in all_chats_id and message.chat.id != message.from_user.id:
        all_chats[str(message.chat.id)] = message.chat.title
        write('чаты', all_chats, f'{make_new_word[1]}.txt')
    elif make_new_word[0] and message.from_user.username == your_id:
        all_words.append(text)
        write('слова', all_words, f'{make_new_word[1]}.txt')


bot.infinity_polling()

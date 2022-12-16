import telebot
#from telebot import types


textUsers = []
resultListAlg = []
intermediate_list = []
checkАction = 0
global mRoot
# Создаем экземпляр бота
bot = telebot.TeleBot('5778440922:AAGM4cixN6aOsocfxJoLBSEHNFBQbZTpk9s')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    global checkАction
    checkАction = 0
    mRoot = m

    bot.send_message(mRoot.chat.id, text = "Привет, {0.first_name}! Данный бот предназначен для помощи бедным студентам.".format(mRoot.from_user))
    bot.send_message(mRoot.chat.id, "Eго смысл в том, чтобы вы не тратили большое количество времени "
                                    "на ручной просчет. Для того, чтобы начать, просто нажми кнопку ""Поехали")
    # Добавляем кнопку
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Поехали")
    markup.add(btn1)
    bot.send_message(m.chat.id, text="Жду...".format(m.from_user), reply_markup=markup)

type_message = 'В текстовом'
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global checkАction
    global type_message
    if checkАction == 0 and message.text.strip() == 'Поехали':
        firstOperation(message, 'сообщение')
        checkАction += 1
        return
    if checkАction == 1:
        if message.text.strip() == 'В двоичном' or message.text.strip() == 'В текстовом':
            type_message = message.text.strip()
        bot.send_message(message.chat.id, 'Пожалуйста введите сообщение')
        checkАction += 1
        return
    if checkАction == 2:
        messageInput(message)
        if checkАction == 1:
            return
        checkАction += 1
        firstOperation(message, 'H0')
        return
    if checkАction == 3:
        if message.text.strip() == 'В двоичном' or message.text.strip() == 'В текстовом':
            type_message = message.text.strip()
        bot.send_message(message.chat.id, 'Пожалуйста введите H0')
        checkАction += 1
        return
    if checkАction == 4:
        H0Input(message)
        if checkАction == 3:
            return
        checkАction += 1
        preparing_for_solution(message)
        return

global_bit_sms = ''
global_bit_H0 = ''
def preparing_for_solution(message):
    bit_sms = global_bit_sms
    H0 = global_bit_H0

    resultListAlg.append(H0)
    len_bit_sms = len(bit_sms)
    len_H0 = len(H0)
    remainder = len_bit_sms % len_H0

    if remainder > 0:
        factor = len_bit_sms // len_H0
        mnoj = factor + 1
        first = len_H0 * mnoj
        difference = first - len_bit_sms
        for i in range(difference):
            if i == 0:
                bit_sms += '1'
            if i > 0:
                bit_sms += '0'
        bot.send_message(message.chat.id,'Мы тут пошуршали и докинули пару битиков, чтобы алгоритм работал корректно...')
        bot.send_message(message.chat.id, f'Отредактированная битовая последовательность: {bit_sms}')
        list_bit_sms = [bit_sms[j:j + len_H0] for j in range(0, len(bit_sms), len_H0)]
    else:
        list_bit_sms = [bit_sms[k:k + len_H0] for k in range(0, len(bit_sms), len_H0)]

    kk = 0
    bot.send_message(message.chat.id, '*чик-чик*')
    bot.send_message(message.chat.id, 'А ой, мы тут порезали твою битовую последовательность на равные части, для дальшейших манипуляций.')
    bot.send_message(message.chat.id, 'Взгляни, что получилось:')
    string_list_items = ''
    for elem in list_bit_sms:
        kk += 1
        string_list_items += f'{kk}-ый элемент списка: {elem}\n'
    bot.send_message(message.chat.id, f'{string_list_items}')

    bot.send_message(message.chat.id, 'Эх...ну разве не красота? \n')


def H0Input(message):
    global checkАction
    if type_message == 'В двоичном':
        H0 = message.text.strip()
        bit_H0 = H0
        if bit_H0 == '':
            bot.send_message(message.chat.id, 'Скорее всего вы ошиблись, так как строка была пуста((')
            checkАction = 3
            return
        if checkBit(H0):
            bot.send_message(message.chat.id, 'Думаю вам нужен текстовый вид представления')
            firstOperation(message, 'H0')
            checkАction = 3
            return
    if type_message == 'В текстовом':
        H0 = message.text.strip()
        bit_H0 = ''.join(format(ord(x), '08b') for x in H0)
        if bit_H0 == '':
            bot.send_message(message.chat.id, 'Скорее всего вы ошиблись, так как строка была пуста((')
            checkАction = 3
            return
        bot.send_message(message.chat.id, f'Ваш H0 в двоичном виде {bit_H0}')
    global global_bit_H0
    global_bit_H0 = bit_H0

def messageInput(message):
    global checkАction
    if type_message == 'В двоичном':
        sms = message.text.strip()
        bit_sms = sms
        if bit_sms == '':
            bot.send_message(message.chat.id, 'Скорее всего вы ошиблись, так как строка была пуста((')
            checkАction = 1
            return
        if checkBit(sms):
            bot.send_message(message.chat.id, 'Думаю вам нужен текстовый вид представления')
            firstOperation(message, 'сообщение')
            checkАction = 1
            return
    if type_message == 'В текстовом':
        sms = message.text.strip()
        bit_sms = ''.join(format(ord(x), '08b') for x in sms)
        if bit_sms == '':
            bot.send_message(message.chat.id, 'Скорее всего вы ошиблись, так как строка была пуста((')
            checkАction = 1
            return
        bot.send_message(message.chat.id, f'Ваше сообщение в двоичном виде {bit_sms}')
    global global_bit_sms
    global_bit_sms = bit_sms


def firstOperation (message, message_or_H0):
    bot.send_message(message.chat.id, f'В каком виде у вас {message_or_H0}?')
    bot.send_message(message.chat.id, 'В двоичном')
    knopki(message)

def knopki(message):
    # Добавляем кнопки
    telebot.types.ReplyKeyboardRemove()  # очищаем старые кнопки
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("В двоичном")
    item2 = telebot.types.KeyboardButton("В текстовом")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, text="В текстовом".format(message.from_user), reply_markup=markup)

def checkBit(str):
    for i in range(len(str)):
        ch = str[i]
        if str[i] != '0' and str[i] != '1':
            return 1
    return 0

# Запускаем бота
bot.polling(none_stop=True, interval=0)

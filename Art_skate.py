import telebot
from Config import token
import logging
from telebot import types

bot = telebot.TeleBot(token)

def filter_dialog(record: logging.LogRecord):
    if 'id' in record.getMessage():
        return record.getMessage()

logger = telebot.logger
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.csv', encoding='UTF-8')
handler.setFormatter(logging.Formatter(fmt='[%(levelname)s: %(asctime)s] %(message)s'))
logger.addFilter(filter_dialog)
logger.addHandler(handler)

def num_cell(message):
    cell = message.text
    return str(cell)

@bot.message_handler(commands=['start'])
def print_mess_first(message):
    text_message_01 = f'<b> Приветствую, {message.from_user.first_name} {message.from_user.last_name}!</b>'
    text_message_02 = f'<b>Этот бот поможет вам оперативно получить первичную информацию!</b>'
    bot.send_message(message.chat.id, text_message_01, parse_mode='html')
    bot.send_message(message.chat.id, text_message_02, parse_mode='html')
    start(message)
def start(message):
    text_message_01 = f'<b>Выберите пункт меню:</b>'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    start = types.KeyboardButton("СТАРТ")
    website = types.KeyboardButton("Мы в интернете")
    offers = types.KeyboardButton("Наши услуги")
    help = types.KeyboardButton("Помощь")
    markup.add(start, offers, website, help)
    bot.send_message(message.chat.id, text_message_01, parse_mode='html', reply_markup=markup)
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Мы в интернете': 
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Посетить страницу в ВКОНТАКТЕ', url='https://vk.com/artskate'))
        markup.add(types.InlineKeyboardButton('Сайт Арт - скейт', url='https://rollersport54.ru/art-skate/'))
        markup.add(types.InlineKeyboardButton('Страница в Instagram', url='https://www.instagram.com/art_skate/'))
        bot.send_message(message.chat.id, 'Вы хотите посетить страницу в ВКОНТАКТЕ или зайти на сайт', reply_markup=markup)
    elif message.text == 'Наши услуги':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        timetable = types.KeyboardButton('Расписание')
        price = types.KeyboardButton('Стоимость')
        contacts = types.KeyboardButton('Контакты')
        details = types.KeyboardButton('Подробнее о группах')
        back = types.KeyboardButton('Назад')
        markup.add(timetable, price, details, contacts, back)
        bot.send_message(message.chat.id, 'Выберите пункт меню:', reply_markup=markup)
    elif message.text == 'Расписание':
        img = open('GTren.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
    elif message.text == 'Стоимость':
        markup = types.InlineKeyboardMarkup(row_width=2)
        price_group = types.InlineKeyboardButton('Групповые занятия', callback_data='Групповые занятия')
        discounts = types.InlineKeyboardButton('Скидки на гр. зан.', callback_data='Скидки')
        privat_tren = types.InlineKeyboardButton('Индивидуальные занятия', callback_data='Индивидуальные занятия')
        service = types.InlineKeyboardButton('Услуги роллер дрома', callback_data='Услуги роллер дрома')
        payment = types.InlineKeyboardButton('Форма оплаты', callback_data='Форма оплаты')
        markup.add(price_group, discounts, privat_tren, service, payment)
        bot.send_message(message.chat.id, 'Выберите услугу:', reply_markup=markup)
    elif message.text == 'Контакты':
        bot.send_message(message.chat.id, f'Позвонить можно по телефону:\n<b>+7 (983) - 306 - 21 - 13 </b>', parse_mode='html')
        bot.send_message(message.chat.id, f'Наш сайт:\n<b>https://rollersport54.ru/art-skate/</b>', parse_mode='html')
        bot.send_message(message.chat.id, f'Страница в ВКОНТАКТЕ:\n<b>https://vk.com/artskate</b>', parse_mode='html')   
    elif message.text == 'Помощь':
        text_message_03 = f'{message.from_user.first_name}, если вы не нашли нужную информацию, \nпозвоните нам по телефону: \n<b>+7 (983) - 306 - 21 - 13 </b>'
        bot.send_message(message.chat.id, text_message_03, parse_mode='html')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Отправить cообщение в WhatsApp', url='https://api.whatsapp.com/send/?phone=79833062113&type=phone_number&app_absent=0'))
        bot.send_message(message.chat.id, 'или напишите в WhatsApp', reply_markup=markup)
    elif message.text == 'Подробнее о группах':
        markup = types.InlineKeyboardMarkup(row_width=2)
        general_groups = types.InlineKeyboardButton('Общие группы', callback_data='Общие группы')
        sports_groups = types.InlineKeyboardButton('Спортивные группы', callback_data='Спортивные группы')
        basics = types.InlineKeyboardButton('Основы', callback_data='Основы')
        master_classes = types.InlineKeyboardButton('Мастер классы', callback_data='Мастер классы')
        markup.add(general_groups, sports_groups, basics, master_classes)
        bot.send_message(message.chat.id, 'Выберите группу:', reply_markup=markup)
    elif message.text == 'Назад':
        start(message)       
    elif message.text == 'СТАРТ':
        start(message)
    else:
        bot.send_sticker(message.chat.id, 'https://tlgrm.ru/_/stickers/5a4/2e3/5a42e329-b131-3d7c-a069-662e320a7c32/192/15.webp')
        bot.send_message(message.chat.id, 'Команду не удалось распознать...')
        start(message)
@bot.callback_query_handler(func=lambda call:True)
def img(call):
    if call.data == 'Групповые занятия':
        bot.send_message(call.message.chat.id, 
        f'* <b>Разовое</b> посещение 800 р.\n* <b>4 занятия</b> в месяц  3200 р. / 2600 р. (пониженная стоимость)\n* <b>8 занятий</b> в месяц  4800 р. / 4000 р. (пониженная стоимость)\n* <b>12 занятий</b> в месяц  6500 р. / 5500 р. (пониженная стоимость)\n* <b>16 занятий</b> в месяц  7500 р. / 6400 р. (пониженная стоимость)', parse_mode='html')
    elif call.data == 'Скидки':
        bot.send_message(call.message.chat.id, 
        f'<b>СКИДКИ</b> — действуют только на групповые занятия.\n<b>ПОНИЖЕНАЯ СТОИМОСТЬ</b> действует при покупке абонемента до завершения действующего (5 недель или последнее занятие), либо при покупке абонемента в день первого занятия или мастер-класса.\n<b>50 % СКИДКА</b> на абонемент для второго ребенка из одной семьи (меньший из абонементов).\n<b>БЕСПЛАТНОЕ ГРУППОВОЕ ЗАНЯТИЕ</b> если привел друга. Действует единоразово и при условии, что друг ранее не занимался в школе.', parse_mode='html')
    elif call.data == 'Индивидуальные занятия':
        bot.send_message(call.message.chat.id,
        f'<b>1 занятие</b> — 1000 р. (2 человека — 1500 р., 3 человека — 2000 р.)\n<b>4 занятия</b> — 3600 р. (есть абонемент на 2 и 3 человек)\n<b>8 занятий</b> — 6400 р. (есть абонемент на 2 и 3 человек)\n<b>Индивидуальное занятие для Спортсменов</b> — 1500 р.', parse_mode='html')
    elif call.data == 'Услуги роллер дрома':
        bot.send_message(call.message.chat.id,
        f'<b>Прокат роликов</b> — 250 р. (есть абонементы на 4 и 8 прокатов)\n<b>Посещение (2 часа)</b> — 300 р. (есть абонементы на 5 и 10 посещений)\n<b>Посещение «безлимит»</b> — 3000 р. (1 месяц)',parse_mode='html')
    elif call.data == 'Форма оплаты':
        bot.send_message(call.message.chat.id,
        f'<b>Наличные</b>\n<b>Безнал (эквайринг)</b>\n<b>QR (в приложении Сбер-онлайн)</b>', parse_mode='html')
    elif call.data == 'Общие группы':
        bot.send_message(call.message.chat.id,
        f'<b>ОБЩИЕ ГРУППЫ</b> — занятия  для поддержания физической формы, приобретение и оттачивания мастерства катания на роликах. Участие в соревнованиях не обязательны.\n<b>Базовые навыки</b> — навыки необходимые для продолжения занятий в группах продвинутого катания и спортивных групп начального уровня.\n<b>Продвинутое катание</b> — занятия по закреплению базовых навыков и продвинутого катания, основы фрискейта, фигурного катания и фристайл слалома.\n<b>Взрослые</b> — занятия по базовым и продвинутым навыкам, основы фигурного катания и фристайл слалома, фитнес на роликах.\n<b>Семейные группы</b> — формат семейных занятий, дети и взрослые в одной группе.', parse_mode='html')
    elif call.data == 'Спортивные группы':
        bot.send_message(call.message.chat.id,
        f'<b>СПОРТИВНЫЕ ГРУППЫ</b> — подготовка спортсменов к участию в соревнованиях по роллер спорту. Начинивающие группы по ступеням; спортивные группы по разрядам. В тренировочный процесс включены: занятия в кроссовках, на роликах,  и растяжке. Дополнительно занятия по хореографии, скольжению и растяжке. Требования к ученикам — владение базовыми навыками.\n<b>Фигурное катание</b> — подготовка спортсменов для соревнований по нормативам и спортивным разрядам. А так же подготовка к участию в соревнованиях «Лиги любителей фигурного катания на роликовых коньках».\n<b>Фристайл слалом</b> — подготовка по дисциплинам Фристайл Слалом Классика и Скоростной слалом.\n<b>Хореография</b> —  работа над корпусом, спиной руками, развитие чувства ритма, растяжка.', parse_mode='html')
    elif call.data == 'Основы':
        bot.send_message(call.message.chat.id,
        f'<b>ОСНОВЫ</b> — минимальные навыки катания на роликах, необходимые для занятий в группе (падение, подъем, движение вперед, остановка). Если вы совсем не умеете кататься на роликах, то мы предлагаем следующие варианты обучения:\n<b>Мастер-классы</b> — занятие «знакомство» с новенькими учениками. Предназначены для оценки уровня катания и подготовки начинающих к групповым занятиям. На мастер классе проходит обучение основной стойке на роликах, падение, простые шаги и остановки. После прохождения мастер-класса мы сможем подобрать для вас подходящую группу.', parse_mode='html')
    elif call.data == 'Мастер классы':
        bot.send_message(call.message.chat.id,
        f'<b>Индивидуальные занятия</b> — занятия с тренером индивидуально или в мини-группе для более качественной подготовки к соревнованиям, проработке отдельных упражнений и постановке программ для соревнований. Для новеньких  прекрасная возможность быстрее встать на ролики и освоить базовые навыки катания (в сравнении с групповыми). Индивидуальные занятия не вносятся в расписание и проводятся в свободное от групповых занятий время.\n<i>Возможны индивидуальные условия и комбинации абонементов, в зависимости от вашей занятости в школе и других коллективах.</i>', parse_mode='html')
print('Bot is started')
bot.polling(non_stop=True)


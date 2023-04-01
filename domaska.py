import telebot
from telebot import types
from telebot.types import LabeledPrice
import psycopg2
import random
from flask import Flask, request
import os


token = '5834072852:AAExuvtIwXrzKnjeb_dfs9WUVXgoS1mKkz4'
provider_token = '350862534:LIVE:Y2IzYzM1YzU1ZDNj'
DB_URI = "postgres://tfikypeo:TC-vm7GF-CIL5ZoLZ06mAzJE3rfSFqqj@mouse.db.elephantsql.com/tfikypeo"
db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()
teachers = [843373640]

url = f'https://domaska-bot.herokuapp.com/{token}'
bot = telebot.TeleBot(token, threaded=False)


app = Flask(__name__)


@app.route('/' + token, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok', 200


@app.route('/')
def wedhook():
    bot.remove_webhook()
    bot.set_webhook(url=url)
    return 'ok', 200


def pay(message):
    global money
    global ready
    ready = 0
    prices = [LabeledPrice(label='Mājas darbs', amount=money),
              LabeledPrice('uz tēju', 1)]
    bot.send_invoice(
        message.chat.id,  # chat_id
        'Mājas darbs',  # title
        ' Mājas darba izplidīšana',  # description
        'Mājas darbs',  # invoice_payload
        provider_token,  # provider_token
        'eur',  # currency
        prices,  # prices
        photo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Homework_-_vector_maths.jpg/330px-Homework_-_vector_maths.jpg',
        photo_height=512,  # !=0/None or picture won't be shown
        photo_width=512,
        photo_size=512,
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter='md')


def info(call):
    global message1
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙", callback_data='back'))
    message1 = bot.edit_message_text(f"""1. Nospediet uz izdarīt mājas darbu un nosūtiet darba dokumentu vai foto 
 \n2. Uzrakstiet, kad vēlaties to saņemt un komentārus
 \n3. Gaidiet apstiprinājumu no mūsu komandas
 \n4. Ja tas ir apstiprināts, samaksājiet par pakalpojumu, izmantojot komandu /buy""", reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)


def start(call):
    global message1
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "Izdarīt mājasdarbu", callback_data='md'))
    markup.add(types.InlineKeyboardButton("Instrukcija", callback_data='info'))
    markup.add(types.InlineKeyboardButton(
        "Nosūtīt ziņu", callback_data='about-md'))
    message1 = bot.edit_message_text(f'Welcome to Ⓜ️ājasDarba bot🤖\n\nNospiediet uz pogu instrukcija lai uzzinātu vairāk\n\nJūsu ātrākais palīgs🏎',
                                     reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)


def md(call):
    global message1
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙", callback_data='back'))
    message1 = bot.edit_message_text(f"1.Nosūtiet darba dokumentu vai foto(document, photo)",
                                     reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)


def kommentari(message):
    global message1
    global ready
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙", callback_data='back'))
    message1 = bot.edit_message_text(f"Paldies, gaidiet apstiprinājumu no mūsu komandas",
                                     reply_markup=markup, chat_id=message.chat.id, message_id=message1.message_id)
    user_id = message.from_user.id
    order_number = random.randint(1000, 9999)
    db_object.execute(
        'INSERT INTO pasutijums(id, order_number) VALUES(%s,%s)', (user_id, order_number))
    db_connection.commit()
    for i in teachers:
        bot.forward_message(
            chat_id=i, from_chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(i, text=f"{order_number}")
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    ready = 0


def aboutmd(call):
    global message1
    global ready
    ready = 6
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙", callback_data='back'))
    message1 = bot.edit_message_text(f"Sūtiet sms", reply_markup=markup,
                                     chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Diemžēl maksājums nenotika,"
                                                "mēģiniet vēlreiz pēc 2 minūtēm")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Paldies par apmaksu! Mēs izdarīsim Jūsu md pēc iespējas ātrāk!'
                     'Ja rodas jautājumi izvēleties pogu |nosūtīt ziņu| galvenā menu '.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')

    user_id = message.from_user.id
    db_object.execute(
        f"SELECT order_number FROM pasutijums WHERE id = '{user_id}'")
    result = db_object.fetchone()
    b0 = str(result)
    b1 = b0.replace("(", "")
    b2 = b1.replace(")", "")
    b3 = b2.replace(",", "")
    for i in teachers:
        bot.send_message(i, f'Order {b3} of user {user_id} was paid')


@bot.message_handler(commands=['submit'])
def submit(message):
    global ready
    ready = 4
    bot.send_message(message.chat.id, "Enter order number")


@bot.message_handler(commands=['done'])
def done(message):
    global ready
    ready = 3
    bot.send_message(message.chat.id, "Enter order number")


@bot.message_handler(commands=['accept'])
def accept(message):
    global ready
    ready = 2
    bot.send_message(message.chat.id, "Enter order number")


@bot.message_handler(commands=['buy'])
def command_pay(message):
    global message1
    global client_id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("5 💶", callback_data='5'))
    markup.add(types.InlineKeyboardButton("10 💶", callback_data='10'))
    markup.add(types.InlineKeyboardButton("15 💶", callback_data='15'))
    markup.add(types.InlineKeyboardButton("20 💶", callback_data='20'))
    markup.add(types.InlineKeyboardButton("25 💶", callback_data='25'))
    markup.add(types.InlineKeyboardButton("30 💶", callback_data='30'))
    markup.add(types.InlineKeyboardButton("35 💶", callback_data='35'))
    markup.add(types.InlineKeyboardButton("40 💶", callback_data='40'))
    markup.add(types.InlineKeyboardButton("50 💶", callback_data='50'))
    client_id = message.chat.id
    message1 = bot.send_message(
        message.chat.id, "Izvēlieties cenuⓂ️", reply_markup=markup).message_id


@bot.message_handler(content_types=['document', 'photo', 'audio'])
def addfile(message):
    global message1
    global ready
    global a3
    if ready == 5:
        bot.send_message(a3, f'Jūsu darbs:')
        bot.forward_message(a3, from_chat_id=message.chat.id,
                            message_id=message.message_id)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙", callback_data='back'))
        for i in teachers:
            bot.forward_message(
                chat_id=i, from_chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)
        message1 = bot.edit_message_text(f"2.Uzrakstiet, kad vēlaties saņemt darbu un komentārus",
                                         reply_markup=markup, chat_id=message.chat.id, message_id=message1.message_id)
        ready = 1


@bot.message_handler(commands=['start'])
def message_reply_start(message):
    global message1
    user_id = message.from_user.id
    username = message.from_user.first_name
    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()
    if not result:
        db_object.execute(
            "INSERT INTO users(id, username) VALUES(%s,%s)", (user_id, username))
        db_connection.commit()
    types.ReplyKeyboardRemove()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "Izdarīt mājasdarbu", callback_data='md'))
    markup.add(types.InlineKeyboardButton("Instrukcija", callback_data='info'))
    markup.add(types.InlineKeyboardButton(
        "Nosūtīt ziņu", callback_data='about-md'))
    message1 = bot.send_message(
        message.chat.id, "Welcome to Ⓜ️ājasDarba bot🤖\n\nNospiediet uz pogu instrukcija lai uzzinātu vairāk\n\nJūsu ātrākais palīgs🏎", reply_markup=markup).message_id


@bot.message_handler(content_types="text")
def message_reply(message):
    global ready
    global message1

    # aboutmd
    if ready == 6:
        for i in teachers:
            bot.forward_message(
                chat_id=i, from_chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)
        ready = 0
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙", callback_data='back'))
        message1 = bot.edit_message_text(
            f"Jūsu ziņojums ir nosūtīts", reply_markup=markup, chat_id=message.chat.id, message_id=message1.message_id)
    elif message.text == "Nē":
        message_reply_start(message)
    elif ready == 69:
        pay(message)
    # submit
    elif ready == 4:
        global a3
        ready = 0
        db_object.execute(f"SELECT order_number FROM pasutijums")
        result = db_object.fetchall()
        users = []
        for user in result:
            b0 = str(user)
            b1 = b0.replace("(", "")
            b2 = b1.replace(")", "")
            b3 = b2.replace(",", "")
            users.append(b3)
        if message.text in users:
            db_object.execute(
                f"SELECT id FROM pasutijums WHERE order_number = '{message.text}'")
            result = db_object.fetchone()
            a0 = str(result)
            a1 = a0.replace("(", "")
            a2 = a1.replace(")", "")
            a3 = a2.replace(",", "")
            ready = 5
            bot.send_message(message.chat.id, f'Send work')
        else:
            submit(message)
    # done
    elif ready == 3:
        ready = 0
        db_object.execute(f"SELECT order_number FROM pasutijums")
        result = db_object.fetchall()
        users = []
        for user in result:
            b0 = str(user)
            b1 = b0.replace("(", "")
            b2 = b1.replace(")", "")
            b3 = b2.replace(",", "")
            users.append(b3)
        if message.text in users:
            db_object.execute(
                f"DELETE FROM pasutijums WHERE order_number = '{message.text}'")
            db_connection.commit()
            bot.send_message(
                message.chat.id, f'Pasūtījums ir izpildīts un noņemts')
        else:
            done(message)

    # accept
    elif ready == 2:
        ready = 0
        db_object.execute(f"SELECT order_number FROM pasutijums")
        result = db_object.fetchall()
        users = []
        for user in result:
            b0 = str(user)
            b1 = b0.replace("(", "")
            b2 = b1.replace(")", "")
            b3 = b2.replace(",", "")
            users.append(b3)
        if message.text in users:
            global order
            order = message.text
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Yes", callback_data='yes'))
            markup.add(types.InlineKeyboardButton("No", callback_data='no'))
            markup.add(types.InlineKeyboardButton(
                "Back", callback_data='back'))
            message1 = bot.send_message(
                message.chat.id, f'Izvēlieties', reply_markup=markup, parse_mode='html')
        else:
            accept(message)

    elif ready == 1:
        kommentari(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global message1
    global order
    global money
    global client_id
    global ready
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Jā")
    item2 = types.KeyboardButton("Nē")
    markup.add(item1, item2)

    if call.data == "md":
        md(call)
    elif call.data == "back":
        start(call)
    elif call.data == "info":
        info(call)
    elif call.data == "about-md":
        aboutmd(call)

    elif call.data == "5":
        money = 500
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)
    elif call.data == "10":
        money = 1000
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)
    elif call.data == "15":
        money = 1500
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)
    elif call.data == "20":
        money = 2000
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)
    elif call.data == "25":
        money = 2500
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)
    elif call.data == "30":
        money = 3000
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)
    elif call.data == "35":
        money = 3500
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)
    elif call.data == "40":
        money = 4000
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)
    elif call.data == "50":
        money = 5000
        ready = 69
        bot.send_message(client_id, 'Apstiprinājums', reply_markup=markup)

    elif call.data == "no":
        db_object.execute(
            f"SELECT id FROM pasutijums WHERE order_number = '{order}'")
        result = db_object.fetchone()
        b0 = str(result)
        b1 = b0.replace("(", "")
        b2 = b1.replace(")", "")
        b3 = b2.replace(",", "")
        bot.send_message(b3, f'Jūsu pasūtījums ir noraidīts')
        bot.send_message(call.message.chat.id,
                         f'Order {order} of user {b3} has been declined')
        db_object.execute(
            f"DELETE FROM pasutijums WHERE order_number = '{order}'")
        db_connection.commit()
    elif call.data == "yes":
        db_object.execute(
            f"SELECT id FROM pasutijums WHERE order_number = '{order}'")
        result = db_object.fetchone()
        b0 = str(result)
        b1 = b0.replace("(", "")
        b2 = b1.replace(")", "")
        b3 = b2.replace(",", "")
        bot.send_message(
            b3, f'Jūsu pasūtījums ir pieņemts. Lūdzu, samaksājiet par pakalpojumu, izmantojot komandu /buy')
        bot.send_message(call.message.chat.id,
                         f'Order {order} of user {b3} has been approved')


ready = 0
message1 = 0
order = 0
a3 = 0
money = 500
client_id = 0
# bot.polling(none_stop=True)
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

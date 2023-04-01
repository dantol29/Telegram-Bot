import psycopg2
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import random

#
admin_chat_id = [843373640, 76683384, 1747614551, 732337421]

DB_URI = "postgres://thstmare:zIduxHeDd2nvkzBd5slGF6MwPz8tTAce@mouse.db.elephantsql.com/thstmare"
db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

API_TOKEN = '5868782166:AAGWhXR2NLw13p1K0tE8Yln3cmZ3ieRivS4'
WEBHOOK_HOST = 'https://victoria-school-app.herokuapp.com/'


dp = Bot(API_TOKEN)
bot = Dispatcher(dp)


async def on_startup(bot):
    await dp.set_webhook(WEBHOOK_HOST)


async def on_shutdown(bot):
    await dp.delete_webhook()


async def menu(message: types.Message):
    global status
    status = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Anonīma sūdzība✉️")
    item2 = types.KeyboardButton("Noteikumi🦉")
    item3 = types.KeyboardButton("Idejas💡")
    item4 = types.KeyboardButton("Ziņot par situāciju🚨")
    markup.add(item1, item2, item3, item4)
    await message.answer("Izvēlieties vienu no manām komandām🤖", reply_markup=markup, parse_mode='html')


@bot.message_handler(chat_id=[843373640, 76683384, 1747614551, 732337421], commands=['admin'])
async def admin(message: types.Message):
    await message.answer("1./visiem - rakstīt ziņu visiem\n2. /users - lietotāju skaits\n3. /answer - atbildēt\n4. /sms - visi sms")


@bot.message_handler(commands=['admin'])
async def admin(message: types.Message):
    await message.answer("You cannot use this")


@bot.message_handler(chat_id=[843373640, 76683384, 1747614551, 732337421], commands=['visiem'])
async def gossip(message: types.Message):
    global status
    status = 666
    await message.answer("Rakstiet ziņu")


@bot.message_handler(commands=['visiem'])
async def gossip(message: types.Message):
    await message.answer("You cannot use this")


@bot.message_handler(chat_id=[843373640, 76683384, 1747614551, 732337421], commands=['sms'])
async def sms(message: types.Message):
    db_object.execute(f"SELECT message_id, username, body FROM sms3")
    result = db_object.fetchall()
    for i in result:
        await message.answer(i)


@bot.message_handler(commands=['sms'])
async def sms(message: types.Message):
    await message.answer("You cannot use this")


@bot.message_handler(chat_id=[843373640, 76683384, 1747614551, 732337421], commands=['answer'])
async def answer(message: types.Message):
    global status
    status = 555
    await message.answer("Rakstiet ziņas numuru")


async def answer2(message: types.Message):
    global status
    status = 444
    await message.answer("Rakstiet atbildi")


@bot.message_handler(commands=['answer'])
async def answer(message: types.Message):
    await message.answer("You cannot use this")


@bot.message_handler(chat_id=[843373640, 76683384, 1747614551, 732337421], commands=['users'])
async def users(message: types.Message):
    db_object.execute(f"SELECT * FROM users ")
    result = db_object.fetchall()
    # for row in result:
    #  bot.send_message(
    #     message.chat.id, f"{row}\n")
    await message.answer(f"User count:  {len(result)}")


@bot.message_handler(commands=['users'])
async def users(message: types.Message):
    await message.answer("You cannot use this")


@bot.message_handler(commands=['chatid'])
async def chat_id(message: types.Message):
    chatid = message.chat.id
    await message.answer(f"Chat id: {chatid}")


@bot.message_handler(commands=['start'])
async def start_reply(message: types.Message):
    global status

    status = 0
    user_id = message.from_user.id
    username = message.from_user.first_name
    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()
    if not result:
        db_object.execute(
            "INSERT INTO users(id, name) VALUES(%s,%s)", (user_id, username))
        db_connection.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Anonīma sūdzība✉️")
    item2 = types.KeyboardButton("Idejas💡")
    item3 = types.KeyboardButton("Noteikumi🦉")
    item4 = types.KeyboardButton("Ziņot par situāciju🚨")
    markup.add(item1, item2, item3, item4)
    await message.answer("""Laipni lūdzam <b>Profesionālās vidusskolas "Victoria"</b> bota🤖\nIzvēlies vienu no pogām""", reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types="text")
async def message_reply(message: types.Message):
    global status
    global result
    global message_delete
    # sudziba
    if message.text == "Anonīma sūdzība✉️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Atpakaļ")
        markup.add(item1)
        await message.answer("Uzrakstiet savu sūdzību✉️",
                             reply_markup=markup, parse_mode='html')
        status = 1
    # atpkal menu
    elif message.text == "Atpakaļ":
        await menu(message)
    # rakstit visiem

    elif status == 666:
        status = 0
        db_object.execute(f"SELECT id FROM users")
        result = db_object.fetchall()
        for user in result:
            b0 = str(user)
            b1 = b0.replace("(", "")
            b2 = b1.replace(")", "")
            b3 = b2.replace(",", "")
            await message.answer(chat_id=b3, text=f"{message.text}")

    elif status == 555:
        message_delete = message.text
        status = 0
        db_object.execute(
            f"SELECT message_id FROM sms3 WHERE message_id = '{message.text}'")
        result = db_object.fetchone()
        if not result:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Atpakaļ")
            markup.add(item1)
            await message.answer("Numurs nav atrāsts",
                                 reply_markup=markup, parse_mode='html')
            await answer(message)
        else:
            db_object.execute(
                f"SELECT id FROM sms3 WHERE message_id = '{message.text}'")
            result = db_object.fetchone()
            await answer2(message)
            b0 = str(result)
            b1 = b0.replace("(", "")
            b2 = b1.replace(")", "")
            result = b2.replace(",", "")

    elif status == 444:
        print(result)
        await dp.send_message(chat_id=result, text=f"Atbilde: {message.text}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Atpakaļ")
        markup.add(item1)
        await message.answer("Ziņa ir nosūtīta",
                             reply_markup=markup, parse_mode='html')
        db_object.execute(
            f"DELETE FROM sms3 WHERE message_id = '{message_delete}'")
        db_connection.commit()
    # admin
    elif message.text == "ADMIN🦉":
        await admin(message)
    # idejas
    elif message.text == "Idejas💡":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Atpakaļ")
        markup.add(item1)
        await message.answer("Uzrakstiet savu ideju💡",
                             reply_markup=markup, parse_mode='html')
        status = 1
    # noteikumi
    elif message.text == "Noteikumi🦉":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Atpakaļ")
        markup.add(item1)
        await message.answer("1. Nelieto lamuvārdus", reply_markup=markup)
        status = 0
    # situacija
    elif message.text == "Ziņot par situāciju🚨":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Atpakaļ")
        markup.add(item1)
        await message.answer("Uzrakstiet par situāciju🚨",
                             reply_markup=markup)
        status = 1
    #    paldies zina ir nosutita un atpakal
    elif status == 1:
        if len(message.text) > 7:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Atpakaļ")
            markup.add(item1)
            await message.answer("Paldies! Jūsu ziņa ir nosūtīta!🦉", reply_markup=markup)
            status = 0
            message_id = str(random.randrange(1001, 9999))
            db_object.execute(
                "INSERT INTO sms3(message_id, username, id, body) VALUES(%s,%s,%s,%s)", (str(message_id), message.from_user.first_name, message.chat.id, message.text))
            db_connection.commit()
            for i in admin_chat_id:
                await dp.forward_message(
                    chat_id=i, from_chat_id=message.chat.id, message_id=message.message_id)
                await dp.send_message(chat_id=i, text=f"{message_id}")
        else:
            await message.answer("Man tas nepatīk!")
            await menu(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Atpakaļ")
        markup.add(item1)
        await message.answer("Es nesaprotu..", reply_markup=markup)
        status = 0


status = 0
executor.start_webhook(
    dispatcher=bot,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="0.0.0.0",
    port=int(os.environ.get('PORT', 5000))
)

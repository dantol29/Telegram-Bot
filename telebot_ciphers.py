import telebot
from telebot import types
import requests

bot = telebot.TeleBot('')
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '/']
alphabet_2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '/']
opposite = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a', '/']

@bot.message_handler(commands=['start'])
def menu(message):  
 markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
 item1=types.KeyboardButton("Атбаш")
 item2=types.KeyboardButton("Кодовое слово")
 item3=types.KeyboardButton("Шифр Цезаря")
 item4=types.KeyboardButton("Шифр Плейфера")
 item5=types.KeyboardButton("XOR")
 markup.add(item1, item2, item3, item4, item5)
 bot.send_message(message.chat.id,'Выбери тип шифра',reply_markup=markup)

def word_code(message):  
 markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
 item1=types.KeyboardButton("Шифровка")
 item2=types.KeyboardButton("Расшифровка")
 markup.add(item1, item2)
 bot.send_message(message.chat.id,'Выберите тип',reply_markup=markup)


@bot.message_handler(content_types="text")
def cipher(message):
   global ready
   global ready_2
   global ready_2_1
   global ready_2_2
   global secret_word
   global codeword_3
   global codeword_2
   global codeword
   global cesar_number
   global cesar_ready
   global playfer_word
   global playfer_ready
   global secret_word
   global p
   global XOR_ready
   global res

   #Шифровка Атбаш
   if message.text == "Атбаш":
    bot.send_message(message.chat.id, "Введите слово")
    ready = 1
   elif ready == 1:
    codeword = message.text.lower()
    x_1 = []
    for letter in codeword:
     if letter != ' ':
      x_1.append(letter)
     else:
      x_1.append('/')  
    y_1 = []
    k_1 = 0
    for k in range(0, len(x_1)):
     for i in range(0, len(alphabet_2)):
      if x_1[k_1] == alphabet_2[i]:
       k_1 = k_1 + 1
       y_1.append(opposite[i])
       break
    answer_1 = ''.join(y_1)
    final_answer_1 = answer_1.replace('/', ' ')
    bot.send_message(message.chat.id, final_answer_1)
    ready = 0
    menu(message)


   elif message.text == "Кодовое слово":
    ready_2 = 1
    bot.send_message(message.chat.id, "Введите кодовое слово")
   elif ready_2 == 1:
    codeword_2 = message.text.lower()
    codeword_3 = message.text.lower()
    ready_2 = 2
    word_code(message)

   #Шифровка с кодовым словом 
   elif ready_2 == 2 and message.text == "Шифровка":
    secret_word = []
    for letter in codeword_3:
     secret_word.append(letter)
    for i in range(0, len(secret_word)):
     for k in range(0, len(alphabet)):
      if secret_word[i] == alphabet[k]:
       del alphabet[k]
       break
    h = 0
    for letter in alphabet:
     secret_word.append(alphabet[h])
     h += 1
    bot.send_message(message.chat.id, "Введите слово")
    ready_2_1 = 3

   elif ready_2_1 == 3:
    x_1 = []
    for letter in message.text.lower():
     if letter != ' ':
      x_1.append(letter)
     else:
      x_1.append('/')  
    y_1 = []
    for k in range(0, len(x_1)):
     for i in range(0, len(alphabet_2)):
      if x_1[k] == alphabet_2[i]:
       y_1.append(secret_word[i])
       break
    answer_1 = ''.join(y_1)
    final_answer_1 = answer_1.replace('/', ' ')
    bot.send_message(message.chat.id, final_answer_1)
    ready_2_1 = 0
    ready_2 = 0
    secret_word.clear()
    menu(message)
   


   #Расшифровка с кодовым словом
   elif ready_2 == 2 and message.text == "Расшифровка":
    secret_word = []
    for letter in codeword_2:
     secret_word.append(letter)

    for i in range(0, len(secret_word)):
     for k in range(0, len(alphabet)):
      if secret_word[i] == alphabet[k]:
       del alphabet[k]
       break
    h = 0
    for letter in alphabet:
     secret_word.append(alphabet[h])
     h += 1
    bot.send_message(message.chat.id, "Введите слово")
    ready_2_2 = 3
   elif ready_2_2 == 3:
    x_1 = []
    for letter in message.text.lower():
     if letter != ' ':
      x_1.append(letter)
     else:
      x_1.append('/')  
    y_1 = []
    for k in range(0, len(x_1)):
     for i in range(0, len(alphabet_2)):
      if x_1[k] == secret_word[i]:
       y_1.append(alphabet_2[i])
       break
    answer_1 = ''.join(y_1)
    final_answer_1 = answer_1.replace('/', ' ')
    bot.send_message(message.chat.id, final_answer_1)
    ready_2_2 = 0
    ready_2 = 0
    secret_word.clear()
    menu(message)



   #Шифр Цезаря
   elif message.text == "Шифр Цезаря":
    bot.send_message(message.chat.id, "Enter a number!")
    cesar_ready = 1
   elif cesar_ready == 1:
    cesar_ready = 2
    number = message.text.lower()
    cesar_number = int(number)
    word_code(message)
   elif cesar_ready == 2 and message.text == "Шифровка":
    bot.send_message(message.chat.id, "Write your message!")
    cesar_ready = 3
   elif cesar_ready == 3:
    x_1 = []
    for letter in message.text.lower():
     if letter != ' ':
      x_1.append(letter)
     else:
      x_1.append('/')  
    y_1 = []
    for k in range(0, len(x_1)):
     for i in range(0, len(alphabet_2)):
      if x_1[k] == alphabet_2[i]:
       if x_1[k] == '/':
         y_1.append('/')
         break
       elif (i+cesar_number) > 27:
        y_1.append(alphabet_2[(i+cesar_number)-26])
        break
       else:
        y_1.append(alphabet_2[i+cesar_number])
        break
    answer_1 = ''.join(y_1)
    final_answer_1 = answer_1.replace('/', ' ')
    bot.send_message(message.chat.id, final_answer_1)
    cesar_ready = 0
    menu(message)

   #Расшифровка
   elif cesar_ready == 2 and message.text == "Расшифровка":
    bot.send_message(message.chat.id, "Write your message!")
    cesar_ready = 4
   elif cesar_ready == 4:
    x_1 = []
    for letter in message.text.lower():
     if letter != ' ':
      x_1.append(letter)
     else:
      x_1.append('/') 
    y_1 = []
    for k in range(0, len(x_1)):
     for i in range(0, len(alphabet_2)):
      if x_1[k] == alphabet_2[i]:
       if x_1[k] == '/':
         y_1.append('/')
         break
       elif (i+cesar_number) > 27:
        y_1.append(alphabet_2[(i-cesar_number)-26])
        break
       else:
        y_1.append(alphabet_2[i-cesar_number])
        break
    answer_1 = ''.join(y_1)
    final_answer_1 = answer_1.replace('/', ' ')
    bot.send_message(message.chat.id, final_answer_1)
    cesar_ready = 0
    menu(message)

   #Шифр Плейфера
   elif message.text == "Шифр Плейфера":
    bot.send_message(message.chat.id, "Введите кодовое слово!")
    playfer_ready = 1
   elif playfer_ready == 1:
    p = [[1, 2, 3, 4 ,5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [5, 6, 7, 8, 9]]
    playfer_word = message.text
    secret_word = []
    for letter in playfer_word:
     secret_word.append(letter)
    for i in range(0, len(secret_word)):
     for k in range(0, len(alphabet)):
      if secret_word[i] == alphabet[k]:
       del alphabet[k]
       break
    h = 0
    for letter in alphabet:
     secret_word.append(alphabet[h])
     h += 1
    p[0] = secret_word[:5]
    p[1] = secret_word[5:10]
    p[2] = secret_word[10:15]
    p[3] = secret_word[15:20]
    p[4] = secret_word[20:25]
    word_code(message)
    playfer_ready = 2
   elif playfer_ready == 2 and message.text == "Шифровка":
    bot.send_message(message.chat.id, "Введите слово!")
    playfer_ready = 3
   elif playfer_ready == 2 and message.text == "Расшифровка":
    bot.send_message(message.chat.id, "Введите слово!")
    playfer_ready = 4
   elif playfer_ready == 4:
    x_1 = []
    pre_x = []
    word = message.text.lower()
    word.strip()
    for letter in word:
     if letter != ' ':
      pre_x.append(letter)
      if len(pre_x) == 2:
       print(pre_x)
       x_1.append(pre_x[0:])
       pre_x.clear() 
    bigramm = []
    for i in range(0, len(x_1)):
     answer_1 = ''.join(x_1[i])
     bigramm.append(answer_1) 
    string_convert = ''.join(bigramm)
    final_list = []
    for letter in string_convert:
     final_list.append(letter)
    print(final_list)
    letter_index = []
    for k in range(0, len(final_list)):
     for u in range(0, 5):
      for i in range (0, 5):
       if p[u][i] == final_list[k]:
        index_letter_row = u
        index_letter_column = i
        letter_index.append(index_letter_row)
        letter_index.append(index_letter_column)
        break
    print(letter_index)
    print(p)
    length = len(letter_index) // 4
    print(length)
    a = 0
    b = 3
    c = 2
    d = 1
    answer_print = []
    for i in range(0, length):
      if letter_index[a] == letter_index[c]:
       x = letter_index[d] - 1
       y = letter_index[b] - 1
       if x == 5:
        x = x + 5
       elif y == 5:
        y = y + 5
       answer_print.append(p[letter_index[a]][x])
       answer_print.append(p[letter_index[c]][y])
       a += 4
       b += 4
       c += 4
       d += 4
      elif letter_index[d] == letter_index[b]:
       x = letter_index[a] - 1
       y = letter_index[c] - 1
       if x == 5:
        x = x + 5
       elif y == 5:
        y = y + 5
       answer_print.append(p[x][letter_index[d]])
       answer_print.append(p[y][letter_index[b]])
       a += 4
       b += 4
       c += 4
       d += 4
      else:
       answer_print.append(p[letter_index[a]][letter_index[b]])
       answer_print.append(p[letter_index[c]][letter_index[d]])
       a += 4
       b += 4
       c += 4
       d += 4
    x_2 = ''.join(answer_print) 
    bot.send_message(message.chat.id, f"{x_2},4")
    menu(message)
   elif playfer_ready == 3:
    x_1 = []
    pre_x = []
    word = message.text.lower()
    word.strip()
    for i in range(0, len(word)):
     if word[i-1] == word[i]:
      word = word[:i] + "x" + word[i:]
    for letter in word:
     if letter != ' ':
      pre_x.append(letter)
      if len(pre_x) == 2:
       print(pre_x)
       x_1.append(pre_x[0:])
       pre_x.clear()
     else:
      x_1.append('/')
      x_1.remove('/') 
    bigramm = []
    for i in range(0, len(x_1)):
     answer_1 = ''.join(x_1[i])
     bigramm.append(answer_1) 
    string_convert = ''.join(bigramm)
    final_list = []
    for letter in string_convert:
     final_list.append(letter)
    print(final_list)
    letter_index = []
    for k in range(0, len(final_list)):
     for u in range(0, 5):
      for i in range (0, 5):
       if p[u][i] == final_list[k]:
        index_letter_row = u
        index_letter_column = i
        letter_index.append(index_letter_row)
        letter_index.append(index_letter_column)
        break
    print(letter_index)
    print(p)
    length = len(letter_index) // 4
    print(length)
    a = 0
    b = 3
    c = 2
    d = 1
    answer_print = []
    for i in range(0, length):
      if letter_index[a] == letter_index[c]:
       x = letter_index[d] + 1
       y = letter_index[b] + 1
       if x == 5:
        x = x - 5
       elif y == 5:
        y = y - 5
       answer_print.append(p[letter_index[a]][x])
       answer_print.append(p[letter_index[c]][y])
       a += 4
       b += 4
       c += 4
       d += 4
      elif letter_index[d] == letter_index[b]:
       x = letter_index[a] + 1
       y = letter_index[c] + 1
       if x == 5:
        x = x - 5
       elif y == 5:
        y = y - 5
       answer_print.append(p[x][letter_index[d]])
       answer_print.append(p[y][letter_index[b]])
       a += 4
       b += 4
       c += 4
       d += 4
      else:
       answer_print.append(p[letter_index[a]][letter_index[b]])
       answer_print.append(p[letter_index[c]][letter_index[d]])
       a += 4
       b += 4
       c += 4
       d += 4
    x_2 = ''.join(answer_print) 
    bot.send_message(message.chat.id, x_2)
    menu(message)
   #неправильный текст

   elif message.text == "XOR":
    bot.send_message(message.chat.id, "Введите кодовую букву!")
    XOR_ready = 1

   elif XOR_ready == 1:
    code_word = message.text
    res = ' '.join(format(ord(i), '08b') for i in code_word)
    
    bot.send_message(message.chat.id, "Введите сообщение!")
    XOR_ready = 2
    
   elif XOR_ready == 2:
    #Message transformation to binary
    test_str = message.text
    res2 = ' '.join(format(ord(x), '08b') for x in test_str)
    res2 = [i for i in res2.split()]
    

    #Binary code(XOR)
    answer = []
    answer2 = []
    for i in range(0, len(res2)):
     for k in range(0, len(res2[i])):
      x = int(res2[i][k]) ^ int(res[k])
      answer.append(str(x))
     answer2.append("".join(answer))
     answer.clear()
    s = ''.join(answer2)
    
    #From binary to string(Encrypted answer)
    #ascii_string = ""
    #for binary_value in answer2:
     #an_integer = int(binary_value, 2)
     #ascii_character = chr(an_integer)
     #print(ascii_character)
     #ascii_string += ascii_character
    bot.send_message(message.chat.id, f"Your message is {s}")

   else:
    bot.send_message(message.chat.id, "Не понимаю..")
    menu(message)

ready = 0
ready_2 = 0
ready_2_1 = 0
ready_2_2 = 0
codeword = ""
codeword_2 = ""
codeword_3 = ""
secret_word = []
cesar_ready = 0
cesar_number = 0
playfer_ready = 0
playfer_word = ""
secret_word = []
p = [[]]
#XOR:
XOR_ready = 0
res = 0

bot.polling(none_stop=True)

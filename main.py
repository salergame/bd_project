import telebot
from telebot import types
import psycopg2
conn=psycopg2.connect(host='localhost',
                      database='postgres',
                      user='postgres',
                      password='1234567')
cur=conn.cursor()
cur1=conn.cursor()

cur1.execute('SELECT role FROM Accounts')
cur.execute('SELECT Password FROM Accounts')
all_users = cur.fetchall()
all_user=cur1.fetchall()
gg = []
user_status={}
for i in all_users:
  gg.append(i[0])




TOKEN = '6392060028:AAEVRZLwG3yJk2hNoxPR5MiNQNpofxRhaRM'

bot = telebot.TeleBot(TOKEN)


bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("Задать вопрос")
    btn3=types.KeyboardButton("Зарегестрироваться")
    btn4=types.KeyboardButton("Вход")
    markup.add(btn1, btn2,btn3,btn4)
    bot.send_message(message.chat.id, text="Привет", reply_markup=markup)
def welcome(message):
    if message.text in gg:
      bot.send_message(message.chat.id, text="Вы авторизовались добро пожаловать")
    else:
      bot.send_message(message.chat.id, text="Пароль введен не правильно")


@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Поздороваться"):
        bot.send_message(message.chat.id, text="Привеет!)")
    elif(message.text == "Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как тебя зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    elif(message.text=="Зарегестрироваться"):
      bot.send_message(message.chat.id, text="Придумайте свои логин и пароль: ")
      bot.register_next_step_handler(message, welcome )
    elif(message.text=="Вход"):
      bot.send_message(message.chat.id, text="Кто вы: ")
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      bttn1 = types.KeyboardButton("Учитель")
      bttn2 = types.KeyboardButton("Ученик")
      bttn3=types.KeyboardButton("Админ")
      back1 = types.KeyboardButton("Вернуться в главное меню")
      markup.add(bttn1, bttn2,bttn3, back1)
      bot.send_message(message.chat.id, text="Идет проверка...", reply_markup=markup)
    elif message.text =="Учитель":
        bot.send_message(message.chat.id, text="Введите свои логин и пароль через запятую: ")
        bot.register_next_step_handler(message,welcome)
    elif message.text == "Ученик":
      bot.send_message(message.chat.id, text="Введите свои логин и пароль через запятую: ")
      bot.register_next_step_handler(message,welcome)  
    elif message.text == "Админ":
      bot.send_message(message.chat.id, text="Введите свои логин и пароль через запятую: ")
      bot.register_next_step_handler(message,welcome)
      
      


    elif(message.text == "Как тебя зовут?"):
        bot.send_message(message.chat.id, "Меня зовут Марат")
    
    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Поздороваться с читателями")
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button2 = types.KeyboardButton("Задать вопрос")
        button3 = types.KeyboardButton("Зарегестрироваться")
        button4= types.KeyboardButton("Вход")
        markup.add(button1, button2,button3,button4)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
# if message.text=="Учитель":
#         bot.send_message(message.chat.id, text="Введите свои учительский пароль: ")
#         bot.register_next_step_handler(message, welcome )
#       elif message.text=="Учитель":
#         bot.send_message(message.chat.id, text="Введите свои ученический пароль: ")
#         bot.register_next_step_handler(message, welcome )
#       elif message.text=="Админ":
#         bot.send_message(message.chat.id, text="Введите свои админский пароль: ")
#         bot.register_next_step_handler(message, welcome )
conn.commit()
if __name__ == '__main__':
    bot.infinity_polling()
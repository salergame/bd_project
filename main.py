import telebot
from telebot import types
import psycopg2

class MyTelegramBot:
    def __init__(self, token):
        self.token = token
        self.conn = psycopg2.connect(host='localhost',
                                     database='postgres',
                                     user='postgres',
                                     password='1234567')
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT Login, Password, role FROM Accounts')
        self.user_credentials = {row[0]: (row[1], row[2]) for row in self.cur.fetchall()}
        self.bot = telebot.TeleBot(self.token)
        self.authenticated_users = {}  # Словарь для отслеживания аутентификации

        self.question_handler = QuestionHandler(self.bot, self)
        self.student_handler = StudentHandler(self.bot, self)
        self.teacher_handler = TeacherHandler(self.bot, self)
        self.admin_handler = AdminHandler(self.bot, self)

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Поздороваться")
            btn2 = types.KeyboardButton("Задать вопрос")
            btn3 = types.KeyboardButton("Вход")
            markup.add(btn1, btn2, btn3)
            self.bot.send_message(message.chat.id, text="Привет", reply_markup=markup)

        @self.bot.message_handler(content_types=['text'])
        def handle_text(message):
            chat_id = message.chat.id

            if message.text == "Поздороваться":
                self.bot.send_message(chat_id, text="Здравствуйте")
            elif message.text == "Задать вопрос":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Как тебя зовут?")
                btn2 = types.KeyboardButton("Что ты можешь?")
                back = types.KeyboardButton("Вернуться в главное меню")
                markup.add(btn1, btn2, back)
                self.bot.send_message(chat_id, text="Задайте мне вопрос", reply_markup=markup)
            elif message.text == "Вход":
                if chat_id not in self.authenticated_users or not self.authenticated_users[chat_id]:
                    self.bot.send_message(chat_id, text="Введите свой логин и пароль через запятую: ")
                    self.bot.register_next_step_handler(message, self.authenticate)
                else:
                    role = self.user_credentials[self.authenticated_users[chat_id]][1]
                    if role == "Студент":
                        self.student_handler.handle_student_menu(message)
                    elif role == "Учитель":
                        self.teacher_handler.handle_teacher_menu(message)
                    elif role == "Админ":
                        self.admin_handler.handle_admin_menu(message)
            elif message.text == "Выход":
                if chat_id in self.authenticated_users:
                    self.authenticated_users.pop(chat_id, None)
                    self.bot.send_message(chat_id, text="Вы успешно вышли из аккаунта.")
                    # Можно добавить дополнительные действия при выходе, если необходимо
                    start(message)  # Возвращаемся в главное меню
            else:
                self.question_handler.handle_question(message)
                self.student_handler.handle_student(message)
                self.teacher_handler.handle_teacher(message)
                self.admin_handler.handle_admin(message)

        self.conn.commit()
        if __name__ == '__main__':
            self.bot.infinity_polling()

    def authenticate(self, message):
        chat_id = message.chat.id
        login, password = map(str.strip, message.text.split(','))

        if login in self.user_credentials and self.user_credentials[login][0] == password:
            self.authenticated_users[chat_id] = login  # Сохраняем логин пользователя
            role = self.user_credentials[login][1]
            self.bot.send_message(chat_id, text=f"Вы успешно вошли в свой аккаунт с ролью {role}. Добро пожаловать!")

            # После успешной аутентификации проверяем, является ли пользователь студентом
            if role == "Студент":
                self.student_handler.handle_student_menu(message)
            elif role == "Учитель":
                self.teacher_handler.handle_teacher_menu(message)
            elif role == "Админ":
                self.admin_handler.handle_admin_menu(message)

        else:
            self.authenticated_users[chat_id] = None  # Пользователь не прошел аутентификацию
            self.bot.send_message(chat_id, text="Ошибка входа. Пожалуйста, проверьте логин и пароль.")

class QuestionHandler:
    def __init__(self, bot, my_bot):
        self.bot = bot
        self.my_bot = my_bot

    def handle_question(self, message):
        if message.text == "Как тебя зовут?":
            self.bot.send_message(message.chat.id, "Меня зовут Марат")
        elif message.text == "Что ты можешь?":
            self.bot.send_message(message.chat.id, text="1. Поздороваться с пользователем ")
            self.bot.send_message(message.chat.id, text="2. Авторизовать ")
            self.bot.send_message(message.chat.id, text="3. Ответить на предложенные вопросы ")
            self.bot.send_message(message.chat.id, text="4. Выдать ошибку")
        elif message.text == "Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Поздороваться")
            button2 = types.KeyboardButton("Задать вопрос")
            button3 = types.KeyboardButton("Вход")
            markup.add(button1, button2, button3)
            self.bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
        else:
            self.bot.send_message(message.chat.id, text="На такую команду я не запрограммирована..")

class StudentHandler:
    def __init__(self, bot, my_bot):
        self.bot = bot
        self.my_bot = my_bot

    def handle_student(self, message):
        # Обработка команд для студента
        if message.text == "Посмотреть предметы":
            self.bot.send_message(message.chat.id, text="Список ваших предметов:")
            # Добавьте здесь логику для вывода предметов студента

    def handle_student_menu(self, message):
        # Показать меню для студента
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Посмотреть предметы")
        button2 = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, back)
        self.bot.send_message(message.chat.id, text="Добро пожаловать, студент!", reply_markup=markup)

class TeacherHandler:
    def __init__(self, bot, my_bot):
        self.bot = bot
        self.my_bot = my_bot

    def handle_teacher(self, message):
        # Обработка команд для учителя
        pass  # Добавьте здесь логику для команд учителя

    def handle_teacher_menu(self, message):
        # Показать меню для учителя
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Добавить оценку")
        button2 = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, back)
        self.bot.send_message(message.chat.id, text="Добро пожаловать, учитель!", reply_markup=markup)

class AdminHandler:
    def __init__(self, bot, my_bot):
        self.bot = bot
        self.my_bot = my_bot

    def handle_admin(self, message):
        # Обработка команд для администратора
        pass  # Добавьте здесь логику для команд администратора

    def handle_admin_menu(self, message):
        # Показать меню для администратора
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Добавить пользователя")
        button2 = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, back)
        self.bot.send_message(message.chat.id, text="Добро пожаловать, администратор!", reply_markup=markup)

if __name__ == '__main__':
    TOKEN = '6392060028:AAEVRZLwG3yJk2hNoxPR5MiNQNpofxRhaRM'
    my_bot = MyTelegramBot(TOKEN)
    my_bot.run()

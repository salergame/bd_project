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
        self.cur.execute('SELECT LOWER(Login), Password, role FROM Accounts')
        self.user_credentials = {row[0]: (row[1], row[2]) for row in self.cur.fetchall()}
        
        self.bot = telebot.TeleBot(self.token)
        
        self.authenticated_users = {}

        self.question_handler = QuestionHandler(self.bot, self)
        self.student_handler = StudentHandler(self.bot, self)
        self.teacher_handler = TeacherHandler(self.bot, self, self.cur)
        
        self.admin_handler = AdminHandler(self, self.cur, self.cur, self.cur,self.cur,self.cur)
        
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
                    start(message)
            else:
                if chat_id in self.authenticated_users:
                    role = self.user_credentials[self.authenticated_users[chat_id]][1]
                    if role == "Студент":
                        self.student_handler.handle_student(message)
                    elif role == "Учитель":
                        self.teacher_handler.handle_teacher(message)
                    elif role == "Админ":
                        self.admin_handler.handle_admin(message)

                self.question_handler.handle_question(message)

        self.conn.commit()
        if __name__ == '__main__':
            self.bot.infinity_polling()

    def authenticate(self, message):
        chat_id = message.chat.id
        login, password = map(str.strip, message.text.split(','))

        

        if login in self.user_credentials and self.user_credentials[login][0] == password:
            self.authenticated_users[chat_id] = login
            role = self.user_credentials[login][1]
            self.bot.send_message(chat_id, text=f"Вы успешно вошли в свой аккаунт с ролью {role}. Добро пожаловать!")

            if role == "Студент":
                self.student_handler.handle_student_menu(message)
            elif role == "Учитель":
                self.teacher_handler.handle_teacher_menu(message)
            elif role == "Админ":
                self.admin_handler.handle_admin_menu(message)

        else:
            self.authenticated_users[chat_id] = None
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

class StudentHandler:
    def __init__(self, bot, my_bot):
        self.bot = bot
        self.my_bot = my_bot

    def handle_student(self, message):
        if message.text == "Посмотреть предметы":
            self.bot.send_message(message.chat.id, text="Список ваших предметов:")

    def handle_student_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Посмотреть предметы")
        button2 = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, back)
        self.bot.send_message(message.chat.id, text="Добро пожаловать, студент!", reply_markup=markup)

class TeacherHandler:
    def __init__(self, bot, my_bot,cur3):
        self.bot = bot
        self.my_bot = my_bot
        self.cur3=cur3

    def handle_teacher(self, message):
        if message.text == 'Посмотреть журнал':
            query = "SELECT Students.name, Ratings.grade FROM Students LEFT JOIN Ratings ON Students.studentid = Ratings.ratingid;"
            
            self.cur3.execute(query)
            results = self.cur3.fetchall()

            if results:
                for row in results:
                    student_name, grade = row
                    self.bot.send_message(message.chat.id, f"{student_name}: {grade}")
            else:
                self.bot.send_message(message.chat.id, "Нет данных в журнале.")
        elif message.text == 'Изменить оценку':
            self.bot.send_message(message.chat.id, "Введите имя студента и новую оценку через запятую:")
            self.bot.register_next_step_handler(message, self.handle_change_grade)



    def handle_change_grade(self, message):
        try:
            student_name, new_grade = map(str.strip, message.text.split(','))
            
            update_query = "UPDATE Ratings SET grade = %s WHERE studentid = (SELECT studentid FROM Students WHERE name = %s) OR grade IS NULL;"
            self.cur3.execute(update_query, (new_grade, student_name))
            self.my_bot.conn.commit()
            self.bot.send_message(message.chat.id, f"Оценка для студента {student_name} успешно изменена на {new_grade}.")
        except:
            self.bot.send_message(message.chat.id, "Ошибка при изменении оценки. Пожалуйста, проверьте ввод.")

    def handle_teacher_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Посмотреть журнал")
        button3 = types.KeyboardButton("Изменить оценку")
        button2 = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, button3,back)
        self.bot.send_message(message.chat.id, text="Добро пожаловать, учитель!", reply_markup=markup)

class AdminHandler:
    def __init__(self, my_bot, cur1, cur2, cur3):
        self.my_bot = my_bot
        self.cur1 = cur1
        self.cur2 = cur2
        self.cur3 = cur3
        self.delete_query = "DELETE FROM Accounts WHERE Login = %s RETURNING role, accountsid;"

    def handle_admin(self, message):
        if message.text == 'Добавить пользователя':
            self.my_bot.bot.send_message(message.chat.id, text='Введите логин, пароль и роль пользователя через запятую')
            self.my_bot.bot.register_next_step_handler(message, self.add_user)
        elif message.text == 'Удалить пользователя':
            self.my_bot.bot.send_message(message.chat.id, text='Введите логин пользователя, которого хотите удалить:')
            self.my_bot.bot.register_next_step_handler(message, self.remove_user)

    def add_user(self, message):
        try:
            login, password, role = map(str.strip, message.text.split(','))
            self.cur1.execute(
                'INSERT INTO Accounts (login, password, role) VALUES (%s, %s, %s) RETURNING accountsid;', (login, password, role))
            accounts_id = self.cur1.fetchone()[0]

            if role == 'Студент' or role == 'Учитель':
                self.my_bot.bot.send_message(message.chat.id, text='Введите имя, фамилию и дату рождения через запятую')
                self.my_bot.bot.register_next_step_handler(message, lambda m: self.add_user_data(m, accounts_id, role))
            else:
                self.my_bot.conn.commit()
                self.my_bot.bot.send_message(message.chat.id, text=f'Пользователь {login} успешно добавлен в базу данных.')

        except:
            self.my_bot.conn.rollback()
            self.my_bot.bot.send_message(message.chat.id, text=f'Ошибка при добавлении пользователя')

    def add_user_data(self, message, accounts_id, role):
        try:
            name, surname, date_of_birth = map(str.strip, message.text.split(','))

            if role == 'Студент':
                self.cur2.execute(
                    'INSERT INTO Students (name, surname, dateofbirth, accountsid) VALUES (%s, %s, %s, %s);',
                    (name, surname, date_of_birth, accounts_id))
            elif role == 'Учитель':
                self.cur3.execute(
                    'INSERT INTO Teachers (name, surname, dateofbirth, accountsid) VALUES (%s, %s, %s, %s);',
                    (name, surname, date_of_birth, accounts_id))

            self.my_bot.conn.commit()
            self.my_bot.bot.send_message(message.chat.id, text=f'Пользователь {name} {surname} успешно добавлен в базу данных.')
        except:
            self.my_bot.conn.rollback()
            self.my_bot.bot.send_message(message.chat.id, text=f'Ошибка при добавлении пользователя')

    def remove_user(self, message):
        try:
            login = message.text.strip()
            result = self.cur2.execute(self.delete_query, (login,))
            result = self.cur2.fetchone()
            if result:
                role, accounts_id = result
                if role == 'Студент':
                    self.cur2.execute('DELETE FROM Students WHERE accountsid = %s;', (accounts_id,))
                elif role == 'Учитель':
                    self.cur3.execute('DELETE FROM Teachers WHERE accountsid = %s;', (accounts_id,))

                self.my_bot.conn.commit()
                self.my_bot.bot.send_message(message.chat.id, text=f'Пользователь {login} успешно удален из базы данных')
            else:
                self.my_bot.bot.send_message(message.chat.id, text=f'Пользователь {login} не найден')
        except:
            self.my_bot.bot.send_message(message.chat.id, text=f'Ошибка при удалении пользователя')

    def handle_admin_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Добавить пользователя")
        button2 = types.KeyboardButton("Удалить пользователя")
        button_exit = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, button_exit, back)
        self.my_bot.bot.send_message(message.chat.id, text="Добро пожаловать, администратор!", reply_markup=markup)

if __name__ == '__main__':
    TOKEN = '6392060028:AAEVRZLwG3yJk2hNoxPR5MiNQNpofxRhaRM'
    my_bot = MyTelegramBot(TOKEN)
    my_bot.run()

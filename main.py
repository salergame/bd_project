import telebot
from telebot import types
import psycopg2
import datetime

class MyTelegramBot:
    def __init__(self, token):
        self.token = token
        self.conn = psycopg2.connect(host='localhost',
                                     database='postgres',
                                     user='postgres',
                                     password='1234567')
        self.cur = self.conn.cursor()
        self.cur1 = self.conn.cursor()
        self.cur2 = self.conn.cursor()
        self.cur3 = self.conn.cursor()
        self.cur4 = self.conn.cursor()

        self.cur.execute('SELECT LOWER(Login), Password, role FROM Accounts')
        self.user_credentials = {row[0]: (row[1], row[2]) for row in self.cur.fetchall()}

        self.bot = telebot.TeleBot(self.token)

        self.authenticated_users = {}

        self.question_handler = QuestionHandler(self.bot, self)
        self.student_handler = StudentHandler(self.bot, self,self.cur,self.cur)
        self.teacher_handler = TeacherHandler(self.bot, self, self.cur, self.cur)
        self.admin_handler = AdminHandler(self, self.cur1, self.cur2, self.cur3, self.cur4)

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
                        if chat_id not in self.student_handler.student_info:
                            self.student_handler.handle_student_menu(message)
                        else:
                            self.student_handler.handle_student_menu(message)
                    elif role == "Учитель":
                        if chat_id not in self.teacher_handler.subject_info:
                            self.teacher_handler.handle_teacher_menu(message)
                        else:
                            subject_id = self.teacher_handler.subject_info[chat_id]
                            self.teacher_handler.handle_teacher_menu(message, subject_id)
                    elif role == "Админ":
                        self.admin_handler.handle_admin_menu(message)

            elif message.text == "Выход":
                if chat_id in self.authenticated_users:
                    role = self.user_credentials[self.authenticated_users[chat_id]][1]
                    if role == "Студент":
                        self.student_handler.student_info.pop(chat_id, None)
                    elif role == "Учитель":
                        self.teacher_handler.subject_info.pop(chat_id, None)
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

        login_lower = login.lower()

        if login_lower in self.user_credentials and self.user_credentials[login_lower][0] == password:
            self.authenticated_users[chat_id] = login_lower
            role = self.user_credentials[login_lower][1]

            if role == "Студент":
                self.student_handler.handle_student_menu(message)
            elif role == "Учитель":
                teacher_id, subject_id, subject_name = self.get_teacher_info(login_lower)
                self.bot.send_message(chat_id, text=f"Вы успешно вошли в свой аккаунт с ролью {role}.")
                self.teacher_handler.handle_teacher_menu(message, subject_id)
            elif role == "Админ":
                self.admin_handler.handle_admin_menu(message)

            if login_lower in self.user_credentials:
                self.authenticated_users[chat_id] = login_lower
                role = self.user_credentials[login_lower][1]

                if role == "Студент":
                    self.student_handler.handle_student_menu(message)
                elif role == "Учитель":
                    teacher_id, subject_id, subject_name = self.get_teacher_info(login_lower)
                    self.bot.send_message(chat_id, text=f"Вы успешно вошли в свой аккаунт с ролью {role}.")
                    self.teacher_handler.handle_teacher_menu(message, subject_id)
                elif role == "Админ":
                    self.admin_handler.handle_admin_menu(message)
            else:
                self.authenticated_users[chat_id] = None
                self.bot.send_message(chat_id, text="Ошибка входа. Пожалуйста, проверьте логин и пароль.")
    def get_teacher_info(self, login):
        query = """
            SELECT Teachers.TeacherID, Items.ItemID, Items.ItemName
            FROM Teachers
            JOIN Items ON Teachers.ItemID = Items.ItemID
            JOIN Accounts ON Teachers.AccountsID = Accounts.AccountsID
            WHERE Accounts.Login = %s;
        """
        self.cur.execute(query, (login,))
        result = self.cur.fetchone()
        if result:
            teacher_id, subject_id, subject_name = result
            return teacher_id, subject_id, subject_name
        else:
            return None, None, None


class QuestionHandler:
    def __init__(self,bot, my_bot):
        self.bot = bot
        self.my_bot = my_bot

    def handle_question(self, message):
        if message.text == "Как тебя зовут?":
            self.bot.send_message(message.chat.id, "Меня зовут Марат")
        elif message.text == "Что ты можешь?":
            self.bot.send_message(message.chat.id, text="В зависемости от вашей роли")

        elif message.text == "Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Поздороваться")
            button2 = types.KeyboardButton("Задать вопрос")
            button3 = types.KeyboardButton("Вход")
            markup.add(button1, button2, button3)
            self.bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

class StudentHandler:
    def __init__(self, bot, my_bot,cur,cur1):
        self.bot = bot
        self.my_bot = my_bot
        self.cur=cur
        self.cur1=cur1
        self.student_info = {}

    def handle_student(self, message):
        if message.text == "Список книг библиотеки университета":
            books = self.get_books_from_library()
            if books:
                book_list_str = "\n".join([f"{book[1]} - {book[2]}" for book in books])
                self.bot.send_message(message.chat.id, text=f"Список книг в библиотеке:\n{book_list_str}")
            else:
                self.bot.send_message(message.chat.id, text="В библиотеке нет доступных книг.")
        elif message.text == "Посмотреть расписание":
            self.bot.send_message(message.chat.id, text="Введите ID вашей группы:")
            self.bot.register_next_step_handler(message, self.handle_enter_group_id)
        elif message.text == "Посмотреть даты тестов":
            query = "SELECT Tests.testdate, Items.itemname FROM Tests " \
                        "LEFT JOIN Items ON Tests.itemid = Items.itemid "

            self.cur.execute(query)
            results = self.cur.fetchall()

            if results:
                for row in results:
                    test_date, itemname = row
                    self.bot.send_message(message.chat.id, f"{test_date}: {itemname}")
            else:
                self.bot.send_message(message.chat.id, "Нет данных насчет тестов.")
        elif message.text == "Посмотреть даты экзаменов":
            query1 = "SELECT Exams.examdate, Items.itemname FROM Exams " \
                        "LEFT JOIN Items ON Exams.itemid = Items.itemid "

            self.cur1.execute(query1)
            results1 = self.cur1.fetchall()

            if results1:
                for row1 in results1:
                    exam_date, itemname = row1
                    self.bot.send_message(message.chat.id, f"{exam_date}: {itemname}")
            else:
                self.bot.send_message(message.chat.id, "Нет данных насчет экзаменов.")

    
    def handle_enter_group_id(self, message):
        try:
            group_id = int(message.text.strip())
            # Здесь можно провести дополнительные проверки, например, существование группы и принадлежность студента к ней

            # Запрос для получения расписания по группе
            query_schedule = "SELECT cs.DayOfWeek, cs.StartTime, cs.EndTime, i.itemname, a.audiencenumber " \
                             "FROM ClassSchedule cs " \
                             "JOIN Items i ON cs.ItemID = i.ItemID " \
                             "JOIN Audience a ON cs.AudienceID = a.AudienceID " \
                             "WHERE cs.groupsid = %s;"

            self.cur.execute(query_schedule, (group_id,))
            schedule_results = self.cur.fetchall()

            if schedule_results:
                schedule_str = "\n".join([f"{row[0]}, {row[1]} - {row[2]}, {row[3]}, {row[4]}" for row in schedule_results])
                self.bot.send_message(message.chat.id, text=f"Расписание для вашей группы:\n{schedule_str}")
            else:
                self.bot.send_message(message.chat.id, text="Нет доступного расписания для вашей группы.")
        except ValueError:
            self.bot.send_message(message.chat.id, text="Введите корректный ID группы (целое число).")
    def get_books_from_library(self):
        query = "SELECT BookID, BookTitle, Author FROM Library"
        self.my_bot.cur.execute(query)
        books = self.my_bot.cur.fetchall()
        return books

    def handle_student_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Посмотреть рассписание")
        button2 = types.KeyboardButton("Список книг библиотеки университета")
        button3=types.KeyboardButton("Посмотреть даты тестов")
        button4=types.KeyboardButton("Посмотреть даты экзаменов")
        button_final = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2,button3,button4,button_final, back)
        self.bot.send_message(message.chat.id, text="Добро пожаловать, студент!", reply_markup=markup)

class TeacherHandler:
    def __init__(self, bot, my_bot, cur3, cur5):
        self.bot = bot
        self.my_bot = my_bot
        self.cur3 = cur3
        self.cur5 = cur5
        self.subject_info = {}

    def handle_teacher(self, message):
        teacher_id, subject_id, unused = self.my_bot.get_teacher_info(self.my_bot.authenticated_users[message.chat.id])

        if message.text == 'Посмотреть журнал':
            if subject_id:
                query = "SELECT Students.name, Ratings.grade FROM Students " \
                        "LEFT JOIN Ratings ON Students.studentid = Ratings.studentsid " \
                        "WHERE Ratings.itemid IN (SELECT Items.ItemID FROM Items WHERE Items.ItemID = %s);"
                self.cur3.execute(query, (subject_id,))
                results = self.cur3.fetchall()

                if results:
                    for row in results:
                        student_name, grade = row
                        self.bot.send_message(message.chat.id, f"{student_name}: {grade}")
                else:
                    self.bot.send_message(message.chat.id, "Нет данных в журнале.")
            else:
                self.bot.send_message(message.chat.id, "Учитель не связан ни с одним предметом. Обратитесь к администратору.")
            self.bot.register_next_step_handler(message, lambda msg: self.handle_change_grade(msg, subject_id))  # Используем lambda для передачи параметра
        elif message.text == 'Получение списка студентов группы':
            self.bot.send_message(message.chat.id, text='Введите ID группы, чтобы получить список студентов:')
            self.bot.register_next_step_handler(message, self.get_students_for_group)
        elif message.text == 'Выход':
            self.my_bot.bot.send_message(message.chat.id, "Выход")

    




    def get_students_in_group(self, group_id):
        query = "SELECT Students.name, Students.studentid FROM Students " \
                "JOIN groups ON Students.studentid = groups.studentid " \
                "JOIN group_university ON groups.groupsid = group_university.groupsid " \
                "WHERE group_university.groupsid = %s;"
        self.cur5.execute(query, (group_id,))
        students = self.cur5.fetchall()
        return students
    
    def handle_teacher_menu(self, message, subject_id=None):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Посмотреть журнал")
        button4 = types.KeyboardButton("Получение списка студентов группы")
        button2 = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2,button4, back)
        self.bot.send_message(message.chat.id, text="Добро пожаловать, учитель!", reply_markup=markup)


class AdminHandler:
    def __init__(self, my_bot, cur1, cur2, cur3, cur4):
        self.my_bot = my_bot
        self.cur1, self.cur2, self.cur3, self.cur4 = cur1, cur2, cur3, cur4
        self.delete_query = "DELETE FROM Accounts WHERE Login = %s RETURNING role, accountsid;"

    def get_users_list(self):
        users_info = "\n".join([f"{login}, {user[1][1]}" for login, user in self.my_bot.user_credentials.items()])
        return users_info

    def handle_admin(self, message):
        if message.text == 'Добавить пользователя':
            self.my_bot.bot.send_message(message.chat.id, text='Введите логин, пароль и роль пользователя через запятую')
            self.my_bot.bot.register_next_step_handler(message, self.add_user)
        elif message.text == 'Удалить пользователя':
            self.my_bot.bot.send_message(message.chat.id, text='Введите логин пользователя, которого хотите удалить:')
            self.my_bot.bot.register_next_step_handler(message, self.remove_user)
        elif message.text == 'Изменить расписание':
            self.my_bot.bot.send_message(message.chat.id, text='Введите ID группы, для которой хотите изменить расписание:')
            self.my_bot.bot.register_next_step_handler(message, self.handle_change_schedule)
        elif message.text == 'Изменить мероприятия':
            self.my_bot.bot.send_message(message.chat.id, text='Введите новое мероприятие и его дату через запятую (например, Мероприятие, 2023-12-31):')
            self.my_bot.bot.register_next_step_handler(message, self.update_events_on_campus)

    def handle_change_schedule(self, message):
        try:
            group_id = int(message.text.strip())  
            group_query = "SELECT group_name FROM group_university WHERE groupsid = %s;"
            self.cur2.execute(group_query, (group_id,))
            group_name = self.cur2.fetchone()

            if group_name:
                self.my_bot.bot.send_message(message.chat.id, text=f'Выбрана группа: {group_name[0]}')
                self.my_bot.bot.send_message(message.chat.id, text='Введите день недели (например, Понедельник):')
                self.my_bot.bot.register_next_step_handler(message, lambda msg: self.choose_day_and_time_for_schedule_change(msg, group_id))
            else:
                self.my_bot.bot.send_message(message.chat.id, text='Группа с указанным ID не найдена.')

        except ValueError:
            self.my_bot.bot.send_message(message.chat.id, text='Введите корректный ID группы (целое число).')

    def choose_day_and_time_for_schedule_change(self, message, group_id):
        try:
            chosen_day = message.text.strip()
            days_of_week = ['Monday', 'Tuesday', 'Wensday', 'Thursday', 'Friday']

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for day in days_of_week:
                markup.add(types.KeyboardButton(day))
            self.my_bot.bot.send_message(message.chat.id, text='Выберите день недели:', reply_markup=markup)
            self.my_bot.bot.register_next_step_handler(message, lambda msg: self.choose_time_for_schedule_change(msg, group_id, chosen_day))

        except ValueError:
            self.my_bot.bot.send_message(message.chat.id, text='Неверный день недели.')

    def choose_time_for_schedule_change(self, message, group_id, chosen_day):
        try:
            query = """
                SELECT DISTINCT StartTime
                FROM ClassSchedule
                WHERE groupsid = %s AND DayOfWeek = %s
                ORDER BY StartTime;
            """
            self.cur2.execute(query, (group_id, chosen_day))
            results = self.cur2.fetchall()

            available_times = [result[0].strftime('%H:%M:%S') for result in results]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for available_time in available_times:
                markup.add(types.KeyboardButton(available_time))
            self.my_bot.bot.send_message(message.chat.id, text='Выберите точное время:', reply_markup=markup)
            self.my_bot.bot.register_next_step_handler(message, lambda msg: self.choose_item_for_schedule_change(msg, group_id, chosen_day))

        except ValueError:
            self.my_bot.bot.send_message(message.chat.id, text='Ошибка при выборе времени.')

    def choose_item_for_schedule_change(self, message, group_id, chosen_day):
        try:
            chosen_time = message.text.strip()
            items = self.get_items()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for item in items:
                markup.add(types.KeyboardButton(item))
            self.my_bot.bot.send_message(message.chat.id, text='Выберите предмет:', reply_markup=markup)
            self.my_bot.bot.register_next_step_handler(message, lambda msg: self.update_schedule(msg, group_id, chosen_day, chosen_time))

        except ValueError:
            self.my_bot.bot.send_message(message.chat.id, text='Ошибка при выборе предмета.')

    def update_schedule(self, message, group_id, chosen_day, chosen_time):
        try:
            chosen_item = message.text.strip()

            get_item_id_query = "SELECT ItemID FROM Items WHERE ItemName = %s;"
            self.cur3.execute(get_item_id_query, (chosen_item,))
            item_id = self.cur3.fetchone()[0]

            update_schedule_query = """
                UPDATE ClassSchedule
                SET ItemID = %s
                WHERE groupsid = %s AND DayOfWeek = %s AND StartTime = %s;
            """

            self.cur4.execute(update_schedule_query, (item_id, group_id, chosen_day, chosen_time))
            self.my_bot.conn.commit()

            self.my_bot.bot.send_message(message.chat.id, text='Расписание успешно изменено.')

        except ValueError:
            self.my_bot.bot.send_message(message.chat.id, text='Неверный предмет.')

    def get_items(self):
        query = "SELECT ItemName FROM Items"
        self.cur1.execute(query)
        items = [row[0] for row in self.cur1.fetchall()]
        return items

    def update_events_on_campus(self, message):
        try:
            event_name, event_date = map(str.strip, message.text.split(','))
            update_query = "INSERT INTO EventsOnCampus (EventName, EventDate) VALUES (%s, %s) RETURNING EventID;"
            self.cur3.execute(update_query, (event_name, event_date))
            event_id = self.cur3.fetchone()[0]
            self.my_bot.conn.commit()

            self.my_bot.bot.send_message(message.chat.id, text=f'Мероприятие успешно изменено.')

        except ValueError:
            self.my_bot.bot.send_message(message.chat.id, text='Неверный формат данных для мероприятия.')
    
    def add_user(self, message):
        try:
            login, password, role = map(str.strip, message.text.split(','))
            self.cur2.execute('INSERT INTO Accounts (login, password, role) VALUES (%s, %s, %s) RETURNING accountsid;', (login, password, role))
            self.my_bot.conn.commit()
            accounts_id = self.cur2.fetchone()[0]

            self.my_bot.user_credentials[login] = (password, role)

            self.my_bot.bot.send_message(message.chat.id, text=f'Пользователь {login} успешно добавлен в базу данных.')

        except Exception as e:
            print(e)
            self.my_bot.conn.rollback()
            self.my_bot.bot.send_message(message.chat.id, text=f'Ошибка при добавлении пользователя')

    def remove_user(self, message):
        try:
            login = message.text.strip()
            result = self.cur3.execute(self.delete_query, (login,))
            result = self.cur3.fetchone()
            if result:
                role, accounts_id = result
                self.my_bot.conn.commit()
                self.my_bot.bot.send_message(message.chat.id, text=f'Пользователь {login} успешно удален из базы данных')
            else:
                self.my_bot.bot.send_message(message.chat.id, text=f'Пользователь {login} не найден')
        except Exception as e:
            print(e)
            self.my_bot.bot.send_message(message.chat.id, text=f'Ошибка при удалении пользователя')

    def handle_admin_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Добавить пользователя")
        button2 = types.KeyboardButton("Удалить пользователя")
        button3 = types.KeyboardButton("Изменить расписание")
        button4 = types.KeyboardButton("Изменить мероприятия")  # Новая кнопка
        button_exit = types.KeyboardButton("Выход")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, button3, button4, button_exit, back)
        self.my_bot.bot.send_message(message.chat.id, text="Добро пожаловать, администратор!", reply_markup=markup)


if __name__ == '__main__':
    TOKEN = '6392060028:AAEVRZLwG3yJk2hNoxPR5MiNQNpofxRhaRM'
    my_bot = MyTelegramBot(TOKEN)
    my_bot.run()

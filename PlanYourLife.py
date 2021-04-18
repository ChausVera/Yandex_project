import sys
import hashlib
import sqlite3
from PyQt5.QtWidgets import (QApplication, QComboBox, QWidget,
                             QCalendarWidget, QTextEdit, QMessageBox,
                             QLineEdit, QPushButton, QTableWidgetItem,
                             QLabel, QListWidget, QTableWidget, QHeaderView)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon  # импорт необходимых библиотек


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.unitUI()
        self.con = sqlite3.connect('accounts.db')
        self.cur = self.con.cursor()
        self.acc = 0
        self.pasw = 0
        self.v = False

    def unitUI(self):
        self.setGeometry(0, 0, 1000, 1500)  # создаем окно
        self.setWindowTitle('Планер')
        self.setWindowIcon(QIcon('web.png'))
        self.lab = QLabel(self)  # ввод логина
        self.lab.move(68, 20)
        self.lab.setText('Логин:')
        self.eline = QLineEdit(self)
        self.eline.move(110, 18)
        self.lab2 = QLabel(self)  # ввод пароля
        self.lab2.move(245, 20)
        self.lab2.setText('Пароль:')
        self.eline2 = QLineEdit(self)
        self.eline2.move(295, 18)
        self.btn = QPushButton('Войти', self)  # кнопка входа
        self.btn.move(420, 5)
        self.btn.resize(115, 22)
        self.btn.setStyleSheet("background-color: cyan")
        self.btn.clicked.connect(self.log_in_system)
        self.btn2 = QPushButton('Зарегестрироваться', self)
        # кнопка регистрации
        self.btn2.move(420, 30)
        self.btn2.setStyleSheet("background-color: green")
        self.btn2.clicked.connect(self.create_new_account)
        self.cal = QCalendarWidget(self)  # создаем календарь
        self.cal.setGridVisible(True)
        self.cal.move(50, 60)
        self.cal.resize(600, 600)
        self.cal.clicked[QDate].connect(self.showDate)
        # отображение отмеченой даты
        self.lab3 = QLabel(self)
        date = self.cal.selectedDate()
        self.lab3.setText(date.toString())
        self.lab3.move(790, 35)
        self.lab3.resize(200, 25)
        self.lab3.setStyleSheet("background-color: lightGray")
        self.lab4 = QLabel(self)  # место отображения отмченой даты
        self.lab4.setText('')
        self.lab4.move(660, 35)
        self.lab4.resize(130, 25)
        self.lab4.setStyleSheet("background-color: lightGray")
        self.btn3 = QPushButton('+', self)  # кнопка для создания событий
        self.btn3.move(660, 3)
        self.btn3.resize(330, 30)
        self.btn3.setStyleSheet("background-color: gray")
        self.btn3.setToolTip('Новое событие')
        self.btn3.clicked.connect(self.create_new_event)
        self.btn4 = QPushButton('Выйти', self)
        # кнопка для выхода из аккаунта
        self.btn4.move(560, 15)
        self.btn4.setStyleSheet("background-color: lightGray")
        self.btn4.clicked.connect(self.exit_account)
        self.btn5 = QPushButton('Удалить событие', self)
        # кнопка для создания событий
        self.btn5.move(550, 665)
        self.btn5.setStyleSheet("background-color: gray")
        self.btn5.clicked.connect(self.delite)
        self.btn6 = QPushButton('Изменить событие', self)
        self.btn6.move(435, 665)
        self.btn6.setStyleSheet("background-color: gray")
        self.btn6.clicked.connect(self.chenge)
        self.btn7 = QPushButton('Подробнее', self)
        self.btn7.move(350, 665)
        self.btn7.setStyleSheet("background-color: gray")
        self.btn7.clicked.connect(self.details)
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(20)
        self.table.setHorizontalHeaderLabels(["id", 'название'])
        self.table.setColumnWidth(1, 80)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.move(675, 70)
        self.table.resize(300, 600)
        self.btn8 = QPushButton('Приглашения', self)
        self.btn8.move(135, 665)
        self.btn8.setStyleSheet("background-color: gray")
        self.btn8.clicked.connect(self.mails)
        self.btn9 = QPushButton('Настройки', self)
        self.btn9.move(50, 665)
        self.btn9.setStyleSheet("background-color: gray")
        self.btn9.clicked.connect(self.tools)

    def showDate(self, date):
        self.lab3.setText(date.toString())
        if self.entrance():
            today_ev = self.cur.execute("""SELECT event,id FROM events
                        WHERE guests LIKE'%{}%'
                        AND date = '{}'""".format(self.acc, self.lab3.text())).fetchall()
            self.table.setRowCount(len(today_ev))
            for i in range(len(today_ev)):
                self.table.setItem(i, 1, QTableWidgetItem(today_ev[i][0]))
                self.table.setItem(i, 0, QTableWidgetItem(str(today_ev[i][1])))

    def log_in_system(self):  # проверки при входе
        h = hashlib.md5(self.eline2.text().encode())
        if self.v:
            pass
        elif (self.eline.text(),) not in self.cur.execute("""SELECT nickname
                    FROM log_in_the_system WHERE id > 0""").fetchall():
            # проверка существования аккаунта
            self.msg = QMessageBox.warning(self, 'Неверный логин',
                                           'Логин не найден')
        elif (h.hexdigest(),) not in self.cur.execute("""SELECT password
                        FROM log_in_the_system
                        WHERE nickname = '{}'""".format(self.eline.text())).fetchall():
            # совпадение ввода с паролем
            self.msg = QMessageBox.warning(self, 'Неверный пароль',
                                           'Возможно нажата клавиша ' +
                                           'CapsLock? \n Может быть ,' +
                                           'у Вас включена неправильная '+
                                           'раскладка? (русская/английская)')
        else:  # удачный вход
            self.acc = self.eline.text()
            self.pasw = self.eline2.text()
            self.eline2.setText(len(self.pasw) * '*')
            self.eline2.setReadOnly(True)
            self.eline.setReadOnly(True)
            self.v = True
            text = 'Добро пожаловать!'
            your_events = self.cur.execute("""SELECT id FROM events
                        WHERE guests LIKE'%{}%' """.format(self.acc)).fetchall()
            col = int(self.cur.execute("""SELECT col_events FROM log_in_the_system
                        WHERE nickname = '{}'""".format(self.acc)).fetchall()[0][0])
            if len(your_events) > col:
                if str(len(your_events) - col)[-1] == '1':
                    text += '\nУ вас ' + str(len(your_events) - col) + ' новое событие!'
                else:
                    text += '\nУ вас ' + str(len(your_events) - col) + ' новых событий!'
            elif len(your_events) < col:
                if str(col - len(your_events))[-1] == '1':
                    text += '\nОтменено ' + str(col - len(your_events)) + ' событие!'
                else:
                    text += '\nОтменено ' + str(col - len(your_events)) + ' событий!'
            self.cur.execute("""UPDATE log_in_the_system SET col_events = ? WHERE nickname = ?""",
                         (str(len(your_events)), self.acc))
            self.con.commit()
            self.msg = QMessageBox.information(self, 'ОК', text)

    def msgbtn(self):
        pass

    def create_new_account(self):  # проверки при регистрации
        h = hashlib.md5(self.eline2.text().encode())
        if self.v:
            pass
        elif len(self.eline.text()) < 4:  # проверка длины логина
            self.msg = QMessageBox.warning(self, 'Неверный логин',
                                           'Логин должен содержать '+
                                           'не менее 4 символов')
        elif set('+-') & set(self.eline.text()) != set():
            # проверка отсутствия символов "+" и "-" в логине
            self.msg = QMessageBox.warning(self, 'Неверный логин',
                                           'Логин не должен содержать' +
                                           ' символы "+" или "-"')
        elif len(self.eline2.text()) < 8:  # проверка длины пароля
            self.msg = QMessageBox.warning(self, 'Неверный пароль',
                                           'Пароль должен содержать ' +
                                           'не менее 8 символов')
        elif set(self.eline2.text()) & set('1234567890') == set():
            # проверка наличия цифр в пароле
            self.msg = QMessageBox.warning(self, 'Неверный пароль',
                                           'В пароле должна содержаться' +
                                           ' минимум одна цифра')
        elif self.eline2.text().isdigit():  # проверка наличия букв в пароле
            self.msg = QMessageBox.warning(self, 'Неверный пароль',
                                           'Пароль должен содержать как ' +
                                           'минимум одну букву')
        elif (self.eline.text(),) in self.cur.execute("""SELECT nickname
                    FROM log_in_the_system WHERE ID > 0""").fetchall():
            self.msg = QMessageBox.warning(self, 'Неверный логин',
                                           'Аккаунт с таким логином '+
                                           'уже существует')
        else:  # удачная регистрация
            self.msg = QMessageBox.information(self, 'ОК',
                                               'Успешная регистрация')
            self.cur.execute("""INSERT INTO log_in_the_system(nickname,
                        password, col_events) VALUES ('{}',
                        '{}', 0)""".format(self.eline.text(),
                                           h.hexdigest()))
            self.con.commit()
            self.acc = self.eline.text()
            self.pasw = self.eline2.text()
            self.eline2.setText(len(self.pasw) * '*')
            self.v = True

    def create_new_event(self):  # создаем новое событие fencing123
        if self.entrance():
            self.ev = NewEvent(self.acc, self.pasw, self.lab3.text())
            self.ev.show()
        else:
            self.msg = QMessageBox.warning(self, 'Ошибка!', 'Войдите в аккаунт')

    def delite(self):
        your_events = self.cur.execute("""SELECT id FROM events
                        WHERE guests LIKE'%{}%' """.format(self.acc)).fetchall()
        try:
            if self.entrance():
                curid = self.table.item(self.table.currentRow(), 0).text()
                allparametr = self.cur.execute("""SELECT * FROM events
                        WHERE id = '{}'""".format(curid)).fetchall()
                if allparametr[0][2] != self.acc:
                    self.msg = QMessageBox.warning(self, 'Ошибка!', 'Вы не можете удалить событие')
                else:
                    self.reply = QMessageBox.question(self, 'Удаление',
                                                      'Вы хотите удалить событие?',
                                                      QMessageBox.Yes | QMessageBox.No,
                                                      QMessageBox.No)
                    if self.reply == QMessageBox.Yes:
                        self.cur.execute("""DELETE FROM events WHERE id = {}""".format(int(curid)))
                        self.cur.execute("""UPDATE log_in_the_system SET col_events = ? WHERE nickname = ?""",
                                 (str(len(your_events) - 1), self.acc))
                        self.con.commit()
            else:
                self.msg = QMessageBox.warning(self, 'Ошибка!', 'Войдите в аккаунт')
        except AttributeError:
            self.msg = QMessageBox.warning(self, 'Ошибка!', 'Выберете событие')

    def exit_account(self):
        if self.entrance():
            self.reply = QMessageBox.question(self, 'Выход',
                                              'Вы хотите выйти из аккаунта?',
                                              QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.No)
            if self.reply == QMessageBox.Yes:
                self.acc = 0
                self.pasw = 0
                self.eline2.setText('')
                self.eline.setText('')
                self.eline2.setReadOnly(False)
                self.eline.setReadOnly(False)
                self.v = False
        else:
            self.msg = QMessageBox.warning(self, 'Ошибка!', 'Войдите в аккаунт')

    def entrance(self):
        if (self.eline.text() == self.acc and
            self.eline2.text() == len(self.pasw) * '*'):
            return True
        return False

    def chenge(self):
        your_events = self.cur.execute("""SELECT id FROM events
                        WHERE guests LIKE'%{}%' """.format(self.acc)).fetchall()
        try:
            if self.entrance():
                curid = self.table.item(self.table.currentRow(), 0).text()
                allparametr = self.cur.execute("""SELECT * FROM events
                        WHERE id = '{}'""".format(curid)).fetchall()
                if allparametr[0][2] != self.acc:
                    self.msg = QMessageBox.warning(self, 'Ошибка!', 'Вы не можете изменить событие')
                else:
                    self.ch = ChangeEvent(allparametr, self.acc)
                    self.ch.show()
                    self.con.commit()
            else:
                self.msg = QMessageBox.warning(self, 'Ошибка!', 'Войдите в аккаунт')
        except AttributeError:
            self.msg = QMessageBox.warning(self, 'Ошибка!', 'Выберете событие')

    def details(self):
        your_events = self.cur.execute("""SELECT id FROM events
                        WHERE guests LIKE'%{}%' """.format(self.acc)).fetchall()
        try:
            if self.entrance():
                curid = self.table.item(self.table.currentRow(), 0).text()
                allparametr = self.cur.execute("""SELECT * FROM events
                        WHERE id = '{}'""".format(curid)).fetchall()
                self.inf = Details(allparametr, self.acc)
                self.inf.show()
                self.con.commit()
            else:
                self.msg = QMessageBox.warning(self, 'Ошибка!', 'Войдите в аккаунт')
        except AttributeError:
            self.msg = QMessageBox.warning(self, 'Ошибка!', 'Выберете событие')

    def mails(self):
        pass

    def tools(self):
        pass


class NewEvent(QWidget):
    def __init__(self, nick, pasw, date):
        self.date = date
        self.usern = nick
        self.userp = pasw
        self.con = sqlite3.connect('accounts.db')
        self.cur = self.con.cursor()
        super().__init__()
        self.guests = [self.usern]
        self.event_name = ''
        self.creator = nick
        self.start = ''
        self.end = ''
        self.komment = ''
        self.unitUI()

    def unitUI(self):
        self.setGeometry(100, 100, 300, 610)
        # создаем окно с параметрами нового события
        self.setWindowTitle('Новое событие')
        self.alln = [i[0] + '\t-' for i in self.cur.execute("""SELECT
                    nickname FROM log_in_the_system
                    WHERE nickname != '{}'""".format(self.usern)).fetchall()]
        self.x = len(self.alln)
        self.min = [str(i).rjust(2, '0') for i in range(0, 56, 5)]
        self.hour = [str(i).rjust(2, '0') for i in range(0, 24)]
        self.lab = QLabel(self)
        self.lab.setText('Название события:')
        self.lab.move(5, 10)
        self.name = QLineEdit(self)
        self.name.move(105, 8)
        self.lab2 = QLabel(self)
        self.lab2.setText('Начало:')
        self.lab2.move(5, 40)
        self.starth = QComboBox(self)
        self.starth.addItems(self.hour)
        self.starth.move(60, 38)
        self.lab3 = QLabel(self)
        self.lab3.setText('час(-ов)')
        self.lab3.move(110, 40)
        self.startm = QComboBox(self)
        self.startm.addItems(self.min)
        self.startm.move(180, 38)
        self.lab4 = QLabel(self)
        self.lab4.setText('минут(-а)')
        self.lab4.move(230, 40)
        self.lab5 = QLabel(self)
        self.lab5.setText('Конец:')
        self.lab5.move(5, 70)
        self.endh = QComboBox(self)
        self.endh.addItems(self.hour)
        self.endh.move(60, 68)
        self.lab6 = QLabel(self)
        self.lab6.setText('час(-ов)')
        self.lab6.move(110, 70)
        self.endm = QComboBox(self)
        self.endm.addItems(self.min)
        self.endm.move(180, 68)
        self.lab7 = QLabel(self)
        self.lab7.setText('минут(-а)')
        self.lab7.move(230, 70)
        self.lab8 = QLabel(self)
        self.lab8.setText('Гости:')
        self.lab8.move(5, 100)
        self.l = QListWidget(self)
        self.l.addItems(self.alln)
        self.l.move(20, 128)
        self.l.itemClicked.connect(self.selectionChanged)
        self.lab9 = QLabel(self)
        self.lab9.setText('Комментарий')
        self.lab9.move(5, 330)
        self.com = QTextEdit(self)
        self.com.move(20, 350)
        self.save = QPushButton('Сохранить', self)
        self.save.move(75, 580)
        self.save.clicked.connect(self.save_event)
        self.otm = QPushButton('Отмена', self)
        self.otm.move(155, 580)
        self.otm.clicked.connect(self.otmen_event)

    def selectionChanged(self, item):
        if '\t-' in item.text():
            item.setText(item.text()[: -2] + '\t+')
            self.guests.append(item.text()[: -2])
        else:
            item.setText(item.text()[: -2] + '\t-')
            del self.guests[self.guests.index(item.text()[: -2])]

    def save_event(self):
        your_events = self.cur.execute("""SELECT id FROM events
                        WHERE guests LIKE'%{}%' """.format(self.usern)).fetchall()
        if self.name.text() == '': # проверка наличия данных
            self.msg = QMessageBox.warning(self, 'Ошибка!',
                                           'Введите название события')
        elif (self.starth.currentText() == '00' and
              self.startm.currentText() == '00' and
              self.endh.currentText() == '00' and
              self.endm.currentText() == '00'):
            self.msg = QMessageBox.warning(self, 'Ошибка!',
                                           'Введите время начала ' +
                                           'и завершения события')
        elif self.guests == []:
            self.msg = QMessageBox.warning(self, 'Ошибка!',
                                           'Выберете гостей')
        else:
            self.cur.execute("""INSERT INTO events(event, creator, date, start,
                            end, guests, komment) VALUES ('{}', '{}', '{}',
                            '{}', '{}', '{}', '{}')""".format(self.name.text(),
                                                  self.usern,
                                                  self.date,
                                                  (self.starth.currentText() +
                                                   ':' +
                                                   self.startm.currentText()),
                                                  (self.endh.currentText() +
                                                   ':' +
                                                   self.endm.currentText()),
                                                  '+'.join(self.guests),
                                                  self.com.toPlainText()))
            self.cur.execute("""UPDATE log_in_the_system SET col_events = ? WHERE nickname = ?""",
                             (str(len(your_events) + 1), self.usern))
            self.con.commit()
            self.close()

    def otmen_event(self):
        self.close()


class ChangeEvent(QWidget): # fencing123
    def __init__(self, allp, acc):
        self.date = allp[0][3]
        self.usern = acc
        self.con = sqlite3.connect('accounts.db')
        self.cur = self.con.cursor()
        super().__init__()
        self.guests = allp[0][6].split('+')
        self.event_name = allp[0][1]
        self.creator = allp[0][2]
        self.valstarth = allp[0][4][: 2]
        self.valstartm = allp[0][4][3:]
        self.valendh = allp[0][5][: 2]
        self.valendm = allp[0][5][3:]
        self.com = QTextEdit(self)
        self.com.append(allp[0][7])
        self.lastid = allp[0][0]
        self.unitUI()

    def unitUI(self):
        self.setGeometry(100, 100, 300, 610)
        self.setWindowTitle('Изменение события')
        self.alln = [i[0] + '\t-' for i in self.cur.execute("""SELECT
                    nickname FROM log_in_the_system
                    WHERE nickname != '{}'""".format(self.usern)).fetchall()]
        for i in range(len(self.alln)):
            if self.alln[i][: -2] in self.guests:
                self.alln[i] = self.alln[i][: -1] + '+'
        self.x = len(self.alln)
        self.min = [str(i).rjust(2, '0') for i in range(0, 56, 5)]
        self.hour = [str(i).rjust(2, '0') for i in range(0, 24)]
        self.lab = QLabel('Название события:', self)
        self.lab.move(5, 10)
        self.name = QLineEdit(self)
        self.name.setText(self.event_name)
        self.name.move(105, 8)
        self.lab2 = QLabel('Начало:', self)
        self.lab2.move(5, 40)
        self.starth = QComboBox(self)
        self.starth.addItems(self.hour)
        self.starth.move(60, 38)
        self.starth.setCurrentIndex(self.hour.index(self.valstarth))
        self.lab3 = QLabel('час(-ов)', self)
        self.lab3.move(110, 40)
        self.startm = QComboBox(self)
        self.startm.addItems(self.min)
        self.startm.move(180, 38)
        self.startm.setCurrentIndex(self.min.index(self.valstartm))
        self.lab4 = QLabel('минут(-а)', self)
        self.lab4.move(230, 40)
        self.lab5 = QLabel('Конец:', self)
        self.lab5.move(5, 70)
        self.endh = QComboBox(self)
        self.endh.addItems(self.hour)
        self.endh.move(60, 68)
        self.endh.setCurrentIndex(self.hour.index(self.valendh))
        self.lab6 = QLabel('час(-ов)', self)
        self.lab6.move(110, 70)
        self.endm = QComboBox(self)
        self.endm.addItems(self.min)
        self.endm.move(180, 68)
        self.endm.setCurrentIndex(self.min.index(self.valendm))
        self.lab7 = QLabel('минут(-а)', self)
        self.lab7.move(230, 70)
        self.lab8 = QLabel('Гости:', self)
        self.lab8.move(5, 100)
        self.l = QListWidget(self)
        self.l.addItems(self.alln)
        self.l.move(20, 128)
        self.l.itemClicked.connect(self.selectionChanged)
        self.lab9 = QLabel('Комментарий', self)
        self.lab9.move(5, 330)
        self.com.move(20, 350)
        self.save = QPushButton('Сохранить', self)
        self.save.move(75, 580)
        self.save.clicked.connect(self.save_event)
        self.otm = QPushButton('Отмена', self)
        self.otm.move(155, 580)
        self.otm.clicked.connect(self.otmen_event)

    def selectionChanged(self, item):
        if '\t-' in item.text():
            item.setText(item.text()[: -2] + '\t+')
            self.guests.append(item.text()[: -2])
        else:
            item.setText(item.text()[: -2] + '\t-')
            del self.guests[self.guests.index(item.text()[: -2])]

    def save_event(self):
        your_events = self.cur.execute("""SELECT id FROM events
                        WHERE guests LIKE'%{}%' """.format(self.usern)).fetchall()
        if self.name.text() == '': # проверка наличия данных
            self.msg = QMessageBox.warning(self, 'Ошибка!',
                                           'Введите название события')
        elif (self.starth.currentText() == '00' and
              self.startm.currentText() == '00' and
              self.endh.currentText() == '00' and
              self.endm.currentText() == '00'):
            self.msg = QMessageBox.warning(self, 'Ошибка!',
                                           'Введите время начала ' +
                                           'и завершения события')
        elif len(self.guests) == 1:
            self.msg = QMessageBox.warning(self, 'Ошибка!',
                                           'Выберете гостей')
        else:
            self.cur.execute("""UPDATE events SET event = '{}', creator = '{}', date = '{}',
                        start = '{}', end = '{}', guests = '{}',
                        komment = '{}' WHERE id = {}""".format(self.name.text(),
                                                  self.usern,
                                                  self.date,
                                                  (self.starth.currentText() +
                                                   ':' +
                                                   self.startm.currentText()),
                                                  (self.endh.currentText() +
                                                   ':' +
                                                   self.endm.currentText()),
                                                  '+'.join(self.guests),
                                                  self.com.toPlainText(), self.lastid))
            self.con.commit()
            self.close()

    def otmen_event(self):
        self.close()


class Details(QWidget): # fencing123
    def __init__(self, allp, acc):
        self.date = allp[0][3]
        self.usern = acc
        self.con = sqlite3.connect('accounts.db')
        self.cur = self.con.cursor()
        super().__init__()
        self.guests = ', '.join(allp[0][6].split('+'))
        self.event_name = allp[0][1]
        self.creator = allp[0][2]
        self.time = allp[0][4] + '-' + allp[0][5]
        self.com = QTextEdit(self)
        self.com.setReadOnly(True)
        self.com.append(allp[0][7])
        print(allp[0][7], type(allp[0][7]))
        self.lastid = allp[0][0]
        self.unitUI()

    def unitUI(self):
        self.setGeometry(150, 150, 300, 300)
        self.setWindowTitle('Информация')
        self.alln = [i[0] + '\t-' for i in self.cur.execute("""SELECT
                    nickname FROM log_in_the_system
                    WHERE nickname != '{}'""".format(self.usern)).fetchall()]
        for i in range(len(self.alln)):
            if self.alln[i][: -2] in self.guests:
                self.alln[i] = self.alln[i][: -1] + '+'
        self.x = len(self.alln)
        self.min = [str(i).rjust(2, '0') for i in range(0, 56, 5)]
        self.hour = [str(i).rjust(2, '0') for i in range(0, 24)]
        self.lab = QLabel('Название события: ' + self.event_name, self)
        self.lab.move(5, 10)
        self.lab2 = QLabel('Время: ' + self.time, self)
        self.lab2.move(5, 30)
        self.lab8 = QLabel('Участники: ' + self.guests, self)
        self.lab8.move(5, 50)
        self.lab9 = QLabel('Комментарий', self)
        self.lab9.move(5, 70)
        self.com.move(20, 90)


if __name__ == '__main__':  # показываем окно пользователю
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
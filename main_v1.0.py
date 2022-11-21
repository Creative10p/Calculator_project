# импорт библиотек
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from sympy import *
import sqlite3


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Calculator5.ui', self) # Загружаем дизайн
        self.prev_calc.hide()
        self.prev_calc_2.hide()
        self.prev_calc_3.hide()
        self.prev_calc_4.hide()
        self.prev_calc_5.hide()
        self.answer.hide()
        self.answer_btn.hide()
        self.Volume.hide()
        self.area.hide()
        self.data.hide()
        self.length.hide()
        self.mass.hide()
        self.speed.hide()
        self.temperature.hide()
        self.time.hide()
        self.integer.hide()
        self.unit_of_the_measurement.hide()
        self.unit_of_the_measurement_2.hide()
        self.setGeometry(50,50,602,260)
        self.result.clicked.connect(self.compute)
        self.clear.clicked.connect(self.clear_operation)
        self.previous_calculations.clicked.connect(self.get_prev_calc)
        self.transpose.clicked.connect(self.transpose_operation)
        self.number_0.clicked.connect(self.writing)
        self.number_1.clicked.connect(self.writing)
        self.number_2.clicked.connect(self.writing)
        self.number_3.clicked.connect(self.writing)
        self.number_4.clicked.connect(self.writing)
        self.number_5.clicked.connect(self.writing)
        self.number_6.clicked.connect(self.writing)
        self.number_7.clicked.connect(self.writing)
        self.number_8.clicked.connect(self.writing)
        self.number_9.clicked.connect(self.writing)
        self.divide.clicked.connect(self.writing)
        self.root.clicked.connect(self.writing)
        self.minus.clicked.connect(self.writing)
        self.multiply.clicked.connect(self.writing)
        self.plus.clicked.connect(self.writing)
        self.dot.clicked.connect(self.writing)
        self.left_bracket.clicked.connect(self.writing)
        self.right_bracket.clicked.connect(self.writing)
        self.degree.clicked.connect(self.writing)
        self.f = False # self.f - флаг, отвечающий на вопрос "нажата ли кнопка self.previous_calculations?"
        self.f2 = False # self.f2 - флаг, отвечающий на вопрос "Было ли произведено вычисление?"
        self.f3 = False # self.f - флаг, отвечающий на вопрос "нажата ли кнопка self.transpose?"

    def writing(self): # функция, отвечающая за запись выражения в self.expr
        if self.f2:
            self.expr.setText('')
            self.f2 = False
        s = self.sender().text()
        if len(self.expr.text()) == 0 or (self.expr.text()[-1].isdigit() and s.isdigit())\
                or (self.expr.text()[-1] == '√') or s == '.' or self.expr.text()[-1] == '.':
            self.expr.setText(f"{self.expr.text()}{s}")
        else:
            self.expr.setText(f"{self.expr.text()} {s}")

    def clear_operation(self): # функция, отвечающая за удаление выражения из self.expr
        self.expr.setText("")

    def get_prev_calc(self): # функция, отвечающая за выведение предыдущих значений
        if (not self.f and self.sender().text() == 'Предыдущие вычисления') or (self.f and self.sender().text() != 'Предыдущие вычисления'):
            con = sqlite3.connect('previous_calculations.sqlite')
            cur = con.cursor()
            result = cur.execute("""select calculation from calculations""").fetchall()
            self.f = True
            try:
                self.prev_calc.show()
                self.prev_calc_2.show()
                self.prev_calc_3.show()
                self.prev_calc_4.show()
                self.prev_calc_5.show()
                self.prev_calc.setText(str(result[0])[2:-3])
                if not self.f3:
                    self.setGeometry(50, 50, 602, 400)
                try:
                    self.prev_calc_2.setText(str(result[1])[2:-3])
                    try:
                        self.prev_calc_3.setText(str(result[2])[2:-3])
                        try:
                            self.prev_calc_4.setText(str(result[3])[2:-3])
                            try:
                                self.prev_calc_5.setText(str(result[4])[2:-3])
                            except:
                                self.prev_calc_5.hide()
                        except:
                            self.prev_calc_4.hide()
                            self.prev_calc_5.hide()
                    except:
                        self.prev_calc_3.hide()
                        self.prev_calc_4.hide()
                        self.prev_calc_5.hide()
                except:
                    self.prev_calc_2.hide()
                    self.prev_calc_3.hide()
                    self.prev_calc_4.hide()
                    self.prev_calc_5.hide()
            except:
                self.prev_calc.hide()
                self.prev_calc_2.hide()
                self.prev_calc_3.hide()
                self.prev_calc_4.hide()
                self.prev_calc_5.hide()
        else:
            self.prev_calc.hide()
            self.prev_calc_2.hide()
            self.prev_calc_3.hide()
            self.prev_calc_4.hide()
            self.prev_calc_5.hide()
            if not self.f3:
                self.setGeometry(50, 50, 602, 260)
            self.f = False

    def compute(self): # функция, отвечающая за вычисления и добавление их в базу данных
        try:
            self.expression = self.expr.text().split()
            for i in range(len(self.expression)):
                if '√' in self.expression[i]:
                    self.expression[i] = (self.expression[i][1:]+'^0.5')
            self.expression2 = " ".join(x for x in self.expression)
            self.res = expand(self.expression2)
            if not str(self.res).isdigit() and '/' not in str(self.res) and '.' not in str(self.res)\
                    and '-' not in str(self.res):
                self.res = 'Ошибка!'
            self.expr.setText(f"{self.expr.text()} = {self.res}")
            self.f2 = True
            con = sqlite3.connect('previous_calculations.sqlite')
            cur = con.cursor()
            result = cur.execute("""select count(*) from calculations""").fetchall()
            result2 = cur.execute(
                f"""INSERT INTO calculations(calculation) VALUES('{self.expr.text()}')""").fetchall()
            if int(str(result)[2]) == 5:
                result3 = cur.execute(f"""delete from calculations
                where id = (select min(id) from calculations)""").fetchall()
            con.commit()
            if self.f:
                self.get_prev_calc()
        except:
            self.expr.setText('Ошибка!')
            self.f2 = True

    def transpose_operation(self): # функция, отвечающая за отображения интерфейса перевода между единицами измерения
        if not self.f3:
            self.f3 = True
            self.answer.show()
            self.answer_btn.show()
            self.Volume.show()
            self.area.show()
            self.data.show()
            self.length.show()
            self.mass.show()
            self.speed.show()
            self.temperature.show()
            self.time.show()
            self.integer.show()
            self.unit_of_the_measurement.show()
            self.unit_of_the_measurement_2.show()
            self.setGeometry(50, 50, 602, 500)
            self.answer_btn.clicked.connect(self.calculation)
        else:
            self.f3 = False
            self.answer.hide()
            self.answer_btn.hide()
            self.Volume.hide()
            self.area.hide()
            self.data.hide()
            self.length.hide()
            self.mass.hide()
            self.speed.hide()
            self.temperature.hide()
            self.time.hide()
            self.integer.hide()
            self.unit_of_the_measurement.hide()
            self.unit_of_the_measurement_2.hide()
            if not self.f:
                self.setGeometry(50, 50, 602, 260)
            else:
                self.setGeometry(50, 50, 602, 400)

    def calculation(self): # функция, отвечающая за перевод из одной единицы измерения в другую
        try:
            if self.length.isChecked():
                dict = {'мм': '1', 'см': '10', 'м': '1000',
                        'км': '1000000'}  # мм -> см = 10; см -> м = 100; м -> км = 1000
                self.answer.setText(
                    str(float(self.integer.text()) * int(dict[self.unit_of_the_measurement.text()[:2]]) / int(
                        dict[self.unit_of_the_measurement_2.text()])))
            if self.area.isChecked():
                dict = {'мм': '1', 'см': '100', 'м': '1000000',
                        'км': '1000000000000'}  # мм -> см = 10; см -> м = 100; м -> км = 1000
                self.answer.setText(
                    str(float(self.integer.text()) * int(dict[self.unit_of_the_measurement.text()[:2]]) / int(
                        dict[self.unit_of_the_measurement_2.text()])))
            if self.Volume.isChecked():
                dict = {'мм': '1', 'см': '1000', 'м': '1000000000',
                        'км': '1000000000000000000'}  # мм -> см = 10; см -> м = 100; м -> км = 1000
                self.answer.setText(
                    str(float(self.integer.text()) * int(dict[self.unit_of_the_measurement.text()[:2]]) / int(
                        dict[self.unit_of_the_measurement_2.text()])))
            if self.speed.isChecked():
                if self.unit_of_the_measurement.text() == 'м/с' \
                        and self.unit_of_the_measurement_2.text() == 'км/ч':
                    self.answer.setText(str(float(self.integer.text()) * 36 / 10))
                elif self.unit_of_the_measurement.text() == 'км/ч' \
                        and self.unit_of_the_measurement_2.text() == 'м/с':
                    self.answer.setText(str(float(self.integer.text()) * 10 / 36))
                else:
                    self.answer.setText('Ошибка!')
            if self.time.isChecked():
                dict = {'мс': '1', 'с': '1000', 'мин': '60000', 'ч': '3600000'}
                self.answer.setText(
                    str(float(self.integer.text()) * int(dict[self.unit_of_the_measurement.text()]) / int(
                        dict[self.unit_of_the_measurement_2.text()])))
            if self.mass.isChecked():
                dict = {'мг': '1', 'г': '1000', 'кг': '1000000', 'т': '1000000000'}
                self.answer.setText(
                    str(float(self.integer.text()) * int(dict[self.unit_of_the_measurement.text()[:2]]) / int(
                        dict[self.unit_of_the_measurement_2.text()])))
            if self.data.isChecked():
                dict = {'б': '1', 'кб': '1024', 'мб': '1048576', 'гб': '1073741824'}
                self.answer.setText(
                    str(float(self.integer.text()) * int(dict[self.unit_of_the_measurement.text()[:2]]) / int(
                        dict[self.unit_of_the_measurement_2.text()])))
            if self.temperature.isChecked():
                if self.unit_of_the_measurement.text() == 'C' \
                        and self.unit_of_the_measurement_2.text() == 'F':
                    self.answer.setText(str((float(self.integer.text()) + 32 * 5 / 9) / 5 * 9))
                elif self.unit_of_the_measurement.text() == 'F' \
                        and self.unit_of_the_measurement_2.text() == 'C':
                    self.answer.setText(str((float(self.integer.text()) - 32) * 5 / 9))
                elif self.unit_of_the_measurement.text() == 'C' \
                        and self.unit_of_the_measurement_2.text() == 'K':
                    self.answer.setText(str(float(self.integer.text()) + 273.15))
                elif self.unit_of_the_measurement.text() == 'K' \
                        and self.unit_of_the_measurement_2.text() == 'C':
                    self.answer.setText(str(float(self.integer.text()) - 273.15))
                else:
                    self.answer.setText('Ошибка!')
        except:
            self.answer.setText('Ошибка!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
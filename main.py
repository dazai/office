# -*- coding: utf-8 -*-
import sqlite3
import sys
import icu
import arabic_reshaper
from bidi.algorithm import get_display

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QAction, QWidget, QTabWidget, \
    QLineEdit, QComboBox, QFormLayout, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from fpdf import FPDF

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        bar = self.menuBar()
        file = bar.addMenu('Fchier')
        file.addAction('New')
        save = QAction("Save", self)
        save.setShortcut("Ctrl+S")
        file.addAction(save)
        edit = bar.addMenu("Edit")
        edit.addAction("copy")
        edit.addAction("paste")
        quitter = QAction("Quitter", self)
        file.addAction(quitter)
        file.triggered[QAction].connect(self.process_trigger)
        self.setWindowTitle("office")
        tabs = Tabs(self)
        self.setCentralWidget(tabs)

    @staticmethod
    def process_trigger():
        sys.exit(0)


def find_all_students():
    cursor.execute(''' SELECT * FROM eleve ''')
    return cursor.fetchall()


class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)
        self.hbox2 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.refresh_button = QPushButton("تحيين")
        self.statistics_layout = QFormLayout()
        self.average = QLineEdit()
        self.all_classes = QComboBox()
        self.criteria = QComboBox()
        self.filter_result = QTableWidget()
        self.classe_list = QComboBox()
        self.level = QComboBox()
        self.result = QTableWidget()
        self.layout = QHBoxLayout()
        self.student_id = 0
        self.delete = QPushButton('supprimer élève')
        self.save = QPushButton('sauvegarder')
        self.add = QPushButton('ajouter élève')
        self.repture = QLineEdit()
        self.current = QCheckBox()
        self.inscription = QLineEdit()
        self.birth_date = QLineEdit()
        self.eleve_classe = QLineEdit()
        self.full_name = QLineEdit()
        # self.first_name = QLineEdit()
        self.sex = QComboBox()
        self.father_name = QLineEdit()
        self.decision = QComboBox()
        self.liste = QTableWidget()
        self.display_all_students()
        self.eleve = QWidget()
        self.classe = QWidget()
        self.biography = QWidget()
        self.statistics = QWidget()
        self.filter = QWidget()
        self.addTab(self.eleve, 'élève')
        self.addTab(self.classe, 'classes')
        self.addTab(self.biography, 'biographie')
        self.addTab(self.statistics, 'statistiques')
        self.addTab(self.filter, "fin d'année")
        self.eleveui()
        # self.biographyUI()
        self.classeui()
        self.statisticsui()
        self.filterui()

    def display_all_students(self):
        liste_eleve = find_all_students()
        if len(liste_eleve) > 0:
            self.liste.setRowCount(len(liste_eleve))
            self.liste.setColumnCount(len(liste_eleve[0]))
            for row in range(self.liste.rowCount()):
                for column in range(self.liste.columnCount()):
                    self.liste.setItem(row, column, QTableWidgetItem(str(liste_eleve[row][column])))
        else:
            self.liste.setRowCount(0)
            self.liste.setColumnCount(0)

    def display_info(self):
        index = self.liste.currentIndex()
        new_index = self.liste.model().index(index.row(), 0)
        new_index1 = self.liste.model().index(index.row(), 1)
        # new_index2 = self.liste.model().index(index.row(), 2)
        new_index3 = self.liste.model().index(index.row(), 2)
        new_index4 = self.liste.model().index(index.row(), 3)
        new_index5 = self.liste.model().index(index.row(), 4)
        new_index6 = self.liste.model().index(index.row(), 5)
        new_index7 = self.liste.model().index(index.row(), 6)
        new_index8 = self.liste.model().index(index.row(), 7)
        new_index9 = self.liste.model().index(index.row(), 8)
        new_index10 = self.liste.model().index(index.row(), 9)
        new_index11 = self.liste.model().index(index.row(), 10)
        self.student_id = int(self.liste.model().data(new_index))
        self.full_name.setText(self.liste.model().data(new_index1))
        # self.first_name.setText(self.liste.model().data(new_index2))
        self.eleve_classe.setText(self.liste.model().data(new_index3))
        self.birth_date.setText(self.liste.model().data(new_index5))
        self.sex.setCurrentText(self.liste.model().data(new_index4))
        self.father_name.setText(self.liste.model().data(new_index6))
        self.inscription.setText(self.liste.model().data(new_index7))
        if self.liste.model().data(new_index8) == 'true':
            self.current.setChecked(True)
            self.repture.setText('')
        else:
            self.current.setChecked(False)
        if not self.current.isChecked():
            self.repture.setText(self.liste.model().data(new_index9))
        self.decision.setCurrentText(self.liste.model().data(new_index10))
        self.average.setText(self.liste.model().data(new_index11))
        self.save.setDisabled(False)
        self.delete.setDisabled(False)

    def save_change(self):
        s = str(self.current.isChecked())
        data = (self.full_name.text(), self.eleve_classe.text(), self.sex.currentText(),
                self.birth_date.text(), self.father_name.text(), self.inscription.text(), s.lower(),
                self.repture.text(), self.decision.currentText(), self.average.text(), self.student_id)
        cursor.execute(''' UPDATE eleve SET nom = ?, classe = ?, sexe = ?, date_naissance = ?, 
         nom_pere = ?, date_inscription = ?, present = ?, date_repture = ?, decision = ?, moyenne = ?  WHERE id = ? ''',
                       data)
        db.commit()
        self.display_all_students()

    def delete_student(self):
        print(self.student_id)
        cursor.execute(''' DELETE FROM eleve WHERE id = ? ''', (self.student_id,))
        db.commit()
        self.full_name.setText("")
        self.eleve_classe.setText("")
        self.birth_date.setText("")
        self.father_name.setText("")
        self.inscription.setText("")
        self.current.setChecked(False)
        self.repture.setText("")
        self.decision.setCurrentText("")
        self.average.setText("")
        self.save.setDisabled(True)
        self.delete.setDisabled(True)
        self.display_all_students()

    def persist(self):
        data = (None, self.full_name.text(), self.eleve_classe.text(), self.sex.currentText(),
                self.birth_date.text(), self.father_name.text(), self.inscription.text(),
                str(self.current.isChecked()).lower(), self.repture.text(), self.decision.currentText(),
                self.average.text())
        cursor.execute(''' INSERT INTO eleve VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', data)
        db.commit()
        self.full_name.setText("")
        # self.first_name.setText("")
        self.eleve_classe.setText("")
        self.birth_date.setText("")
        self.father_name.setText("")
        self.inscription.setText("")
        self.current.setChecked(False)
        self.repture.setText("")
        self.decision.setCurrentText("")
        self.average.setText("")
        self.display_all_students()

    def eleveui(self):
        self.liste.cellClicked.connect(self.display_info)
        buttons = QHBoxLayout()
        form = QFormLayout()
        self.save.setDisabled(True)
        self.delete.setDisabled(True)
        self.save.clicked.connect(self.save_change)
        self.delete.clicked.connect(self.delete_student)
        self.add.clicked.connect(self.persist)
        self.sex.addItem("ذكر")
        self.sex.addItem("أنثى")
        self.decision.addItem("")
        self.decision.addItem("يرتقي")
        self.decision.addItem("يرتقي بااسعاف")
        self.decision.addItem("يرسب")
        self.decision.addItem("يرفت")
        form.addRow("nom: ", self.full_name)
        # form.addRow("prénom: ", self.first_name)
        form.addRow("classe: ", self.eleve_classe)
        form.addRow("date de naissance: ", self.birth_date)
        form.addRow("sexe: ", self.sex)
        form.addRow("nom du père: ", self.father_name)
        form.addRow("date d'inscription: ", self.inscription)
        form.addRow("décision de la jury: ", self.decision)
        form.addRow("moyenne: ", self.average)
        form.addRow("présent: ", self.current)
        form.addRow("date de repture: ", self.repture)
        buttons.addWidget(self.add)
        buttons.addWidget(self.save)
        buttons.addWidget(self.delete)
        form.addRow(buttons)
        self.current.stateChanged.connect(
            lambda: self.repture.setDisabled(True) if self.current.isChecked() else self.repture.setDisabled(False)
        )
        form.setVerticalSpacing(30)
        self.layout.addWidget(self.liste)
        self.layout.addLayout(form)
        self.eleve.setLayout(self.layout)

    def add_elements(self):
        if self.level.currentText() == '':
            cursor.execute(''' SELECT nom_classe FROM classe ''')
        else:
            cursor.execute(''' SELECT nom_classe FROM classe WHERE niveau = ?''', (self.level.currentText(),))
        list_classe = cursor.fetchall()
        for i in range(self.classe_list.count()):
            self.classe_list.removeItem(0)
        for e in list_classe:
            self.classe_list.addItem(e[0])

    def find_students_by_class(self):
        classe = self.classe_list.currentText()
        cursor.execute(''' SELECT nom FROM eleve WHERE classe = ? ''', (classe,))
        liste = cursor.fetchall()
        l = [e[0] for e in liste]
        collator = icu.Collator.createInstance(icu.Locale('ar_utf8'))
        l1 = sorted(l, key=collator.getSortKey)
        return l1

    def display_students_by_class(self):
        liste_eleve = self.find_students_by_class()

        if len(liste_eleve) > 0:
            self.result.setRowCount(len(liste_eleve))
            self.result.setColumnCount(1)
            for row in range(self.result.rowCount()):
                for column in range(self.result.columnCount()):
                    self.result.setItem(row, column, QTableWidgetItem(str(liste_eleve[row])))
        else:
            self.result.setRowCount(0)
            self.result.setColumnCount(0)

    def generate_pdf(self):
        liste = self.find_students_by_class()
        pdf_file = FPDF()
        pdf_file.add_page()
        pdf_file.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf_file.set_font('DejaVu', '', 14)
        reshaped_text = arabic_reshaper.reshape(self.classe_list.currentText())  # correct its shape
        bidi_text = get_display(reshaped_text)
        pdf_file.cell(200, 6, bidi_text, ln=1, align='C')
        for e in liste:
            # print(u"ذهب الطالب الى المدرسة")
            # s = "ذهب الطالب الى المدرسة"
            reshaped_text = arabic_reshaper.reshape(e)  # correct its shape
            bidi_text = get_display(reshaped_text)
            print(bidi_text)
            pdf_file.cell(200, 6, bidi_text, ln=1, align='R', border=1)
            # pdf_file.cell(20, 5, e[1], ln=1, align="C", border=1)
            # pdf_file.write(8, e[0])
            # pdf_file.ln(8)
        pdf_file.output(self.classe_list.currentText() + ".pdf", 'F')
        pdf_file.close()

    def delete_classe(self):
        classe = self.classe_list.currentText()
        cursor.execute(''' DELETE FROM eleve WHERE classe = ? ''', (classe,))
        cursor.execute(''' DELETE FROM classe WHERE nom_classe = ? ''', (classe,))
        db.commit()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Classe supprimé avec succès")
        msg.exec_()

    def classeui(self):
        layout = QFormLayout()
        buttons = QHBoxLayout()
        sort = QPushButton("trier les élèves")
        delete = QPushButton("supprimer classe")
        add = QPushButton("ajouter classe")
        pdf = QPushButton("générer liste des élèves")
        list_students = QPushButton("lister les élèves")
        add.clicked.connect(add_class)
        delete.clicked.connect(self.delete_classe)
        buttons.addWidget(pdf)
        buttons.addWidget(list_students)
        buttons.addWidget(add)
        buttons.addWidget(delete)
        buttons.addWidget(sort)
        self.level.addItem('')
        self.level.addItem("7ème année")
        self.level.addItem("8ème année")
        self.level.addItem("9ème année")
        self.level.currentTextChanged.connect(self.add_elements)
        self.classe_list.currentTextChanged.connect(self.display_students_by_class)
        pdf.clicked.connect(self.generate_pdf)
        layout.addRow("Niveau: ", self.level)
        layout.addRow("Classe: ", self.classe_list)
        layout.addRow(buttons)
        layout.addRow("Liste: ", self.result)
        self.classe.setLayout(layout)

    @staticmethod
    def get_stats(classe, gender):
        cursor.execute(''' SELECT COUNT(*) FROM eleve WHERE classe = ? AND sexe = ? ''', (classe, gender))
        return cursor.fetchall()

    @staticmethod
    def get_all_classes_by_level(level):
        cursor.execute(''' SELECT * FROM classe WHERE niveau = ?''', (level,))
        return cursor.fetchall()

    def refresh(self):
        # refresh = QPushButton("تحيين")
        # refresh.clicked.connect(self.refresh)
        statistics_layout = QFormLayout()
        statistics_layout.addWidget(self.refresh_button)
        hbox = QHBoxLayout()
        nbr_classe7 = len(self.get_all_classes_by_level("7ème année"))
        statistics_layout.addRow("المستوى : السابعة أساسي   " + str(nbr_classe7) + " أقسام ", hbox)
        statistics_layout.addRow(
            "القسم                      ذكور                   اناث                   المجموع", hbox)
        all_males7 = 0
        all_males8 = 0
        all_males9 = 0
        all_females7 = 0
        all_females8 = 0
        all_females9 = 0
        for classe in self.get_all_classes_by_level("7ème année"):
            res_male = str(self.get_stats(classe[0], "ذكر")[0][0])
            res_femelle = str(self.get_stats(classe[0], "أنثى")[0][0])
            all_males7 += int(res_male)
            all_females7 += int(res_femelle)
            res = classe[0] + "                        " + res_male + "                      " + \
                res_femelle + "                            " + str(int(res_femelle) + int(res_male))

            statistics_layout.addRow(res, hbox)
        last = str(all_males7 + all_females7) + "                             " + str(
            all_females7) + "                          " + str(all_males7) + "                           " + str(
            nbr_classe7)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)
        statistics_layout.addRow(last, hbox)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)

        nbr_classe8 = len(self.get_all_classes_by_level("8ème année"))
        statistics_layout.addRow("المستوى : الثامنة أساسي  " + str(nbr_classe8) + " أقسام ", hbox)
        statistics_layout.addRow(
            "القسم                      ذكور                   اناث                   المجموع", hbox)
        for classe in self.get_all_classes_by_level("8ème année"):
            res_male = str(self.get_stats(classe[0], "ذكر")[0][0])
            res_femelle = str(self.get_stats(classe[0], "أنثى")[0][0])
            all_males8 += int(res_male)
            all_females8 += int(res_femelle)
            res = classe[0] + "                        " + res_male + "                      " + \
                res_femelle + "                            " + str(int(res_femelle) + int(res_male))

            statistics_layout.addRow(res, hbox)
        last = str(all_males8 + all_females8) + "                             " + str(
            all_females8) + "                          " + str(all_males8) + "                       " + str(
            nbr_classe8)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)
        statistics_layout.addRow(last, hbox)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)

        nbr_classe9 = len(self.get_all_classes_by_level("9ème année"))
        statistics_layout.addRow("المستوى : التاسعة أساسي   " + str(nbr_classe9) + " أقسام ", hbox)
        statistics_layout.addRow(
            "القسم                      ذكور                   اناث                   المجموع", hbox)
        for classe in self.get_all_classes_by_level("9ème année"):
            res_male = str(self.get_stats(classe[0], "ذكر")[0][0])
            res_femelle = str(self.get_stats(classe[0], "أنثى")[0][0])
            all_males9 += int(res_male)
            all_females9 += int(res_femelle)
            res = classe[0] + "                        " + res_male + "                      " + \
                res_femelle + "                            " + str(int(res_femelle) + int(res_male))

            statistics_layout.addRow(res, hbox)
        last = str(all_males9 + all_females9) + "                             " + str(
            all_females9) + "                           " + str(all_males9) + "                                " + str(
            nbr_classe9)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)
        statistics_layout.addRow(last, hbox)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)
        statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", hbox)

        all_males = all_males7 + all_males8 + all_males9
        all_females = all_females7 + all_females8 + all_females9
        last = str(all_males + all_females) + "                             " + str(
            all_females) + "                           " + str(all_males) + "                          " + str(
            nbr_classe7 + nbr_classe8 + nbr_classe9)
        statistics_layout.addRow(last, hbox)

        statistics_layout.setVerticalSpacing(20)

        for i in range(self.statistics_layout.rowCount()):
            self.statistics_layout.removeRow(0)

        self.statistics_layout.addRow(statistics_layout)
        self.statistics.setLayout(self.statistics_layout)

    def statisticsui(self):
        self.refresh_button.clicked.connect(self.refresh)
        self.statistics_layout.addWidget(self.refresh_button)
        nbr_classe7 = len(self.get_all_classes_by_level("7ème année"))
        self.statistics_layout.addRow("المستوى : السابعة أساسي   " + str(nbr_classe7) + " أقسام ", self.hbox1)
        self.statistics_layout.addRow(
            "القسم                      ذكور                   اناث                   المجموع", self.hbox1)
        all_males7 = 0
        all_males8 = 0
        all_males9 = 0
        all_females7 = 0
        all_females8 = 0
        all_females9 = 0
        for classe in self.get_all_classes_by_level("7ème année"):
            res_male = str(self.get_stats(classe[0], "ذكر")[0][0])
            res_femelle = str(self.get_stats(classe[0], "أنثى")[0][0])
            all_males7 += int(res_male)
            all_females7 += int(res_femelle)
            res = classe[0] + "                        " + res_male + "                      " + \
                res_femelle + "                            " + str(int(res_femelle) + int(res_male))

            self.statistics_layout.addRow(res, self.hbox1)
        last = str(all_males7 + all_females7) + "                             " + str(
            all_females7) + "                          " + str(all_males7) + "                           " + str(
            nbr_classe7)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)
        self.statistics_layout.addRow(last, self.hbox1)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)

        nbr_classe8 = len(self.get_all_classes_by_level("8ème année"))
        self.statistics_layout.addRow("المستوى : الثامنة أساسي  " + str(nbr_classe8) + " أقسام ", self.hbox1)
        self.statistics_layout.addRow(
            "القسم                      ذكور                   اناث                   المجموع", self.hbox1)
        for classe in self.get_all_classes_by_level("8ème année"):
            res_male = str(self.get_stats(classe[0], "ذكر")[0][0])
            res_femelle = str(self.get_stats(classe[0], "أنثى")[0][0])
            all_males8 += int(res_male)
            all_females8 += int(res_femelle)
            res = classe[0] + "                        " + res_male + "                      " + \
                res_femelle + "                            " + str(int(res_femelle) + int(res_male))

            self.statistics_layout.addRow(res, self.hbox1)
        last = str(all_males8 + all_females8) + "                             " + str(
            all_females8) + "                          " + str(all_males8) + "                       " + str(
            nbr_classe8)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)
        self.statistics_layout.addRow(last, self.hbox1)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)

        nbr_classe9 = len(self.get_all_classes_by_level("9ème année"))
        self.statistics_layout.addRow("المستوى : التاسعة أساسي   " + str(nbr_classe9) + " أقسام ", self.hbox1)
        self.statistics_layout.addRow(
            "القسم                      ذكور                   اناث                   المجموع", self.hbox1)
        for classe in self.get_all_classes_by_level("9ème année"):
            res_male = str(self.get_stats(classe[0], "ذكر")[0][0])
            res_femelle = str(self.get_stats(classe[0], "أنثى")[0][0])
            all_males9 += int(res_male)
            all_females9 += int(res_femelle)
            res = classe[0] + "                        " + res_male + "                      " + \
                res_femelle + "                            " + str(int(res_femelle) + int(res_male))

            self.statistics_layout.addRow(res, self.hbox1)
        last = str(all_males9 + all_females9) + "                             " + str(
            all_females9) + "                           " + str(all_males9) + "                                " + str(
            nbr_classe9)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)
        self.statistics_layout.addRow(last, self.hbox1)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)
        self.statistics_layout.addRow(
            "---------------------------------------------------------------------------------------", self.hbox1)

        all_males = all_males7 + all_males8 + all_males9
        all_females = all_females7 + all_females8 + all_females9
        last = str(all_males + all_females) + "                             " + str(
            all_females) + "                           " + str(all_males) + "                          " + str(
            nbr_classe7 + nbr_classe8 + nbr_classe9)
        self.statistics_layout.addRow(last, self.hbox1)

        self.statistics_layout.setVerticalSpacing(20)
        self.statistics.setLayout(self.statistics_layout)

    def find_students_by_criteria(self):
        criteria = self.criteria.currentText()
        classe = self.all_classes.currentText()
        if criteria == "قائمة المرتقين":
            cursor.execute(''' SELECT * FROM eleve WHERE classe = ? AND decision = ? ''', (classe, "يرتقي"))
        elif criteria == "قائمة الراسبين":
            cursor.execute(''' SELECT * FROM eleve WHERE classe = ? AND decision = ? ''', (classe, "يرسب"))
        else:
            cursor.execute(''' SELECT * FROM eleve WHERE classe = ? AND decision = ? ''', (classe, "يرفت"))
        return cursor.fetchall()

    def display_list(self):
        liste = self.find_students_by_criteria()
        liste1 = sorted(liste, key=lambda t: t[-1], reverse=True)
        if len(liste) > 0:
            self.filter_result.setRowCount(len(liste))
            self.filter_result.setColumnCount(2)
            for row in range(self.filter_result.rowCount()):
                self.filter_result.setItem(row, 0, QTableWidgetItem(str(liste1[row][1])))
                self.filter_result.setItem(row, 1, QTableWidgetItem(str(liste1[row][-1])))
        else:
            self.filter_result.setRowCount(0)
            self.filter_result.setColumnCount(0)

    @staticmethod
    def get_all_classes():
        cursor.execute(''' SELECT * FROM classe ''')
        return cursor.fetchall()

    def generate_custom_pdf(self):
        liste = self.find_students_by_criteria()
        print(liste)
        pdf_file = FPDF()
        pdf_file.add_page()
        pdf_file.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf_file.set_font('DejaVu', '', 14)
        reshaped_text = arabic_reshaper.reshape(self.all_classes.currentText())  # correct its shape
        bidi_text = get_display(reshaped_text)
        pdf_file.cell(200, 6.3, bidi_text, ln=1, align='C')
        for e in liste:
            # print(u"ذهب الطالب الى المدرسة")
            # s = "ذهب الطالب الى المدرسة"
            reshaped_text = arabic_reshaper.reshape(
                e[1] + "                              " + e[-1])  # correct its shape
            bidi_text = get_display(reshaped_text)
            print(bidi_text)
            pdf_file.cell(200, 6.3, bidi_text, ln=1, align='R', border=1)
            # pdf_file.cell(20, 5, e[1], ln=1, align="C", border=1)
            # pdf_file.write(8, e[0])
            # pdf_file.ln(8)
        pdf_file.output(self.all_classes.currentText() + " " + self.criteria.currentText() + ".pdf", 'F')
        pdf_file.close()

    def filterui(self):
        form = QFormLayout()
        generate_list = QPushButton("générer liste des élèves")
        generate_list.clicked.connect(self.generate_custom_pdf)
        self.criteria.addItem("")
        self.criteria.addItem("قائمة المرتقين")
        self.criteria.addItem("قائمة الراسبين")
        self.criteria.addItem("قائمة المنقطعين")
        for e in self.get_all_classes():
            self.all_classes.addItem(e[0])
        self.criteria.currentTextChanged.connect(self.display_list)
        self.all_classes.currentTextChanged.connect(self.display_list)
        form.addRow("Choisir une liste: ", self.criteria)
        form.addRow("Classe: ", self.all_classes)
        form.addWidget(generate_list)
        form.addRow("Liste: ", self.filter_result)
        self.filter.setLayout(form)


class Auth(QWidget):
    def __init__(self):
        super(Auth, self).__init__()
        self.form = QFormLayout()
        self.login = QLineEdit()
        self.passwd = QLineEdit()
        self.passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.validate = QPushButton("valider")
        self.validate.setShortcut("Return")
        self.validate.clicked.connect(self.authenticate)
        self.form.addRow("login: ", self.login)
        self.form.addRow("mot de passe: ", self.passwd)
        self.form.addRow(self.validate)
        self.setWindowTitle("Authentification")
        self.setLayout(self.form)

    @staticmethod
    def authenticate():
        authentication()


class_widget = QWidget()
class_widget.setGeometry(500, 250, 300, 150)
class_widget.setWindowTitle("ajouter classe")


class AddClassUi(QWidget):
    def __init__(self, parent=class_widget):
        super(AddClassUi, self).__init__(parent)
        self.form = QFormLayout()
        self.nom = QLineEdit()
        self.niveau = QComboBox()
        self.niveau.addItem("")
        self.niveau.addItem("7ème année")
        self.niveau.addItem("8ème année")
        self.niveau.addItem("9ème année")
        # self.nbr_eleve = QLineEdit()
        self.add = QPushButton("ajouter")
        self.add.clicked.connect(self.persist_class)
        self.form.addRow("nom classe: ", self.nom)
        self.form.addRow("niveau: ", self.niveau)
        # self.form.addRow("nbr élève: ", self.nbr_eleve)
        self.form.addRow(self.add)
        self.setLayout(self.form)

    def persist_class(self):
        if self.nom.text().strip() == "" or self.niveau.currentText() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Merci de remplir tous les champs")
            msg.exec_()
        else:
            try:
                data = (self.nom.text(), self.niveau.currentText())
                cursor.execute(''' INSERT INTO classe VALUES (?, ?)''', data)
                db.commit()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Classe ajouté avec succès")
                msg.exec_()
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Classe existe déja")
                msg.exec_()


def add_class():
    add = AddClassUi()
    class_widget.show()
    add.show()


db = sqlite3.connect('office.sqlite')
cursor = db.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS classe(
nom_classe varchar PRIMARY KEY ,
niveau varchar 
) ''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS eleve(
id integer PRIMARY KEY AUTOINCREMENT ,
nom varchar ,
classe varchar REFERENCES classe(nom_classe) ,
sexe varchar ,
date_naissance varchar ,
nom_pere varchar ,
date_inscription varchar ,
present varchar ,
date_repture varchar ,
decision varchar ,
moyenne varchar 
) ''')

auth = Auth()
auth.setGeometry(500, 250, 300, 110)
auth.show()
main = MainWindow()
main.setGeometry(0, 0, 1200, 1000)


def authentication():
    if auth.login.text().strip() == "saad sboui" and auth.passwd.text() == "00000000":
        auth.destroy()
        main.show()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Login ou mot de passe incorrect")
        msg.exec_()


sys.exit(app.exec_())

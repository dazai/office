# -*- coding: utf-8 -*-

import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QAction, QWidget, QTabWidget, \
    QLineEdit, QComboBox, QFormLayout, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem

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
        file.triggered[QAction].connect(self.processtrigger)
        self.setWindowTitle("office")
        tabs = Tabs(self)
        self.setCentralWidget(tabs)

    def processtrigger(self):
        pass


def find_all_students():
    cursor.execute(''' SELECT * FROM eleve ''')
    return cursor.fetchall()


def display_all_students():
    liste_eleve = find_all_students()
    print(liste_eleve)
    liste = QTableWidget()
    if len(liste_eleve) > 0:
        liste.setRowCount(len(liste_eleve))
        liste.setColumnCount(len(liste_eleve[0]))
        for row in range(liste.rowCount()):
            for column in range(liste.columnCount()):
                liste.setItem(row, column, QTableWidgetItem(str(liste_eleve[row][column])))
        return liste
    return QTableWidget()


class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)
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
        self.last_name = QLineEdit()
        self.first_name = QLineEdit()
        self.sex = QComboBox()
        self.father_name = QLineEdit()
        self.liste = display_all_students()
        self.eleve = QWidget()
        self.classe = QWidget()
        self.biography = QWidget()
        self.statistics = QWidget()
        self.addTab(self.eleve, 'élève')
        self.addTab(self.classe, 'classes')
        self.addTab(self.biography, 'biographie')
        self.addTab(self.statistics, 'statistiques')
        self.eleveui()
        # self.biographyUI()
        self.classeui()
        # self.statisticsUI()

    def display_info(self):
        index = self.liste.currentIndex()
        new_index = self.liste.model().index(index.row(), 0)
        new_index1 = self.liste.model().index(index.row(), 1)
        new_index2 = self.liste.model().index(index.row(), 2)
        new_index3 = self.liste.model().index(index.row(), 3)
        new_index4 = self.liste.model().index(index.row(), 4)
        new_index5 = self.liste.model().index(index.row(), 5)
        new_index6 = self.liste.model().index(index.row(), 6)
        new_index7 = self.liste.model().index(index.row(), 7)
        new_index8 = self.liste.model().index(index.row(), 8)
        new_index9 = self.liste.model().index(index.row(), 9)
        self.student_id = int(self.liste.model().data(new_index))
        self.last_name.setText(self.liste.model().data(new_index1))
        self.first_name.setText(self.liste.model().data(new_index2))
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
        self.save.setDisabled(False)
        self.delete.setDisabled(False)

    def save_change(self):
        s = str(self.current.isChecked())
        data = (self.last_name.text(), self.first_name.text(), self.eleve_classe.text(), self.sex.currentText(),
                self.birth_date.text(), self.father_name.text(), self.inscription.text(), s.lower(),
                self.repture.text(), self.student_id)
        cursor.execute(''' UPDATE eleve SET nom = ?, prenom = ?, classe = ?, sexe = ?, date_naissance = ?, 
         nom_pere = ?, date_inscription = ?, present = ?, date_repture = ? WHERE id = ? ''', data)
        db.commit()

    def delete_student(self):
        print(self.student_id)
        cursor.execute(''' DELETE FROM eleve WHERE id = ? ''', (self.student_id,))
        db.commit()

    def persist(self):
        data = (None, self.last_name.text(), self.first_name.text(), self.eleve_classe.text(), self.sex.currentText(),
                self.birth_date.text(), self.father_name.text(), self.inscription.text(),
                str(self.current.isChecked()).lower(), self.repture.text())
        cursor.execute(''' INSERT INTO eleve VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', data)
        db.commit()

    def eleveui(self):
        self.liste.cellClicked.connect(self.display_info)
        buttons = QHBoxLayout()
        form = QFormLayout()
        self.save.setDisabled(True)
        self.delete.setDisabled(True)
        self.save.clicked.connect(self.save_change)
        self.delete.clicked.connect(self.delete_student)
        self.add.clicked.connect(self.persist)
        self.sex.addItem("Male")
        self.sex.addItem("Femelle")
        form.addRow("nom: ", self.last_name)
        form.addRow("prénom: ", self.first_name)
        form.addRow("classe: ", self.eleve_classe)
        form.addRow("date de naissance: ", self.birth_date)
        form.addRow("sexe: ", self.sex)
        form.addRow("nom du père: ", self.father_name)
        form.addRow("date d'inscription: ", self.inscription)
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
            cursor.execute(''' SELECT nom_classe FROM classe WHERE niveau = ?''', (self.level.currentText(), ))
        list_classe = cursor.fetchall()
        for i in range(self.classe_list.count()):
            self.classe_list.removeItem(0)
        for e in list_classe:
            self.classe_list.addItem(e[0])

    def find_students_by_class(self):
        classe = self.classe_list.currentText()
        cursor.execute(''' SELECT * FROM eleve WHERE classe = ? ''', (classe,))
        return cursor.fetchall()

    def display_students_by_class(self):
        liste_eleve = self.find_students_by_class()
        if len(liste_eleve) > 0:
            self.result.setRowCount(len(liste_eleve))
            self.result.setColumnCount(len(liste_eleve[0]))
            for row in range(self.result.rowCount()):
                for column in range(self.result.columnCount()):
                    self.result.setItem(row, column, QTableWidgetItem(str(liste_eleve[row][column])))

    def classeui(self):
        layout = QFormLayout()
        buttons = QHBoxLayout()
        sort = QPushButton("trier les élèves")
        delete = QPushButton("supprimer classe")
        add = QPushButton("ajouter classe")
        list_classes = QPushButton("lister les classes")
        list_students = QPushButton("lister les élèves")
        buttons.addWidget(list_classes)
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
        layout.addRow("Niveau: ", self.level)
        layout.addRow("Classe: ", self.classe_list)
        layout.addRow(buttons)
        layout.addRow("Liste: ", self.result)
        self.classe.setLayout(layout)


db = sqlite3.connect('office.sqlite')
cursor = db.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS classe(
nom_classe varchar PRIMARY KEY ,
niveau varchar ,
nbr_eleve integer 
) ''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS eleve(
id integer PRIMARY KEY AUTOINCREMENT ,
nom varchar ,
prenom varchar ,
classe varchar REFERENCES classe(nom_classe) ,
sexe varchar ,
date_naissance varchar ,
nom_pere varchar ,
date_inscription varchar ,
present varchar ,
date_repture varchar 
) ''')

main = MainWindow()
main.setGeometry(0, 0, 1200, 1000)
main.show()
sys.exit(app.exec_())

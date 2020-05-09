# -*- coding: utf-8 -*-

import sys
import sqlite3

from PyQt5 import QtSql, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QAction, QWidget, QTabWidget, \
    QTableView, QLineEdit, QComboBox, QFormLayout, QCheckBox, QPushButton, QListView, QTableWidget, QTableWidgetItem

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
    liste = QTableWidget()
    liste.setRowCount(len(liste_eleve))
    liste.setColumnCount(len(liste_eleve[1]))
    for row in range(liste.rowCount()):
        for column in range(liste.columnCount()):
            liste.setItem(row, column, QTableWidgetItem(str(liste_eleve[row][column])))
    return liste


class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)
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

    def function(self):
        index = self.liste.currentIndex()
        new_index1 = self.liste.model().index(index.row(), 1)
        new_index2 = self.liste.model().index(index.row(), 2)
        new_index3 = self.liste.model().index(index.row(), 3)
        new_index4 = self.liste.model().index(index.row(), 4)
        new_index5 = self.liste.model().index(index.row(), 5)
        new_index6 = self.liste.model().index(index.row(), 6)
        new_index7 = self.liste.model().index(index.row(), 7)
        new_index8 = self.liste.model().index(index.row(), 8)
        new_index9 = self.liste.model().index(index.row(), 9)
        self.first_name.setText(self.liste.model().data(new_index1))
        self.last_name.setText(self.liste.model().data(new_index2))
        self.eleve_classe.setText(self.liste.model().data(new_index3))
        self.birth_date.setText(self.liste.model().data(new_index5))
        self.sex.setCurrentText(self.liste.model().data(new_index4))
        self.father_name.setText(self.liste.model().data(new_index6))
        self.inscription.setText(self.liste.model().data(new_index7))
        if self.liste.model().data(new_index8) == 'true':
            self.current.setChecked(True)
        else:
            self.current.setChecked(False)
        if not self.current.isChecked():
            self.repture.setText(self.liste.model().data(new_index9))

    def eleveui(self):
        self.liste.cellClicked.connect(self.function)
        layout = QHBoxLayout()
        buttons = QHBoxLayout()
        form = QFormLayout()
        add = QPushButton('ajouter élève')
        persist = QPushButton('sauvegarder')
        delete = QPushButton('supprimer élève')
        add.setDisabled(True)
        persist.setDisabled(True)
        delete.setDisabled(True)
        self.sex.addItem("Male")
        self.sex.addItem("Femelle")
        form.addRow("nom: ", self.first_name)
        form.addRow("prénom: ", self.last_name)
        form.addRow("classe: ", self.eleve_classe)
        form.addRow("date de naissance: ", self.birth_date)
        form.addRow("sexe: ", self.sex)
        form.addRow("nom du père: ", self.father_name)
        form.addRow("date d'inscription: ", self.inscription)
        form.addRow("présent: ", self.current)
        form.addRow("date de repture: ", self.repture)
        buttons.addWidget(add)
        buttons.addWidget(persist)
        buttons.addWidget(delete)
        form.addRow(buttons)
        self.current.stateChanged.connect(
            lambda: self.repture.setDisabled(True) if self.current.isChecked() else self.repture.setDisabled(False)
        )
        form.setVerticalSpacing(30)
        layout.addWidget(self.liste)
        layout.addLayout(form)
        self.eleve.setLayout(layout)

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
        level = QComboBox()
        level.addItem('')
        level.addItem("7ème année")
        level.addItem("8ème année")
        level.addItem("9ème année")
        level.currentTextChanged.connect(lambda: print(level.currentText()))
        classe = QComboBox()
        result = QListView()
        layout.addRow("Niveau: ", level)
        layout.addRow("Classe: ", classe)
        layout.addRow(buttons)
        layout.addRow("Liste: ", result)
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

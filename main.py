# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QAction, QWidget, QTabWidget, \
    QTableView, QLineEdit, QComboBox, QFormLayout, QCheckBox, QPushButton

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
    pass


class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)
        self.repture = QLineEdit()
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
        # self.classeUI()
        # self.statisticsUI()

    def eleveui(self):
        find_all_students()
        layout = QHBoxLayout()
        buttons = QHBoxLayout()
        form = QFormLayout()
        add = QPushButton('ajouter élève')
        persist = QPushButton('sauvegarder')
        delete = QPushButton('supprimer élève')
        add.setDisabled(True)
        persist.setDisabled(True)
        delete.setDisabled(True)
        model = QtSql.QSqlTableModel()
        model.setHeaderData(0, Qt.Horizontal,  "ID")
        model.setHeaderData(1, Qt.Horizontal, "First name")
        model.setHeaderData(2, Qt.Horizontal, "Last name")
        view = QTableView()
        view.setModel(model)
        first_name = QLineEdit()
        last_name = QLineEdit()
        classe = QLineEdit()
        birth_date = QLineEdit()
        inscription = QLineEdit()
        current = QCheckBox()
        sex = QComboBox()
        sex.addItem("Male")
        sex.addItem("Femelle")
        father_name = QLineEdit()
        form.addRow("nom: ", first_name)
        form.addRow("prénom: ", last_name)
        form.addRow("classe: ", classe)
        form.addRow("date de naissance: ", birth_date)
        form.addRow("sexe: ", sex)
        form.addRow("nom du père: ", father_name)
        form.addRow("date d'inscription: ", inscription)
        form.addRow("présent: ", current)
        form.addRow("date de repture: ", self.repture)
        buttons.addWidget(add)
        buttons.addWidget(persist)
        buttons.addWidget(delete)
        form.addRow(buttons)
        current.stateChanged.connect(lambda: self.set_repture(current))
        form.setVerticalSpacing(30)
        layout.addWidget(view)
        layout.addLayout(form)
        self.eleve.setLayout(layout)

    def set_repture(self, btn):
        if btn.isChecked():
            self.repture.setDisabled(True)
        else:
            self.repture.setDisabled(False)


main = MainWindow()
main.setGeometry(0, 0, 1200, 1000)
main.show()
sys.exit(app.exec_())

import sys
import sqlite3

from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
from PyQt6 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.loadTable)
        self.addButton.clicked.connect(self.openEditor)

    def loadTable(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT Items.id, Name.coffeename, Roasting.degree,
        ground, taste, price, volume FROM Items
        JOIN Roasting ON Roasting.id = Items.roasting
        JOIN Name ON Name.id = Items.name""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'название', 'обжарка', 'молотый?', 'вкус', 'цена (руб)', 'вес (гр)'])
        self.tableWidget.resizeColumnsToContents()

    def openEditor(self):
        self.editorForm = EditorForm()
        self.editorForm.show()

class EditorForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.okButton.clicked.connect(self.addData)

    def addData(self):
        try:
            self.cur.execute(self.request.toPlainText())
            self.con.commit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())

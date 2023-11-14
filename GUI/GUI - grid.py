import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("une premiere fenetre")
        self.setLayout(QGridLayout())
        self.resize(250,100)
        lblTemp = QLabel("Température")

        tbxTemperature=QLineEdit()
        self.QlineEdit = QLineEdit(tbxTemperature)
        self.QlineEdit.setValidator(QIntValidator())
        self.QlineEdit.setObjectName("temperature")
        self.QlineEdit.setText("")



        my_label2 = QLabel("")
        my_button = QPushButton("OK",clicked =lambda: ok())

        cbxconversionType=QComboBox()
        cbxconversionType.addItem("°C -> °K")
        cbxconversionType.addItem("°K -> °C")


        my_button2 = QPushButton("Quitter",clicked =lambda: quit())

        self.layout().addWidget(lblTemp,0, 0)
        self.layout().addWidget(self.QlineEdit,0, 1)
        self.layout().addWidget(my_label2,1, 0)
        self.layout().addWidget(my_button,1, 1)
        self.layout().addWidget(cbxconversionType,1,2)
        self.layout().addWidget(my_button2,2, 2)

        def ok():

            
                if self.QlineEdit.text() > -273 :
                    my_label2.setText(f'Bonjour {self.QlineEdit.text().text()}')






        self.show()


if __name__ == '__main__':
    app=QApplication([])
    mw=MainWindows()
    app.exec()
import sys
from PyQt5.QtWidgets import *

class MainWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("une premiere fenetre")
        self.setLayout(QGridLayout())
        self.resize(250,100)
        my_label = QLabel("Saisir votre nom :")
        my_entry=QLineEdit()
        my_entry.setObjectName("nom")
        my_entry.setText("")
        my_label2 = QLabel("")
        my_button = QPushButton("OK",clicked =lambda: ok())
        my_button2= QPushButton("Quitter",clicked =lambda: quit())

        self.layout().addWidget(my_label,0, 0)
        self.layout().addWidget(my_entry,0, 1)
        self.layout().addWidget(my_label2,1, 0)
        self.layout().addWidget(my_button,1, 1)
        self.layout().addWidget(my_button2,2, 2)

        def ok():
            if my_entry.text() !="":
                my_label2.setText(f'Bonjour {my_entry.text()}')
                my_entry.setText("")



        self.show()


if __name__ == '__main__':
    app=QApplication([])
    mw=MainWindows()
    app.exec()
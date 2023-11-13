import sys
from PyQt5.QtWidgets import *
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QLabel("Saisir votre nom :"))
layout.addWidget(QLineEdit())
layout.addWidget(QPushButton("valider"))
layout.addWidget(QLabel())
layout.addWidget(QPushButton("Quitter"))

window.setLayout(layout)
window.show()

if __name__ == '__main__':
    sys.exit(app.exec_())
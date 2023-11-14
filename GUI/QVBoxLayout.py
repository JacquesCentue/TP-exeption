import sys
from PyQt5.QtWidgets import *
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QLabel("Saisir votre nom :"))
layout.addWidget(QLineEdit())
ok = layout.addWidget(QPushButton("valider"))
layout.addWidget(QLabel())
quit = layout.addWidget(QPushButton("Quitter"))



window.setLayout(layout)
window.show()
def __actionQuitter(self):
    app.exit(0)

if __name__ == '__main__':
    sys.exit(app.exec_())
    quit.clicked.connect(__actionQuitter)
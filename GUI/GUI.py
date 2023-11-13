import sys
from PyQt5.QtWidgets import QApplication, QWidget,QVBoxLayout
from PyQt5 import *
app = QApplication(sys.argv)
root = QWidget()
root.resize(250, 250)
root.setWindowTitle("test")
root.setLayout(QVBoxLayout())
QVBoxLayout.addWidget(PyQt5.Qlabel)

root.show()
if __name__ == '__main__':
    sys.exit(app.exec_())
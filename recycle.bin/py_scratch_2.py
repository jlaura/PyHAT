# import sys
# from PyQt4.QtGui import QApplication
# from PyQt4.QtGui import QSpinBox
# from PyQt4.QtGui import QVBoxLayout
# from PyQt4.QtGui import QWidget
#
#
# class SpinboxWidget(QWidget):
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent)
#         self.layout = QVBoxLayout()
#         self.addSpinboxes(10)
#         self.setLayout(self.layout)
#
#     def addSpinboxes(self, n):
#         spb = []
#         for i in range(n):
#             spinbox = QSpinBox()
#             spinbox.setMaximum(1000)
#             spb.append(spinbox)
#             self.layout.addWidget(spinbox)
#
#         for i in range(n-1):
#             spb[i].valueChanged.connect(spb[i + 1].setMinimum)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setStyle('plastique')
#     widget = SpinboxWidget()
#     widget.setWindowTitle('Spinbox Tester')
#     widget.show()
#
# sys.exit(app.exec_())
#
# class A:
#     def f(self):
#         print('f')
#
#     def g(self):
#         print('g')
#
#
# a1 = A()
# # a2 = A()
#
# # aList = [a1.f, a2.g]
# aList = [a1.f, a1.g]
#
# print(a1.f in aList)
# print(a1.g in aList)
# # print(a2.f in aList)
# # print(a2.g in aList)
=======
import sys
from PyQt4 import QtGui, QtCore
from pysat_ui import *
count = 1

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI(self)

    def initUI(self, MainWindow):
        pysat_ui.mainframe(self, MainWindow)
        button = QtGui.QPushButton('close',)



def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


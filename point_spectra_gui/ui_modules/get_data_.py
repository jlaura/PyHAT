from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class get_data_u_:
    def __init__(self, pysat_fun, module_layout, arg_list, kw_list):
        self.pysat_fun = pysat_fun
        self.module_layout = module_layout
        self.arg_list = arg_list
        self.kw_list = kw_list
        self.ui_id = None
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.get_data_ui()  # initiate the UI
        self.pysat_fun.set_greyed_modules(self.get_data)
        try:
            self.get_data_button.clicked.connect(lambda: self.on_getDataButton_clicked(self.get_data_line_edit,
                                                                                       "unknown"))  # when a button is clicked call the on_getDataButton_clicked function
        except:
            pass

    def get_data_ui(self):
        self.get_data = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.get_data.setFont(font)
        self.get_data.setObjectName(_fromUtf8("get_data"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.get_data)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.get_data_label = QtGui.QLabel(self.get_data)
        self.get_data_label.setObjectName(_fromUtf8("get_data_label"))
        self.horizontalLayout.addWidget(self.get_data_label)
        self.get_data_line_edit = QtGui.QLineEdit(self.get_data)
        self.get_data_line_edit.setReadOnly(True)
        self.get_data_line_edit.setObjectName(_fromUtf8("get_data_line_edit"))
        self.horizontalLayout.addWidget(self.get_data_line_edit)
        self.get_data_button = QtGui.QToolButton(self.get_data)
        self.get_data_button.setObjectName(_fromUtf8("get_data_button"))
        self.horizontalLayout.addWidget(self.get_data_button)
        self.module_layout.addWidget(self.get_data)

        self.get_data.setTitle(_translate("MainWindow", "Load Unknown Data", None))
        self.get_data_label.setText(_translate("MainWindow", "File Name", None))
        self.get_data_button.setText(_translate("MainWindow", "...", None))
        self.set_data_parameters()

    def set_data_parameters(self):
        if self.arg_list is None:
            self.get_data_line_edit.setText(_translate("MainWindow", "*.csv", None))
        else:
            # the 0'th element has the name of the file that we want to work with.
            self.get_data_line_edit.setText(self.arg_list[0])
            self.push_parameters(self.arg_list, self.kw_list)

    def push_parameters(self, arg_list, kw_list):
        ui_list = "get_known_data"
        fun_list = "get_data"
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, arg_list, kw_list, self.ui_id)

    def on_getDataButton_clicked(self, lineEdit, key):
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open " + key + " Data File", '.', "(*.csv)")
        lineEdit.setText(filename)
        if lineEdit.text() == "":
            lineEdit.setText("*.csv")
        self.push_parameters([filename, key], {})


class get_data_k_:
    def __init__(self, pysat_fun, module_layout, arg_list, kw_list):
        self.pysat_fun = pysat_fun
        self.module_layout = module_layout
        self.arg_list = arg_list
        self.kw_list = kw_list
        self.ui_id = None
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.get_data_ui()  # initiate the UI
        self.pysat_fun.set_greyed_modules(self.get_data)
        try:
            self.get_data_button.clicked.connect(lambda: self.on_getDataButton_clicked(self.get_data_line_edit,
                                                                                       "known"))  # when a button is clicked call the on_getDataButton_clicked function
        except:
            pass

    def get_data_ui(self):
        self.get_data = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.get_data.setFont(font)
        self.get_data.setObjectName(_fromUtf8("get_data"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.get_data)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.get_data_label = QtGui.QLabel(self.get_data)
        self.get_data_label.setObjectName(_fromUtf8("get_data_label"))
        self.horizontalLayout.addWidget(self.get_data_label)
        self.get_data_line_edit = QtGui.QLineEdit(self.get_data)
        self.get_data_line_edit.setReadOnly(True)
        self.get_data_line_edit.setObjectName(_fromUtf8("get_data_line_edit"))
        self.horizontalLayout.addWidget(self.get_data_line_edit)
        self.get_data_button = QtGui.QToolButton(self.get_data)
        self.get_data_button.setObjectName(_fromUtf8("get_data_button"))
        self.horizontalLayout.addWidget(self.get_data_button)
        self.module_layout.addWidget(self.get_data)

        self.get_data.setTitle(_translate("MainWindow", "Load Known Data", None))
        self.get_data_label.setText(_translate("MainWindow", "File Name", None))
        self.get_data_button.setText(_translate("MainWindow", "...", None))
        self.set_data_parameters()

    def set_data_parameters(self):
        if self.arg_list is None:
            self.get_data_line_edit.setText(_translate("MainWindow", "*.csv", None))
        else:
            # the 0'th element has the name of the file that we want to work with.
            self.get_data_line_edit.setText(self.arg_list[0])
            self.push_parameters(self.arg_list, self.kw_list)

    def push_parameters(self, arg_list, kw_list):
        ui_list = "get_known_data"
        fun_list = "get_data"
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, arg_list, kw_list, self.ui_id)

    def on_getDataButton_clicked(self, lineEdit, key):
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open " + key + " Data File", '.', "(*.csv)")
        lineEdit.setText(filename)
        if lineEdit.text() == "":
            lineEdit.setText("*.csv")
        self.push_parameters([filename, key], {})

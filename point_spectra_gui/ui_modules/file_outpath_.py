from PyQt4 import QtCore, QtGui

try:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, QtGui.QApplication.UnicodeUTF8)

except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class file_outpath_:
    def __init__(self, pysat_fun, module_layout, arg_list, kw_list):
        self.ui_id = None
        self.pysat_fun = pysat_fun
        self.arg_list = arg_list
        self.kw_list = kw_list
        self.module_layout = module_layout
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.file_outpath_ui()
        self.pysat_fun.set_greyed_modules(self.file_out_path)
        try:
            self.file_out_path_button.clicked.connect(self.on_outPutLocationButton_clicked)
        except:
            pass

    def file_outpath_ui(self):
        self.file_out_path = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.file_out_path.setFont(font)
        self.file_out_path.setObjectName("file_out_path")
        self.horizontalLayout = QtGui.QHBoxLayout(self.file_out_path)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_out_path_label = QtGui.QLabel(self.file_out_path)
        self.file_out_path_label.setObjectName("file_out_path_label")
        self.horizontalLayout.addWidget(self.file_out_path_label)
        self.file_out_path_line_edit = QtGui.QLineEdit(self.file_out_path)
        self.file_out_path_line_edit.setReadOnly(True)  # User can't edit this line
        self.file_out_path_line_edit.setObjectName("file_out_path_line_edit")
        self.horizontalLayout.addWidget(self.file_out_path_line_edit)
        self.file_out_path_button = QtGui.QToolButton(self.file_out_path)
        self.file_out_path_button.setObjectName("file_out_path_button")
        self.horizontalLayout.addWidget(self.file_out_path_button)
        self.module_layout.addWidget(self.file_out_path)

        self.file_out_path.setTitle(_translate("MainWindow", "Ouput Folder", None))
        self.file_out_path_label.setText(_translate("MainWindow", "Folder Name", None))
        self.file_out_path_line_edit.setText(_translate("MainWindow", "*/", None))
        self.file_out_path_button.setText(_translate("MainWindow", "...", None))
        self.set_parameters()

    def set_parameters(self):
        if self.arg_list is not None:
            self.file_out_path_line_edit.setText(self.arg_list[0])
            self.push_parameters()

    def push_parameters(self):
        filename = self.file_out_path_line_edit.text()
        ui_list = "file_outpath"
        fun_list = "set_file_outpath"
        kw_list = {}
        arg_list = [filename]
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, arg_list, kw_list, self.ui_id)
        pass

    def on_outPutLocationButton_clicked(self):
        filename = QtGui.QFileDialog.getExistingDirectory(None, "Select Output Directory", '.')
        self.file_out_path_line_edit.setText(filename)
        if self.file_out_path_line_edit.text() == "":
            self.file_out_path_line_edit.setText("*/")
        self.push_parameters()

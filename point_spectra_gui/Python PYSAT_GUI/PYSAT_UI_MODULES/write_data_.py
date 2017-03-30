from PyQt4 import QtCore, QtGui
from pysat.utils.gui_utils import make_combobox
from PYSAT_UI_MODULES.Error_ import error_print

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


class write_data_:
    def __init__(self, pysat_fun, module_layout):
        self.pysat_fun = pysat_fun
        self.ui_id = None
        self.module_layout = module_layout
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.write_data_ui()
        self.pysat_fun.set_greyed_modules(self.write_data)

    def get_write_params(self):
        datakey=self.write_data_choose_data.currentText()
        filename=self.write_data_file.text()

        args=[filename,datakey]
        kws={}
        ui_list = 'do_write_data'
        fun_list = 'do_write_data'
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, args, kws, self.ui_id)

    def write_data_ui(self):
        self.write_data = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.write_data.setFont(font)
        self.write_data_vlayout = QtGui.QVBoxLayout(self.write_data)

        self.write_data_choose_data_label = QtGui.QLabel(self.write_data)
        self.write_data_choose_data_label.setText(_translate("write_data", "Choose data set to write to .csv:", None))
        self.write_data_vlayout.addWidget(self.write_data_choose_data_label)

        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No data has been loaded!')
            datachoices = ['No data has been loaded!']
        self.write_data_choose_data = make_combobox(datachoices)
        self.write_data_vlayout.addWidget(self.write_data_choose_data)

        self.write_data_linedit_label=QtGui.QLabel(self.write_data)
        self.write_data_linedit_label.setText('Specify a filename:')
        self.write_data_vlayout.addWidget(self.write_data_linedit_label)

        self.write_data_file=QtGui.QLineEdit(self.write_data)
        self.write_data_file.setText('output.csv')
        self.write_data_vlayout.addWidget(self.write_data_file)

        self.module_layout.addWidget(self.write_data)
        self.write_data.raise_()
        self.write_data.setTitle(_translate("MainWindow", "Write to CSV", None))

        self.write_data_choose_data.currentIndexChanged.connect(lambda: self.get_write_params())
        self.write_data_file.textChanged.connect(lambda: self.get_write_params())
        self.get_write_params()

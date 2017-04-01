from PyQt4 import QtCore, QtGui
from pysat.utils.gui_utils import make_combobox
from ui_modules import error_print

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

class get_mask_:
    def __init__(self, pysat_fun, module_layout, arg_list, kw_list):
        self.pysat_fun = pysat_fun
        self.arg_list = arg_list
        self.kw_list = kw_list
        self.module_layout = module_layout
        self.ui_id = None
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.get_mask_ui()
        self.pysat_fun.set_greyed_modules(self.get_mask)

    def get_mask_params(self):
        datakey = self.mask_choosedata.currentText()
        maskfile = self.get_mask_line_edit.text()
        ui_list = "do_mask"
        fun_list = "do_mask"
        args = [datakey, maskfile]
        kws = {}
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, args, kws, self.ui_id)

    def get_mask_ui(self):
        self.get_mask = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.get_mask.setFont(font)
        self.get_mask.setObjectName(_fromUtf8("get_mask"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.get_mask)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.choosedata_label = QtGui.QLabel(self.get_mask)
        self.choosedata_label.setObjectName(_fromUtf8("choosedata_label"))
        self.horizontalLayout.addWidget(self.choosedata_label)
        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No data has been loaded!')
            datachoices = ['No data has been loaded!']
        self.mask_choosedata = make_combobox(datachoices)
        self.horizontalLayout.addWidget(self.mask_choosedata)

        self.get_mask_label = QtGui.QLabel(self.get_mask)
        self.get_mask_label.setObjectName(_fromUtf8("get_mask_label"))
        self.horizontalLayout.addWidget(self.get_mask_label)
        self.get_mask_line_edit = QtGui.QLineEdit(self.get_mask)
        self.get_mask_line_edit.setReadOnly(True)
        self.get_mask_line_edit.setObjectName(_fromUtf8("get_mask_line_edit"))
        self.horizontalLayout.addWidget(self.get_mask_line_edit)
        self.get_mask_button = QtGui.QToolButton(self.get_mask)
        self.get_mask_button.setObjectName(_fromUtf8("get_mask_button"))
        self.horizontalLayout.addWidget(self.get_mask_button)
        self.module_layout.addWidget(self.get_mask)

        self.get_mask.setTitle(_translate("MainWindow", "Mask Data", None))
        self.choosedata_label.setText(_translate("MainWindow", "Choose data: ", None))
        self.get_mask_label.setText(_translate("MainWindow", "Mask file: ", None))
        self.get_mask_line_edit.setText(_translate("MainWindow", "*.csv", None))
        self.get_mask_button.setText(_translate("MainWindow", "...", None))
        self.get_mask_line_edit.textChanged.connect(lambda: self.get_mask_params())
        self.mask_choosedata.currentIndexChanged.connect(lambda: self.get_mask_params())
        self.get_mask_button.clicked.connect(lambda: self.on_getDataButton_clicked(self.get_mask_line_edit))
        self.set_mask_params()

    def set_mask_params(self):
        if self.arg_list is None:
            self.get_mask_line_edit.setText(_translate("MainWindow", "*.csv", None))
        else:
            self.get_mask_line_edit.setText(self.arg_list[1])
            index = self.mask_choosedata.findText(str(self.arg_list[0]))  # findText 'unknown' or 'known'
            if index is not -1:  # if it's there choose it based on the returned index
                self.mask_choosedata.setCurrentIndex(index)

    def on_getDataButton_clicked(self, lineEdit):
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open Mask Data File", '.', "(*.csv)")
        lineEdit.setText(filename)
        if lineEdit.text() == "":
            lineEdit.setText("*.csv")

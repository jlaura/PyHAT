from PyQt4 import QtCore, QtGui
from ui_modules.Error_ import error_print
from pysat.utils.gui_utils import make_combobox

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class interpolation_:
    def __init__(self, pysat_fun, module_layout, arg_list, kw_list):
        self.pysat_fun = pysat_fun
        self.module_layout = module_layout
        self.arg_list = arg_list
        self.kw_list = kw_list
        self.ui_id = None
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.interpolation_ui()
        self.pysat_fun.set_greyed_modules(self.Interpolation)
        self.interpoliation_choosedata.currentIndexChanged.connect(lambda: self.get_parameters())
        self.interpolation_choosedata_2.currentIndexChanged.connect(lambda: self.get_parameters())

    def interpolation_ui(self):
        # TODO have the comboboxes called
        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No Data has been loaded')
            datachoices = ['No data has been loaded!']
        self.Interpolation = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Interpolation.setFont(font)
        self.Interpolation.setObjectName("Interpolation")
        self.verticalLayout = QtGui.QVBoxLayout(self.Interpolation)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.choosedata_layout = QtGui.QHBoxLayout()
        self.choosedata_layout.setMargin(11)
        self.choosedata_layout.setSpacing(6)
        self.choosedata_layout.setObjectName("choosedata_layout")
        self.interpolation_choosedata_label = QtGui.QLabel(self.Interpolation)
        self.interpolation_choosedata_label.setObjectName("interpolation_choosedata_label")
        self.choosedata_layout.addWidget(self.interpolation_choosedata_label)
        self.interpoliation_choosedata = make_combobox(datachoices)
        self.interpoliation_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.interpoliation_choosedata.setObjectName("interpolation_choosedata")
        self.choosedata_layout.addWidget(self.interpoliation_choosedata)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.choosedata_layout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.choosedata_layout)
        self.choosedata_layout_2 = QtGui.QHBoxLayout()
        self.choosedata_layout_2.setMargin(11)
        self.choosedata_layout_2.setSpacing(6)
        self.choosedata_layout_2.setObjectName("choosedata_layout_2")
        self.interpolation_choosedata_label_2 = QtGui.QLabel(self.Interpolation)
        self.interpolation_choosedata_label_2.setObjectName("interpolation_choosedata_label_2")
        self.choosedata_layout_2.addWidget(self.interpolation_choosedata_label_2)
        self.interpolation_choosedata_2 = make_combobox(datachoices)
        self.interpolation_choosedata_2.setIconSize(QtCore.QSize(50, 20))
        self.interpolation_choosedata_2.setObjectName("interpolation_choosedata_2")
        self.choosedata_layout_2.addWidget(self.interpolation_choosedata_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.choosedata_layout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.choosedata_layout_2)
        self.module_layout.addWidget(self.Interpolation)

        self.Interpolation.setTitle(_translate("MainWindow", "Interpolation", None))
        self.interpolation_choosedata_label.setText(_translate("MainWindow", "Choose data to interpolate: ", None))
        self.interpolation_choosedata_label_2.setText(_translate("MainWindow", "Choose data to use as reference: ", None))
        self.set_parameters()

    def set_parameters(self):
        if self.arg_list is not None:
            index = self.interpoliation_choosedata.findText(str(self.arg_list[0]))
            index2 = self.interpolation_choosedata_2.findText(str(self.arg_list[1]))
            if index is not -1 and index2 is not -1:
                self.interpoliation_choosedata.setCurrentIndex(index)
                self.interpolation_choosedata_2.setCurrentIndex(index2)
            self.get_parameters()

    def get_parameters(self):
        key1 = self.interpoliation_choosedata.currentText()
        key2 = self.interpolation_choosedata_2.currentText()
        # arg_list.append(['unknown data','known data'])
        args = [key1, key2]
        kws = {}
        self.push_parameters(args, kws)

    def push_parameters(self, arg_list, kw_list):
        ui_list = "do_interp"
        fun_list = "do_interp"
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, arg_list, kw_list, self.ui_id)
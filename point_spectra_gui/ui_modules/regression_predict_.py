from ui_modules.Error_ import error_print
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


class regression_predict_:
    def __init__(self, pysat_fun, module_layout,arg_list,kw_list):
        self.pysat_fun = pysat_fun
        self.ui_id = None
        self.module_layout = module_layout
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.regression_ui()
        self.pysat_fun.set_greyed_modules(self.regression_predict)

        self.regression_predict_choosedata.currentIndexChanged.connect(lambda: self.get_predict_parameters())
        self.regression_predict_choosemodel.currentIndexChanged.connect(lambda: self.get_predict_parameters())

    def get_predict_parameters(self):

        datakey = self.regression_predict_choosedata.currentText()
        modelkey = self.regression_predict_choosemodel.currentText()
        predictname = ('meta', modelkey + ' - ' + datakey + ' - Predict')

        args = [datakey, modelkey, predictname]
        kws = {}
        ui_list='do_regression_predict'
        fun_list='do_regression_predict'
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, args, kws, self.ui_id)


    def set_predict_parameters(self):
        pass

    def regression_ui(self):
        self.regression_predict = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.regression_predict.setFont(font)
        self.regression_predict.setObjectName(_fromUtf8("regression_predict"))
        self.regression_predict_vlayout = QtGui.QVBoxLayout(self.regression_predict)
        self.regression_predict_vlayout.setObjectName(_fromUtf8("regression_vlayout"))
        # create a layout for choosing data to predict on
        self.regression_predict_choosedata_hlayout = QtGui.QHBoxLayout()
        self.regression_predict_choosedata_hlayout.setObjectName(_fromUtf8("regression_predict_choosedata_hlayout"))
        self.regression_predict_choosedata_label = QtGui.QLabel(self.regression_predict)
        self.regression_predict_choosedata_label.setObjectName(_fromUtf8("regression_predict_choosedata_label"))
        self.regression_predict_choosedata_hlayout.addWidget(self.regression_predict_choosedata_label)
        # create the combobox with data choices
        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No Data has been loaded')
            datachoices = ['No data has been loaded!']
        self.regression_predict_choosedata = make_combobox(datachoices)
        self.regression_predict_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.regression_predict_choosedata.setObjectName(_fromUtf8("regression_predict_choosedata"))
        self.regression_predict_choosedata_hlayout.addWidget(self.regression_predict_choosedata)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.regression_predict_choosedata_hlayout.addItem(spacerItem)
        self.regression_predict_vlayout.addLayout(self.regression_predict_choosedata_hlayout)
        # create a layout for choosing which model to use
        self.regression_predict_choosemodel_hlayout = QtGui.QHBoxLayout()
        self.regression_predict_choosemodel_hlayout.setObjectName(_fromUtf8("regression_predict_choosemodel_hlayout"))
        self.regression_predict_choosemodel_label = QtGui.QLabel(self.regression_predict)
        self.regression_predict_choosemodel_label.setObjectName(_fromUtf8("regression_predict_choosemodel_label"))
        self.regression_predict_choosemodel_hlayout.addWidget(self.regression_predict_choosemodel_label)
        # create the combobox with model choices

        modelchoices = self.pysat_fun.modelkeys
        if modelchoices == []:
            error_print('No model has been trained')
            modelchoices = ['No model has been trained!']
        self.regression_predict_choosemodel = make_combobox(modelchoices)
        self.regression_predict_choosemodel.setIconSize(QtCore.QSize(50, 20))
        self.regression_predict_choosemodel.setObjectName(_fromUtf8("regression_predict_choosedata"))
        self.regression_predict_choosemodel_hlayout.addWidget(self.regression_predict_choosemodel)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.regression_predict_choosemodel_hlayout.addItem(spacerItem1)
        self.regression_predict_vlayout.addLayout(self.regression_predict_choosemodel_hlayout)

        self.module_layout.addWidget(self.regression_predict)
        self.regression_predict.raise_()
        self.regression_predict.setTitle(_translate("regression_predict", "Regression - Predict", None))
        self.regression_predict_choosedata_label.setText(_translate("regression", "Choose data: ", None))
        self.regression_predict_choosemodel_label.setText(_translate("regression", "Choose Model: ", None))
        self.get_predict_parameters()


def make_combobox(choices):
    combo = QtGui.QComboBox()

    for i, choice in enumerate(choices):
        combo.addItem(_fromUtf8(""))
        combo.setItemText(i, _translate('', choice, None))

    return combo


def make_listwidget(choices):
    listwidget = QtGui.QListWidget()
    listwidget.setItemDelegate
    for item in choices:
        item = QtGui.QListWidgetItem(item)
        listwidget.addItem(item)
    return listwidget

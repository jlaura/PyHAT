from ui_modules.Error_ import error_print
from PyQt4 import QtCore, QtGui
import numpy as np
import inspect

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


class plot_:
    def __init__(self, pysat_fun, module_layout, arg_list, kw_list):
        self.pysat_fun = pysat_fun
        self.module_layout = module_layout
        self.ui_id = None
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.plot_ui()
        self.pysat_fun.set_greyed_modules(self.plot)

    def get_plot_parameters(self):
        datakey = self.scatter_choosedata.currentText()
        xvar = self.xvar_choices.currentText()
        yvar = self.yvar_choices.currentText()
        try:
            xvar = (self.vars_level0[self.vars_level1.index(xvar)], xvar)
            yvar = (self.vars_level0[self.vars_level1.index(yvar)], yvar)
        except:
            print('Problem setting x and/or y variable!')
            pass
        figname = self.figname_text.text()
        title = self.plot_title_text.text()
        xrange = self.xmin_spin.value(), self.xmax_spin.value()
        yrange = self.ymin_spin.value(), self.ymax_spin.value()
        xtitle = self.xtitle_text.text()
        ytitle = self.ytitle_text.text()
        lbl = self.legend_label_text.text()
        one_to_one = self.onetoone.isChecked()
        figfile = self.file_text.text()

        color = self.color_choices.currentText()
        alpha = self.alpha_spin.value()

        if color == 'Red':
            color = [1, 0, 0, alpha]
        if color == 'Green':
            color = [0, 1, 0, alpha]
        if color == 'Blue':
            color = [0, 0, 1, alpha]
        if color == 'Cyan':
            color = [0, 1, 1, alpha]
        if color == 'Yellow':
            color = [1, 1, 0, alpha]
        if color == 'Magenta':
            color = [1, 0, 1, alpha]
        if color == 'Black':
            color = [0, 0, 0, alpha]

        marker = self.marker_choices.currentText()
        if marker == 'Circles':
            marker = 'o'
        if marker == 'Squares':
            marker = 's'
        if marker == 'Diamonds':
            marker = 'D'
        if marker == 'Triangle Up':
            marker = '^'
        if marker == 'Triangle Down':
            marker = 'v'
        if marker == 'Triangle Right':
            marker = '>'
        if marker == 'Triangle Left':
            marker = '<'

        line = self.line_choices.currentText()
        if line == 'No Line':
            linestyle = 'None'
        if line == 'Line':
            linestyle = '-'
        if line == 'Dashed Line':
            linestyle = '--'
        if line == 'Dotted Line':
            linestyle = ':'

        args = [datakey, xvar, yvar]
        kws = {'figname': figname,
               'title': title,
               'xrange': xrange,
               'yrange': yrange,
               'xtitle': xtitle,
               'ytitle': ytitle,
               'lbl': lbl,
               'one_to_one': one_to_one,
               'figfile': figfile,
               'color': color,
               'marker': marker,
               'linestyle': linestyle
               }
        ui_list = "do_plot"
        fun_list = "do_plot"
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, args, kws, self.ui_id)

    def set_plot_parameters(self):
        pass

    def plot_ui(self):
        self.plot = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plot.setFont(font)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.verticalLayout = QtGui.QVBoxLayout(self.plot)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scatter_choosedata_flayout = QtGui.QFormLayout()
        self.scatter_choosedata_flayout.setMargin(11)
        self.scatter_choosedata_flayout.setSpacing(6)
        self.scatter_choosedata_flayout.setObjectName(_fromUtf8("scatter_choosedata_flayout"))
        self.scatter_choosedata_label = QtGui.QLabel(self.plot)
        self.scatter_choosedata_label.setObjectName(_fromUtf8("scatter_choosedata_label"))
        self.scatter_choosedata_flayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.scatter_choosedata_label)
        # self.scatter_choosedata = QtGui.QComboBox(self.plot) # we have to remove this as it can't be safely overwritten

        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No Data has been loaded')
            datachoices = ['No data has been loaded!']
        self.scatter_choosedata = make_combobox(datachoices)

        self.scatter_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.scatter_choosedata.setObjectName(_fromUtf8("scatter_choosedata"))
        self.scatter_choosedata_flayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.scatter_choosedata)
        self.figname_label = QtGui.QLabel(self.plot)
        self.figname_label.setObjectName(_fromUtf8("figname_label"))
        self.scatter_choosedata_flayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.figname_label)
        self.figname_text = QtGui.QLineEdit(self.plot)
        self.figname_text.setObjectName(_fromUtf8("figname_text"))
        self.scatter_choosedata_flayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.figname_text)
        self.plot_title_label = QtGui.QLabel(self.plot)
        self.plot_title_label.setObjectName(_fromUtf8("plot_title_label"))
        self.scatter_choosedata_flayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.plot_title_label)
        self.plot_title_text = QtGui.QLineEdit(self.plot)
        self.plot_title_text.setEnabled(True)
        self.plot_title_text.setObjectName(_fromUtf8("plot_title_text"))
        self.scatter_choosedata_flayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.plot_title_text)
        self.verticalLayout.addLayout(self.scatter_choosedata_flayout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.scatter_choosex_flayout = QtGui.QFormLayout()
        self.scatter_choosex_flayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.scatter_choosex_flayout.setMargin(11)
        self.scatter_choosex_flayout.setSpacing(6)
        self.scatter_choosex_flayout.setObjectName(_fromUtf8("scatter_choosex_flayout"))
        self.scatter_choosex_label = QtGui.QLabel(self.plot)
        self.scatter_choosex_label.setObjectName(_fromUtf8("scatter_choosex_label"))
        self.scatter_choosex_flayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.scatter_choosex_label)

        self.xvar_choices = make_combobox([''])
        self.plot_change_vars(self.xvar_choices)
        self.xvar_choices.setObjectName(_fromUtf8("xvar_choices"))
        self.scatter_choosex_flayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.xvar_choices)

        self.xtitle_label = QtGui.QLabel(self.plot)
        self.xtitle_label.setObjectName(_fromUtf8("xtitle_label"))
        self.scatter_choosex_flayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.xtitle_label)
        self.xtitle_text = QtGui.QLineEdit(self.plot)
        self.xtitle_text.setObjectName(_fromUtf8("xtitle_text"))
        self.scatter_choosex_flayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.xtitle_text)
        self.xmin_labe = QtGui.QLabel(self.plot)
        self.xmin_labe.setObjectName(_fromUtf8("xmin_labe"))
        self.scatter_choosex_flayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.xmin_labe)
        self.xmin_spin = QtGui.QDoubleSpinBox(self.plot)
        self.xmin_spin.setObjectName(_fromUtf8("xmin_spin"))
        self.xmin_spin.setRange(-10000000, 10000000)
        self.scatter_choosex_flayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.xmin_spin)
        self.xmax_label = QtGui.QLabel(self.plot)
        self.xmax_label.setObjectName(_fromUtf8("xmax_label"))
        self.scatter_choosex_flayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.xmax_label)
        self.xmax_spin = QtGui.QDoubleSpinBox(self.plot)
        self.xmax_spin.setObjectName(_fromUtf8("xmax_spin"))
        self.xmax_spin.setRange(-10000000, 10000000)
        self.scatter_choosex_flayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.xmax_spin)
        self.verticalLayout.addLayout(self.scatter_choosex_flayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.scatter_choosey_flayout = QtGui.QFormLayout()
        self.scatter_choosey_flayout.setMargin(11)
        self.scatter_choosey_flayout.setSpacing(6)
        self.scatter_choosey_flayout.setObjectName(_fromUtf8("scatter_choosey_flayout"))
        self.yvar_choices = make_combobox([''])
        self.plot_change_vars(self.yvar_choices)
        self.yvar_choices.setObjectName(_fromUtf8("yvar_choices"))
        self.scatter_choosey_flayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.yvar_choices)
        self.ytitle_label = QtGui.QLabel(self.plot)
        self.ytitle_label.setObjectName(_fromUtf8("ytitle_label"))
        self.scatter_choosey_flayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.ytitle_label)
        self.ytitle_text = QtGui.QLineEdit(self.plot)
        self.ytitle_text.setObjectName(_fromUtf8("ytitle_text"))
        self.scatter_choosey_flayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ytitle_text)
        self.ymin_label = QtGui.QLabel(self.plot)
        self.ymin_label.setObjectName(_fromUtf8("ymin_label"))
        self.scatter_choosey_flayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.ymin_label)
        self.ymin_spin = QtGui.QDoubleSpinBox(self.plot)
        self.ymin_spin.setObjectName(_fromUtf8("ymin_spin"))
        self.ymin_spin.setRange(-10000000, 10000000)
        self.scatter_choosey_flayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.ymin_spin)
        self.ymax_label = QtGui.QLabel(self.plot)
        self.ymax_label.setObjectName(_fromUtf8("ymax_label"))
        self.scatter_choosey_flayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.ymax_label)
        self.ymax_spin = QtGui.QDoubleSpinBox(self.plot)
        self.ymax_spin.setObjectName(_fromUtf8("ymax_spin"))
        self.ymax_spin.setRange(-10000000, 10000000)
        self.scatter_choosey_flayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.ymax_spin)
        self.scatter_choosey_label = QtGui.QLabel(self.plot)
        self.scatter_choosey_label.setObjectName(_fromUtf8("scatter_choosey_label"))
        self.scatter_choosey_flayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.scatter_choosey_label)
        self.verticalLayout.addLayout(self.scatter_choosey_flayout)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.legend_hlayout = QtGui.QHBoxLayout()
        self.legend_hlayout.setMargin(11)
        self.legend_hlayout.setSpacing(6)
        self.legend_hlayout.setObjectName(_fromUtf8("legend_hlayout"))
        self.legend_label = QtGui.QLabel(self.plot)
        self.legend_label.setObjectName(_fromUtf8("legend_label"))
        self.legend_label.setText('Legend label: ')
        self.legend_hlayout.addWidget(self.legend_label)
        self.legend_label_text = QtGui.QLineEdit(self.plot)
        self.legend_label_text.setObjectName(_fromUtf8("legend_label_text"))
        self.legend_hlayout.addWidget(self.legend_label_text)
        self.onetoone = QtGui.QCheckBox(self.plot)
        self.onetoone.setObjectName(_fromUtf8("onetoone"))
        self.onetoone.setText('One to One')
        self.legend_hlayout.addWidget(self.onetoone)
        self.verticalLayout.addLayout(self.legend_hlayout)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.scatter_chooseline_flayout = QtGui.QFormLayout()
        self.scatter_chooseline_flayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.scatter_chooseline_flayout.setMargin(11)
        self.scatter_chooseline_flayout.setSpacing(6)
        self.scatter_chooseline_flayout.setObjectName(_fromUtf8("scatter_chooseline_flayout"))
        self.color_label = QtGui.QLabel(self.plot)
        self.color_label.setObjectName(_fromUtf8("color_label"))
        self.scatter_chooseline_flayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.color_label)
        self.color_choices = QtGui.QComboBox(self.plot)
        self.color_choices.setIconSize(QtCore.QSize(50, 20))
        self.color_choices.setObjectName(_fromUtf8("color_choices"))
        self.scatter_chooseline_flayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.color_choices)
        self.line_label = QtGui.QLabel(self.plot)
        self.line_label.setObjectName(_fromUtf8("line_label"))
        self.scatter_chooseline_flayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.line_label)
        self.line_choices = QtGui.QComboBox(self.plot)
        self.line_choices.setIconSize(QtCore.QSize(50, 20))
        self.line_choices.setObjectName(_fromUtf8("line_choices"))
        self.scatter_chooseline_flayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.line_choices)
        self.marker_label = QtGui.QLabel(self.plot)
        self.marker_label.setObjectName(_fromUtf8("marker_label"))
        self.scatter_chooseline_flayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.marker_label)
        self.marker_choices = QtGui.QComboBox(self.plot)
        self.marker_choices.setIconSize(QtCore.QSize(50, 20))
        self.marker_choices.setObjectName(_fromUtf8("marker_choices"))
        self.scatter_chooseline_flayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.marker_choices)
        self.file_label = QtGui.QLabel(self.plot)
        self.file_label.setObjectName(_fromUtf8("file_label"))
        self.scatter_chooseline_flayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.file_label)
        self.file_text = QtGui.QLineEdit(self.plot)
        self.file_text.setObjectName(_fromUtf8("file_text"))
        self.scatter_chooseline_flayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.file_text)
        self.alpha_label = QtGui.QLabel(self.plot)
        self.alpha_label.setObjectName(_fromUtf8("alpha_label"))
        self.scatter_chooseline_flayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.alpha_label)
        self.alpha_spin = QtGui.QDoubleSpinBox(self.plot)
        self.alpha_spin.setObjectName(_fromUtf8("alpha_spin"))
        self.alpha_spin.setRange(0, 1)
        self.alpha_spin.setValue(0.5)
        self.alpha_spin.setSingleStep(0.1)
        self.alpha_spin.setObjectName(_fromUtf8("alpha_spin"))
        self.scatter_chooseline_flayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.alpha_spin)
        self.verticalLayout.addLayout(self.scatter_chooseline_flayout)
        self.module_layout.addWidget(self.plot)

        self.plot.setTitle(_translate("MainWindow", "Scatter Plot", None))
        self.scatter_choosedata_label.setText(_translate("MainWindow", "Choose data: ", None))
        self.figname_label.setText(_translate("MainWindow", "Figure name:", None))
        self.plot_title_label.setText(_translate("MainWindow", "Plot Title: ", None))
        self.scatter_choosex_label.setText(_translate("MainWindow", "Choose X variable:", None))
        self.xtitle_label.setText(_translate("MainWindow", "X title:", None))
        self.xmin_labe.setText(_translate("MainWindow", "X min:", None))
        self.xmax_label.setText(_translate("MainWindow", "X max:", None))
        self.ytitle_label.setText(_translate("MainWindow", "Y title:", None))
        self.ymin_label.setText(_translate("MainWindow", "Y min:", None))
        self.ymax_label.setText(_translate("MainWindow", "Y max:", None))
        self.scatter_choosey_label.setText(_translate("MainWindow", "Choose Y variable:", None))
        self.legend_label.setText(_translate("MainWindow", "Legend Label: ", None))
        self.onetoone.setText(_translate("MainWindow", "One to One", None))
        self.color_label.setText(_translate("MainWindow", "Color:", None))
        self.color_choices.addItem(_fromUtf8("Red"))
        self.color_choices.addItem(_fromUtf8("Green"))
        self.color_choices.addItem(_fromUtf8("Blue"))
        self.color_choices.addItem(_fromUtf8("Cyan"))
        self.color_choices.addItem(_fromUtf8("Yellow"))
        self.color_choices.addItem(_fromUtf8("Magenta"))
        self.color_choices.addItem(_fromUtf8("Black"))
        self.line_label.setText(_translate("MainWindow", "Line:", None))
        self.line_choices.addItem("No Line")
        self.line_choices.addItem("Line")
        self.line_choices.addItem("Dashed Line")
        self.line_choices.addItem("Dotted Line")
        self.marker_label.setText(_translate("MainWindow", "Marker:", None))
        self.marker_choices.addItem("Circles")
        self.marker_choices.addItem("Squares")
        self.marker_choices.addItem("Diamonds")
        self.marker_choices.addItem("Triangle Up")
        self.marker_choices.addItem("Triangle Down")
        self.marker_choices.addItem("Triangle Left")
        self.marker_choices.addItem("Triangle Right")
        self.marker_choices.addItem("None")
        self.file_label.setText(_translate("MainWindow", "Plot Filename:", None))
        self.alpha_label.setText(_translate("MainWindow", "Alpha:", None))

        self.plot.setTitle(_translate("plot", "Plot", None))
        self.scatter_choosedata.activated[int].connect(lambda: self.plot_change_vars(self.xvar_choices))
        self.scatter_choosedata.activated[int].connect(
            lambda: self.get_minmax(self.xmin_spin, self.xmax_spin, self.xvar_choices.currentText()))
        self.scatter_choosedata.activated[int].connect(
            lambda: self.get_minmax(self.ymin_spin, self.ymax_spin, self.yvar_choices.currentText()))
        self.xvar_choices.activated[int].connect(
            lambda: self.get_minmax(self.xmin_spin, self.xmax_spin, self.xvar_choices.currentText()))
        self.scatter_choosedata.activated[int].connect(lambda: self.plot_change_vars(self.yvar_choices))
        self.yvar_choices.activated[int].connect(
            lambda: self.get_minmax(self.ymin_spin, self.ymax_spin, self.yvar_choices.currentText()))
        self.color_choices.activated.connect(lambda: self.get_plot_parameters())

        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QtGui.QComboBox):
                obj.currentIndexChanged.connect(lambda: self.get_plot_parameters())
            if isinstance(obj, QtGui.QLineEdit):
                obj.textChanged.connect(lambda: self.get_plot_parameters())
            if isinstance(obj, QtGui.QDoubleSpinBox):
                obj.valueChanged.connect(lambda: self.get_plot_parameters())
            if isinstance(obj, QtGui.QCheckBox):
                obj.toggled.connect(lambda: self.get_plot_parameters())

    def plot_change_vars(self, obj):
        obj.clear()
        try:
            self.vars_level0 = self.pysat_fun.data[self.scatter_choosedata.currentText()].df.columns.get_level_values(0)
            self.vars_level1 = self.pysat_fun.data[self.scatter_choosedata.currentText()].df.columns.get_level_values(1)
            self.vars_level1 = self.vars_level1[self.vars_level0 != 'wvl']
            self.vars_level0 = self.vars_level0[self.vars_level0 != 'wvl']
            self.vars_level1 = list(self.vars_level1[self.vars_level0 != 'masked'])
            self.vars_level0 = list(self.vars_level0[self.vars_level0 != 'masked'])
            try:
                self.vars_level0 = [i for i in self.vars_level0 if 'Unnamed' not in str(i)]  # remove unnamed columns from choices
            except:
                pass
            try:
                self.vars_level1 = [i for i in self.vars_level1 if 'Unnamed' not in str(i)]  # remove unnamed columns from choices
            except:
                pass
            choices = self.vars_level1

        except:
            try:
                choices = self.pysat_fun.data[self.scatter_choosedata.currentText()].columns.values
            except:
                choices = ['No valid choices']
        for i in choices:
            obj.addItem(str(i))

    def get_minmax(self, objmin, objmax, var):
        try:
            varind = self.vars_level1.index(var)
            vartuple = (self.vars_level0[varind], self.vars_level1[varind])
            vardata = self.pysat_fun.data[self.scatter_choosedata.currentText()].df[vartuple]
        except:
            try:
                vardata = self.pysat_fun.data[self.scatter_choosedata.currentText()][var]
            except:
                vardata = [0, 0]
        try:
            varmin = float(np.min(vardata))
            varmax = float(np.max(vardata))
            objmin.setValue(varmin)
            objmax.setValue(varmax)
        except:
            objmin.setValue(0)
            objmax.setValue(1)

def make_combobox(choices):
    combo = QtGui.QComboBox()

    for i, choice in enumerate(choices):
        combo.addItem(_fromUtf8(""))
        combo.setItemText(i, str(choice))

    return combo


def make_listwidget(choices):
    listwidget = QtGui.QListWidget()
    listwidget.setItemDelegate
    for item in choices:
        item = QtGui.QListWidgetItem(item)
        listwidget.addItem(item)
    return listwidget

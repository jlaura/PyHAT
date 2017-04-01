from PyQt4 import QtCore, QtGui
from pysat.utils.gui_utils import make_combobox
from ui_modules.Error_ import error_print

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


class dim_red_plot_:
    def __init__(self, pysat_fun, module_layout,arg_list,kw_list):
        self.pysat_fun = pysat_fun
        self.arg_list = arg_list
        self.kw_list = kw_list
        self.ui_id = None
        self.module_layout = module_layout
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.dim_red_plot_ui()
        self.set_dim_red_params()
        self.get_dim_red_params()
        self.pysat_fun.set_greyed_modules(self.dim_red_plot)

    def set_dim_red_params(self):
        if self.arg_list is not None:
            datakey = self.arg_list[0]
            xvar = self.arg_list[1]
            yvar = self.arg_list[2]
            filename = self.arg_list[3]
            colorvar = self.kw_list['colorvar'][1]
            method = self.kw_list['method']

            self.dim_red_plot_choose_data.setCurrentIndex(self.dim_red_plot_choose_data.findText(datakey))
            self.dim_red_choosealg.setCurrentIndex(self.dim_red_choosealg.findText(method))
            self.xychoices_change_vars(self.xvar_choices)
            self.xychoices_change_vars(self.yvar_choices)
            self.xvar_choices.setCurrentIndex(self.xvar_choices.findText(xvar))
            self.yvar_choices.setCurrentIndex(self.yvar_choices.findText(yvar))
            self.colorchoices.setCurrentIndex(self.colorchoices.findText(colorvar))
            self.file_text.setText(filename)



    def get_dim_red_params(self):
        datakey=self.dim_red_plot_choose_data.currentText()
        method=self.dim_red_choosealg.currentText()
        xvar=self.xvar_choices.currentText()
        yvar=self.yvar_choices.currentText()
        colorvar=('comp',self.colorchoices.currentText())
        filename=self.file_text.text()


        args=[datakey,xvar,yvar,filename]
        kws={'colorvar':colorvar,'method':method}

        ui_list = "do_plot_dim_red"
        fun_list = "do_plot_dim_red"
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, args, kws, self.ui_id)



    def dim_red_plot_ui(self):
        self.dim_red_plot = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dim_red_plot.setFont(font)
        self.dim_red_plot.setObjectName(_fromUtf8("Dimensionality Reduction Plot"))
        self.dim_red_plot_vlayout = QtGui.QVBoxLayout(self.dim_red_plot)
        self.dim_red_plot_vlayout.setObjectName(_fromUtf8("dim_red_plot_vlayout"))
        #choose data set to apply dim reduction to
        self.dim_red_plot_choose_data_label = QtGui.QLabel(self.dim_red_plot)
        self.dim_red_plot_choose_data_label.setObjectName(_fromUtf8("dim_red_plot_choose_data_label"))
        self.dim_red_plot_choose_data_label.setText(_translate("dim_red_plot", "Choose data:", None))
        self.dim_red_plot_vlayout.addWidget(self.dim_red_plot_choose_data_label)
        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No data has been loaded!')
            datachoices = ['No data has been loaded!']
        self.dim_red_plot_choose_data = make_combobox(datachoices)
        self.dim_red_plot_vlayout.addWidget(self.dim_red_plot_choose_data)

        #Choose the algorithm
        self.dim_red_choosealg_label=QtGui.QLabel(self.dim_red_plot)
        self.dim_red_choosealg_label.setText(_translate("dim_red_plot", "Choose method:", None))
        self.dim_red_plot_vlayout.addWidget(self.dim_red_choosealg_label)
        alg_choices=['Choose a method','PCA','ICA','ICA-JADE']
        self.dim_red_choosealg=make_combobox(alg_choices)
        self.dim_red_plot_vlayout.addWidget(self.dim_red_choosealg)

        #choose the x and y variables
        xyvarchoices=['Choose a method first']
        self.xvar_choices_label=QtGui.QLabel(self.dim_red_plot)
        self.xvar_choices_label.setText('Choose X variable:')
        self.xvar_choices = make_combobox(xyvarchoices)
        self.xvar_choices.setObjectName(_fromUtf8("xvar_choices"))
        self.dim_red_plot_vlayout.addWidget(self.xvar_choices_label)
        self.dim_red_plot_vlayout.addWidget(self.xvar_choices)

        self.yvar_choices_label = QtGui.QLabel(self.dim_red_plot)
        self.yvar_choices_label.setText('Choose Y variable:')
        self.yvar_choices = make_combobox(xyvarchoices)
        self.yvar_choices.setObjectName(_fromUtf8("yvar_choices"))
        self.dim_red_plot_vlayout.addWidget(self.yvar_choices_label)
        self.dim_red_plot_vlayout.addWidget(self.yvar_choices)

        #choose the (optional) variable to use to color code the points
        self.colorchoices_label = QtGui.QLabel(self.dim_red_plot)
        self.colorchoices_label.setText('Choose variable to color code points (optional):')
        self.colorchoices = make_combobox([''])
        self.colorchoices_change_vars(self.colorchoices)
        self.colorchoices.setObjectName(_fromUtf8("colorchoices"))
        self.dim_red_plot_vlayout.addWidget(self.colorchoices_label)
        self.dim_red_plot_vlayout.addWidget(self.colorchoices)

        #choose a filename for the plot
        self.file_label = QtGui.QLabel(self.dim_red_plot)
        self.file_label.setObjectName(_fromUtf8("file_label"))
        self.file_text = QtGui.QLineEdit(self.dim_red_plot)
        self.file_text.setObjectName(_fromUtf8("file_text"))
        self.dim_red_plot_vlayout.addWidget(self.file_label)
        self.dim_red_plot_vlayout.addWidget(self.file_text)


        self.module_layout.addWidget(self.dim_red_plot)
        self.dim_red_plot.raise_()
        self.dim_red_plot.setTitle(_translate("MainWindow", "Dimensionality Reduction", None))


        self.dim_red_plot_choose_data.currentIndexChanged.connect(lambda: self.get_dim_red_params())
        self.dim_red_choosealg.currentIndexChanged.connect(lambda: self.get_dim_red_params())
        self.dim_red_choosealg.currentIndexChanged.connect(lambda: self.xychoices_change_vars(self.xvar_choices))
        self.dim_red_choosealg.currentIndexChanged.connect(lambda: self.xychoices_change_vars(self.yvar_choices))
        self.xvar_choices.currentIndexChanged.connect(lambda: self.get_dim_red_params())
        self.yvar_choices.currentIndexChanged.connect(lambda: self.get_dim_red_params())
        self.colorchoices.currentIndexChanged.connect(lambda: self.get_dim_red_params())
        self.file_text.textChanged.connect(lambda: self.get_dim_red_params())
    def xychoices_change_vars(self,obj):
        obj.clear()
        choices=self.pysat_fun.data[self.dim_red_plot_choose_data.currentText()].df[self.dim_red_choosealg.currentText()].columns.values
        for i in choices:
            obj.addItem(str(i))

    def colorchoices_change_vars(self, obj):
        obj.clear()
        choices = ['None']
        try:
            self.vars_level0 = self.pysat_fun.data[self.dim_red_plot_choose_data.currentText()].df.columns.get_level_values(0)
            self.vars_level1 = self.pysat_fun.data[self.dim_red_plot_choose_data.currentText()].df.columns.get_level_values(1)
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
            for i in self.vars_level1:
                choices.append(str(i))

        except:
            try:
                choices.append(self.pysat_fun.data[self.dim_red_plot_choose_data.currentText()].columns.values)
            except:
                pass
        for i in choices:
            obj.addItem(str(i))
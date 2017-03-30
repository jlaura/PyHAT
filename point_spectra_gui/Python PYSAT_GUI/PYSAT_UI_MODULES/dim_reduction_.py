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


class dim_reduction_:
    def __init__(self, pysat_fun, module_layout,arg_list,kw_list):
        self.pysat_fun = pysat_fun
        self.arg_list = arg_list
        self.kw_list = kw_list
        self.ui_id = None
        self.module_layout = module_layout
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.dim_reduction_ui()
        self.set_dim_red_params()
        self.dim_red_choosealg.currentIndexChanged.connect(  #
            lambda: self.make_dim_red_widget(self.dim_red_choosealg.currentText()))  #
        self.get_dim_red_params()
        self.pysat_fun.set_greyed_modules(self.dim_reduction)

    def set_dim_red_params(self):
        if self.arg_list is not None:
            datakey = self.arg_list[0]
            method = self.arg_list[1]
            self.dim_reduction_choose_data.setCurrentIndex(self.dim_reduction_choose_data.findText(datakey))
            self.dim_red_choosealg.setCurrentIndex(self.dim_red_choosealg.findText(method))
            self.make_dim_red_widget(method)
            if method=='PCA':
                nc=self.kw_list['method_kws']['n_components']
                self.dim_red_widget.pca_nc_spinbox.setValue(nc)
            if method == 'ICA':
                nc = self.kw_list['method_kws']['n_components']
                self.dim_red_widget.ica_nc_spinbox.setValue(nc)
            if method == 'ICA-JADE':
                nc = self.kw_list['method_kws']['n_components']
                self.dim_red_widget.ica_jade_nc_spinbox.setValue(nc)


    def get_dim_red_params(self):
        datakey=self.dim_reduction_choose_data.currentText()
        method=self.dim_red_choosealg.currentText()
        params=[]
        method_kws={}
        try:
            if method=='PCA':
                method_kws={'n_components':self.dim_red_widget.pca_nc_spinbox.value()}

            if method=='ICA':
                method_kws = {'n_components': self.dim_red_widget.ica_nc_spinbox.value()}

            if method=='ICA-JADE':
                method_kws = {'n_components': self.dim_red_widget.ica_jade_nc_spinbox.value()}

        except:
            pass
        args=[datakey,method,params]
        kws = {'method_kws':method_kws}
        ui_list = "do_dim_red"
        fun_list = "do_dim_red"
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, args, kws, self.ui_id)


    def make_dim_red_widget(self,method):
        print(method)
        try:
            self.dim_red_widget.deleteLater()
        except:
            pass
        self.dim_red_widget = QtGui.QWidget()
        if method == 'PCA':
            self.dim_red_widget.pca_hlayout = QtGui.QHBoxLayout(self.dim_red_widget)
            self.dim_red_widget.pca_nc_label = QtGui.QLabel(self.dim_red_widget)
            self.dim_red_widget.pca_nc_label.setText('# of components:')
            self.dim_red_widget.pca_hlayout.addWidget(self.dim_red_widget.pca_nc_label)
            self.dim_red_widget.pca_nc_spinbox = QtGui.QSpinBox(self.dim_red_widget)

            self.dim_red_widget.pca_hlayout.addWidget(self.dim_red_widget.pca_nc_spinbox)
            self.dim_red_widget.pca_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                           QtGui.QSizePolicy.Minimum)
            self.dim_red_widget.pca_hlayout.addItem(self.dim_red_widget.pca_spacer)
            self.dim_red_widget.pca_nc_spinbox.valueChanged.connect(lambda: self.get_dim_red_params())
        if method == 'ICA':
            self.dim_red_widget.ica_hlayout = QtGui.QHBoxLayout(self.dim_red_widget)
            self.dim_red_widget.ica_nc_label = QtGui.QLabel(self.dim_red_widget)
            self.dim_red_widget.ica_nc_label.setText('# of components:')
            self.dim_red_widget.ica_hlayout.addWidget(self.dim_red_widget.ica_nc_label)
            self.dim_red_widget.ica_nc_spinbox = QtGui.QSpinBox(self.dim_red_widget)
            self.dim_red_widget.ica_hlayout.addWidget(self.dim_red_widget.ica_nc_spinbox)
            self.dim_red_widget.ica_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                           QtGui.QSizePolicy.Minimum)
            self.dim_red_widget.ica_hlayout.addItem(self.dim_red_widget.ica_spacer)
            self.dim_red_widget.ica_nc_spinbox.valueChanged.connect(lambda: self.get_dim_red_params())
        if method == 'ICA-JADE':
            self.dim_red_widget.ica_jade_hlayout = QtGui.QHBoxLayout(self.dim_red_widget)
            self.dim_red_widget.ica_jade_nc_label = QtGui.QLabel(self.dim_red_widget)
            self.dim_red_widget.ica_jade_nc_label.setText('# of components:')
            self.dim_red_widget.ica_jade_hlayout.addWidget(self.dim_red_widget.ica_jade_nc_label)
            self.dim_red_widget.ica_jade_nc_spinbox = QtGui.QSpinBox(self.dim_red_widget)
            self.dim_red_widget.ica_jade_hlayout.addWidget(self.dim_red_widget.ica_jade_nc_spinbox)
            self.dim_red_widget.ica_jade_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                           QtGui.QSizePolicy.Minimum)
            self.dim_red_widget.ica_jade_hlayout.addItem(self.dim_red_widget.ica_jade_spacer)
            self.dim_red_widget.ica_jade_nc_spinbox.valueChanged.connect(lambda: self.get_dim_red_params())

        self.dim_reduction_vlayout.addWidget(self.dim_red_widget)
        self.get_dim_red_params()

    def dim_reduction_ui(self):
        self.dim_reduction = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dim_reduction.setFont(font)
        self.dim_reduction.setObjectName(_fromUtf8("Dimensionality Reduction"))
        self.dim_reduction_vlayout = QtGui.QVBoxLayout(self.dim_reduction)
        self.dim_reduction_vlayout.setObjectName(_fromUtf8("dim_reduction_vlayout"))
        #choose data set to apply dim reduction to
        self.dim_reduction_choose_data_label = QtGui.QLabel(self.dim_reduction)
        self.dim_reduction_choose_data_label.setObjectName(_fromUtf8("dim_reduction_choose_data_label"))
        self.dim_reduction_vlayout.addWidget(self.dim_reduction_choose_data_label)
        datachoices = self.pysat_fun.datakeys
        if datachoices == []:
            error_print('No data has been loaded!')
            datachoices = ['No data has been loaded!']
        self.dim_reduction_choose_data = make_combobox(datachoices)
        self.dim_reduction_vlayout.addWidget(self.dim_reduction_choose_data)

        #Choose the algorithm to apply
        self.dim_red_choosealg_label=QtGui.QLabel(self.dim_reduction)
        self.dim_reduction_vlayout.addWidget(self.dim_red_choosealg_label)
        alg_choices=['Choose a method','PCA','ICA','ICA-JADE']
        self.dim_red_choosealg=make_combobox(alg_choices)
        self.dim_reduction_vlayout.addWidget(self.dim_red_choosealg)


        self.module_layout.addWidget(self.dim_reduction)
        self.dim_reduction.raise_()
        self.dim_reduction.setTitle(_translate("MainWindow", "Dimensionality Reduction", None))
        self.dim_reduction_choose_data_label.setText(_translate("dim_reduction", "Choose data:", None))
        self.dim_red_choosealg_label.setText(_translate("dim_reduction", "Choose method:", None))
        self.dim_reduction_choose_data.currentIndexChanged.connect(lambda: self.get_dim_red_params())
        self.dim_red_choosealg.currentIndexChanged.connect(lambda: self.get_dim_red_params())


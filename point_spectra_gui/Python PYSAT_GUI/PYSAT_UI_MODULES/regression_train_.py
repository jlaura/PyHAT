from PYSAT_UI_MODULES import make_combobox, make_listwidget
from PYSAT_UI_MODULES.Error_ import error_print
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


class regression_train_:
    def __init__(self, pysat_fun, module_layout, arg_list, kw_list):
        self.arg_list = arg_list
        self.kw_list = kw_list
        self.pysat_fun = pysat_fun
        self.ui_id = None
        self.module_layout = module_layout
        self.main()

    def main(self):
        self.ui_id = self.pysat_fun.set_list(None, None, None, None, self.ui_id)
        self.regression_ui()  # start the regression UI. create our submodule
        self.pysat_fun.set_greyed_modules(self.regression_train)  # set the module grey after use.
        self.regression_ransac_checkbox.toggled.connect(  #
            lambda: self.make_ransac_widget(self.regression_ransac_checkbox.isChecked()))  #
        self.regression_choosealg.currentIndexChanged.connect(  #
            lambda: self.make_regression_widget(self.regression_choosealg.currentText()))  #

    def get_regression_parameters(self):
        method = self.regression_choosealg.currentText()
        datakey = self.regression_choosedata.currentText()
        xvars = [str(x.text()) for x in self.regression_train_choosex.selectedItems()]
        yvars = [('comp', str(y.text())) for y in self.regression_train_choosey.selectedItems()]
        yrange = [self.yvarmin_spin.value(), self.yvarmax_spin.value()]
        params = {}
        ransacparams = {}
        kws = {}
        try:
            modelkey = method + ' - ' + str(yvars[0][-1]) + ' (' + str(yrange[0]) + '-' + str(yrange[1]) + ') '
        except:
            modelkey = method
        try:
            if method == 'OLS':
                params = {'fit_intercept': self.reg_widget.ols_intercept_checkbox.isChecked()}
                modelkey = modelkey + str(params)
            if method == 'OMP':
                params = {'fit_intercept': self.reg_widget.omp_intercept_checkbox.isChecked(),
                          'n_nonzero_coefs': self.reg_widget.omp_nfeatures.value(),
                          'CV': self.reg_widget.omp_cv_checkbox.isChecked()}
                modelkey = modelkey + str(params)
            if method == 'Lasso':
                params = {'alpha': self.reg_widget.lasso_alpha.value(),
                          'fit_intercept': self.reg_widget.lasso_intercept_checkbox.isChecked(),
                          'max_iter': self.reg_widget.lasso_max.value(), 'tol': self.reg_widget.lasso_tol.value(),
                          'positive': self.reg_widget.lasso_positive_checkbox.isChecked(), 'selection': 'random',
                          'CV': self.reg_widget.lasso_cv_checkbox.isChecked()}
                print(params)
            if method == 'Elastic Net':
                pass
            if method == 'Ridge':
                pass
            if method == 'Bayesian Ridge':
                pass
            if method == 'ARD':
                pass
            if method == 'LARS':
                pass
            if method == 'Lasso LARS':
                pass
            if method == 'SVR':
                pass
            if method == 'KRR':
                pass

            if method == 'PLS':
                params = {'n_components': self.reg_widget.pls_nc_spinbox.value(),
                          'scale': False}
                modelkey = modelkey + '(nc=' + str(params['n_components']) + ')'
                kws = {'modelkey': modelkey}
            if method == 'GP':
                params = {'reduce_dim': self.reg_widget.gp_dim_red_combobox.currentText(),
                          'n_components': self.reg_widget.gp_dim_red_nc_spinbox.value(),
                          'random_start': self.reg_widget.gp_rand_starts_spin.value(),
                          'theta0': self.reg_widget.gp_theta0_spin.value(),
                          'thetaL': self.reg_widget.gp_thetaL_spin.value(),
                          'thetaU': self.reg_widget.gp_thetaU_spin.value()}

                modelkey = modelkey + str(params)

        except:
            pass
        kws = {'modelkey': modelkey}
        if self.regression_ransac_checkbox.isChecked():
            lossval = self.ransac_widget.ransac_lossfunc_combobox.currentText()
            if lossval == 'Squared Error':
                loss = 'squared_loss'
            if lossval == 'Absolute Error':
                loss = 'absolute_loss'
            ransacparams = {'residual_threshold': self.ransac_widget.ransac_thresh_spin.value(),
                            'loss': loss}
        ui_list = "do_regression_train"
        fun_list = "do_regression_train"

        args = [datakey, xvars, yvars, yrange, method, params, ransacparams]
        self.ui_id = self.pysat_fun.set_list(ui_list, fun_list, args, kws, self.ui_id)

    def set_regression_parameters(self):
        datakey = self.arg_list[0]
        xvars = self.arg_list[1]
        yvars = self.arg_list[2]
        yrange = self.arg_list[3]
        method = self.arg_list[4]
        params = self.arg_list[5]
        ransacparams = self.arg_list[6]
        self.regression_choosedata.currentIndex(self.regression_choosedata.findText(str(datakey)))

    def make_ransac_widget(self, isChecked):
        if not isChecked:
            self.ransac_widget.deleteLater()
        else:
            self.ransac_widget = QtGui.QWidget()
            self.ransac_widget.ransac_widget_hlayout = QtGui.QHBoxLayout(self.ransac_widget)
            self.ransac_widget.ransac_lossfunc_hlayout = QtGui.QHBoxLayout()
            self.ransac_widget.ransac_lossfunc_label = QtGui.QLabel(self.ransac_widget)
            self.ransac_widget.ransac_lossfunc_label.setText('Loss function:')
            self.ransac_widget.ransac_lossfunc_hlayout.addWidget(self.ransac_widget.ransac_lossfunc_label)
            self.ransac_widget.ransac_lossfunc_combobox = QtGui.QComboBox(self.ransac_widget)
            self.ransac_widget.ransac_lossfunc_combobox.addItem(_fromUtf8("Squared Error"))
            self.ransac_widget.ransac_lossfunc_combobox.addItem(_fromUtf8("Absolute Error"))
            self.ransac_widget.ransac_lossfunc_hlayout.addWidget(self.ransac_widget.ransac_lossfunc_combobox)
            self.ransac_widget.ransac_lossfunc_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                                          QtGui.QSizePolicy.Minimum)
            self.ransac_widget.ransac_lossfunc_hlayout.addItem(self.ransac_widget.ransac_lossfunc_spacer)
            self.ransac_widget.ransac_widget_hlayout.addLayout(self.ransac_widget.ransac_lossfunc_hlayout)
            self.ransac_widget.ransac_thresh_hlayout = QtGui.QHBoxLayout()
            self.ransac_widget.ransac_thresh_label = QtGui.QLabel(self.ransac_widget)
            self.ransac_widget.ransac_thresh_label.setText('Threshold:')
            self.ransac_widget.ransac_thresh_hlayout.addWidget(self.ransac_widget.ransac_thresh_label)
            self.ransac_widget.ransac_thresh_spin = QtGui.QDoubleSpinBox(self.ransac_widget)
            self.ransac_widget.ransac_thresh_hlayout.addWidget(self.ransac_widget.ransac_thresh_spin)
            self.ransac_widget.ransac_thresh_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                                        QtGui.QSizePolicy.Minimum)
            self.ransac_widget.ransac_thresh_hlayout.addItem(self.ransac_widget.ransac_thresh_spacer)
            self.ransac_widget.ransac_widget_hlayout.addLayout(self.ransac_widget.ransac_thresh_hlayout)
            self.ransac_hlayout.addWidget(self.ransac_widget)

            self.ransac_widget.ransac_lossfunc_combobox.currentIndexChanged.connect(
                lambda: self.get_regression_parameters())
            self.ransac_widget.ransac_thresh_spin.valueChanged.connect(lambda: self.get_regression_parameters())

    def make_regression_widget(self, alg):
        print(alg)
        try:
            self.reg_widget.deleteLater()
        except:
            pass
        self.reg_widget = QtGui.QWidget()
        if alg == 'PLS':
            self.reg_widget.pls_hlayout = QtGui.QHBoxLayout(self.reg_widget)
            self.reg_widget.pls_nc_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.pls_nc_label.setText('# of components:')
            self.reg_widget.pls_hlayout.addWidget(self.reg_widget.pls_nc_label)
            self.reg_widget.pls_nc_spinbox = QtGui.QSpinBox(self.reg_widget)
            self.reg_widget.pls_hlayout.addWidget(self.reg_widget.pls_nc_spinbox)
            self.reg_widget.pls_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                           QtGui.QSizePolicy.Minimum)
            self.reg_widget.pls_hlayout.addItem(self.reg_widget.pls_spacer)
            self.reg_widget.pls_nc_spinbox.valueChanged.connect(lambda: self.get_regression_parameters())

        elif alg == 'GP':
            self.reg_widget = QtGui.QWidget()
            self.reg_widget.gp_vlayout = QtGui.QVBoxLayout(self.reg_widget)
            self.reg_widget.gp_dim_red_hlayout = QtGui.QHBoxLayout()
            self.reg_widget.gp_dim_red_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_dim_red_label.setText('Choose dimensionality reduction method:')
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_label)
            self.reg_widget.gp_dim_red_combobox = QtGui.QComboBox(self.reg_widget)
            self.reg_widget.gp_dim_red_combobox.addItem(_fromUtf8("PCA"))
            self.reg_widget.gp_dim_red_combobox.addItem(_fromUtf8("ICA"))
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_combobox)
            self.reg_widget.gp_dim_red_nc_label = QtGui.QLabel()
            self.reg_widget.gp_dim_red_nc_label.setText('# of components:')
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_nc_label)
            self.reg_widget.gp_dim_red_nc_spinbox = QtGui.QSpinBox(self.reg_widget)
            self.reg_widget.gp_dim_red_hlayout.addWidget(self.reg_widget.gp_dim_red_nc_spinbox)

            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_dim_red_hlayout)
            self.reg_widget.gp_rand_starts_hlayout = QtGui.QHBoxLayout()
            self.reg_widget.gp_rand_starts_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_rand_starts_label.setText('# of random starts:')
            self.reg_widget.gp_rand_starts_hlayout.addWidget(self.reg_widget.gp_rand_starts_label)
            self.reg_widget.gp_rand_starts_spin = QtGui.QSpinBox(self.reg_widget)
            self.reg_widget.gp_rand_starts_spin.setValue(1)
            self.reg_widget.gp_rand_starts_hlayout.addWidget(self.reg_widget.gp_rand_starts_spin)
            self.reg_widget.spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                            QtGui.QSizePolicy.Minimum)
            self.reg_widget.gp_rand_starts_hlayout.addItem(self.reg_widget.spacerItem4)
            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_rand_starts_hlayout)
            self.reg_widget.gp_theta_vlayout = QtGui.QVBoxLayout()
            self.reg_widget.gp_theta0_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_theta0_label.setText('Starting Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_theta0_label)
            self.reg_widget.gp_theta0_spin = QtGui.QDoubleSpinBox(self.reg_widget)
            self.reg_widget.gp_theta0_spin.setValue(1.0)
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_theta0_spin)
            self.reg_widget.gp_thetaL_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_thetaL_label.setText('Lower bound on Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaL_label)
            self.reg_widget.gp_thetaL_spin = QtGui.QDoubleSpinBox(self.reg_widget)
            self.reg_widget.gp_thetaL_spin.setValue(0.1)
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaL_spin)
            self.reg_widget.gp_thetaU_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.gp_thetaU_label.setText('Upper bound on Theta:')
            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaU_label)
            self.reg_widget.gp_thetaU_spin = QtGui.QDoubleSpinBox(self.reg_widget)
            self.reg_widget.gp_thetaU_spin.setMaximum(10000)
            self.reg_widget.gp_thetaU_spin.setValue(100.0)

            self.reg_widget.gp_theta_vlayout.addWidget(self.reg_widget.gp_thetaU_spin)
            self.reg_widget.spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                            QtGui.QSizePolicy.Minimum)
            self.reg_widget.gp_theta_vlayout.addItem(self.reg_widget.spacerItem5)
            self.reg_widget.gp_vlayout.addLayout(self.reg_widget.gp_theta_vlayout)
            self.reg_widget.gp_dim_red_combobox.currentIndexChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_dim_red_nc_spinbox.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_rand_starts_spin.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_theta0_spin.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_thetaL_spin.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.gp_thetaU_spin.valueChanged.connect(lambda: self.get_regression_parameters())
        elif alg == 'OLS':
            self.reg_widget.ols_hlayout = QtGui.QHBoxLayout(self.reg_widget)
            self.reg_widget.ols_intercept_checkbox = QtGui.QCheckBox(self.reg_widget)
            self.reg_widget.ols_intercept_checkbox.setText('Fit Intercept')
            self.reg_widget.ols_intercept_checkbox.setChecked(True)
            self.reg_widget.ols_hlayout.addWidget(self.reg_widget.ols_intercept_checkbox)
            self.reg_widget.ols_intercept_checkbox.stateChanged.connect(lambda: self.get_regression_parameters())

        elif alg == 'OMP':
            self.reg_widget.omp_hlayout = QtGui.QHBoxLayout(self.reg_widget)
            self.reg_widget.omp_label = QtGui.QLabel(self.reg_widget)
            self.reg_widget.omp_label.setText('# of nonzero coefficients:')
            self.reg_widget.omp_hlayout.addWidget(self.reg_widget.omp_label)
            self.reg_widget.omp_nfeatures = QtGui.QSpinBox(self.reg_widget)
            self.reg_widget.omp_nfeatures.setMaximum(9999)
            try:
                xvars = [str(x.text()) for x in self.regression_train_choosex.selectedItems()]
                nfeatures_default = 0.1 * self.pysat_fun.data[self.regression_choosedata.currentText()].df[
                    xvars].columns.levels[1].size
                self.reg_widget.omp_nfeatures.setValue(nfeatures_default)
            except:
                self.reg_widget.omp_nfeatures.setValue(10)
            self.reg_widget.omp_hlayout.addWidget(self.reg_widget.omp_nfeatures)
            self.reg_widget.omp_intercept_checkbox = QtGui.QCheckBox(self.reg_widget)
            self.reg_widget.omp_intercept_checkbox.setText('Fit Intercept')
            self.reg_widget.omp_intercept_checkbox.setChecked(True)
            self.reg_widget.omp_hlayout.addWidget(self.reg_widget.omp_intercept_checkbox)

            self.reg_widget.omp_cv_checkbox = QtGui.QCheckBox(self.reg_widget)
            self.reg_widget.omp_cv_checkbox.setText('Optimize with Cross Validation? (Ignores # of coeffs)')
            self.reg_widget.omp_cv_checkbox.setChecked(True)
            self.reg_widget.omp_hlayout.addWidget(self.reg_widget.omp_cv_checkbox)

            self.reg_widget.omp_intercept_checkbox.stateChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.omp_cv_checkbox.stateChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.omp_nfeatures.valueChanged.connect(lambda: self.get_regression_parameters())

        elif alg == 'Lasso':
            self.reg_widget.lasso_vlayout = QtGui.QVBoxLayout(self.reg_widget)
            self.reg_widget.lasso_alpha_hlayout = QtGui.QHBoxLayout(self.reg_widget)
            self.reg_widget.lasso_iter_hlayout = QtGui.QHBoxLayout(self.reg_widget)
            self.reg_widget.lasso_checkboxes_hlayout = QtGui.QHBoxLayout(self.reg_widget)

            self.reg_widget.lasso_alphalabel = QtGui.QLabel(self.reg_widget)
            self.reg_widget.lasso_alphalabel.setText('Alpha:')
            self.reg_widget.lasso_alpha_hlayout.addWidget(self.reg_widget.lasso_alphalabel)

            self.reg_widget.lasso_alpha = QtGui.QDoubleSpinBox(self.reg_widget)
            self.reg_widget.lasso_alpha.setMaximum(1000)
            self.reg_widget.lasso_alpha.setMinimum(0.0001)
            self.reg_widget.lasso_alpha.setValue(1.0)
            self.reg_widget.lasso_alpha_hlayout.addWidget(self.reg_widget.lasso_alpha)

            self.reg_widget.lasso_alpha_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                                   QtGui.QSizePolicy.Minimum)
            self.reg_widget.lasso_alpha_hlayout.addItem(self.reg_widget.lasso_alpha_spacer)
            self.reg_widget.lasso_vlayout.addItem(self.reg_widget.lasso_alpha_hlayout)

            self.reg_widget.lasso_maxlabel = QtGui.QLabel(self.reg_widget)
            self.reg_widget.lasso_maxlabel.setText('Max # of iterations:')
            self.reg_widget.lasso_iter_hlayout.addWidget(self.reg_widget.lasso_maxlabel)

            self.reg_widget.lasso_max = QtGui.QSpinBox(self.reg_widget)
            self.reg_widget.lasso_max.setMaximum(100000)
            self.reg_widget.lasso_max.setMinimum(1)
            self.reg_widget.lasso_max.setValue(1000)
            self.reg_widget.lasso_iter_hlayout.addWidget(self.reg_widget.lasso_max)

            self.reg_widget.lasso_tollabel = QtGui.QLabel(self.reg_widget)
            self.reg_widget.lasso_tollabel.setText('Tolerance:')
            self.reg_widget.lasso_iter_hlayout.addWidget(self.reg_widget.lasso_tollabel)

            self.reg_widget.lasso_tol = QtGui.QDoubleSpinBox(self.reg_widget)
            self.reg_widget.lasso_tol.setMaximum(1000)
            self.reg_widget.lasso_tol.setMinimum(0.0000001)
            self.reg_widget.lasso_tol.setDecimals(5)
            self.reg_widget.lasso_tol.setValue(0.0001)
            self.reg_widget.lasso_iter_hlayout.addWidget(self.reg_widget.lasso_tol)

            self.reg_widget.lasso_iter_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                                  QtGui.QSizePolicy.Minimum)
            self.reg_widget.lasso_iter_hlayout.addItem(self.reg_widget.lasso_iter_spacer)
            self.reg_widget.lasso_vlayout.addItem(self.reg_widget.lasso_iter_hlayout)

            self.reg_widget.lasso_intercept_checkbox = QtGui.QCheckBox(self.reg_widget)
            self.reg_widget.lasso_intercept_checkbox.setText('Fit Intercept')
            self.reg_widget.lasso_intercept_checkbox.setChecked(True)
            self.reg_widget.lasso_checkboxes_hlayout.addWidget(self.reg_widget.lasso_intercept_checkbox)

            self.reg_widget.lasso_positive_checkbox = QtGui.QCheckBox(self.reg_widget)
            self.reg_widget.lasso_positive_checkbox.setText('Force positive coefficients')
            self.reg_widget.lasso_positive_checkbox.setChecked(False)
            self.reg_widget.lasso_checkboxes_hlayout.addWidget(self.reg_widget.lasso_positive_checkbox)

            self.reg_widget.lasso_cv_checkbox = QtGui.QCheckBox(self.reg_widget)
            self.reg_widget.lasso_cv_checkbox.setText('Optimize with Cross Validation? (Ignores alpha)')
            self.reg_widget.lasso_cv_checkbox.setChecked(True)
            self.reg_widget.lasso_checkboxes_hlayout.addWidget(self.reg_widget.lasso_cv_checkbox)

            self.reg_widget.lasso_checkbox_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                                      QtGui.QSizePolicy.Minimum)
            self.reg_widget.lasso_checkboxes_hlayout.addItem(self.reg_widget.lasso_checkbox_spacer)
            self.reg_widget.lasso_vlayout.addItem(self.reg_widget.lasso_checkboxes_hlayout)

            self.reg_widget.lasso_alpha.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.lasso_max.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.lasso_tol.valueChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.lasso_intercept_checkbox.stateChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.lasso_positive_checkbox.stateChanged.connect(lambda: self.get_regression_parameters())
            self.reg_widget.lasso_cv_checkbox.stateChanged.connect(lambda: self.get_regression_parameters())

        if alg == 'Elastic Net':
            pass
        if alg == 'Ridge':
            pass
        if alg == 'Bayesian Ridge':
            pass
        if alg == 'ARD':
            pass
        if alg == 'LARS':
            pass
        if alg == 'Lasso LARS':
            pass
        if alg == 'SVR':
            pass
        if alg == 'KRR':
            pass

        self.regression_vlayout.addWidget(self.reg_widget)
        self.get_regression_parameters()

    def regression_ui(self):
        self.regression_train = QtGui.QGroupBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.regression_train.setFont(font)
        self.regression_train.setObjectName(_fromUtf8("regression_train"))
        self.regression_vlayout = QtGui.QVBoxLayout(self.regression_train)
        self.regression_vlayout.setObjectName(_fromUtf8("regression_vlayout"))
        # choose data
        self.regression_choosedata_hlayout = QtGui.QHBoxLayout()
        self.regression_choosedata_hlayout.setObjectName(_fromUtf8("regression_choosedata_hlayout"))
        self.regression_train_choosedata_label = QtGui.QLabel(self.regression_train)
        self.regression_train_choosedata_label.setObjectName(_fromUtf8("regression_train_choosedata_label"))
        self.regression_train_choosedata_label.setText(_translate("regression_train", "Choose data:", None))
        self.regression_choosedata_hlayout.addWidget(self.regression_train_choosedata_label)
        datachoices = self.pysat_fun.datakeys
        datachoices = [i for i in datachoices if i != 'CV Results']  # prevent CV results from showing up as an option
        if datachoices == []:
            error_print('No Data has been loaded')
            datachoices = ['No data has been loaded!']
        self.regression_choosedata = make_combobox(datachoices)
        self.regression_choosedata.setIconSize(QtCore.QSize(50, 20))
        self.regression_choosedata.setObjectName(_fromUtf8("regression_choosedata"))
        self.regression_choosedata_hlayout.addWidget(self.regression_choosedata)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.regression_choosedata_hlayout.addItem(spacerItem)
        self.regression_vlayout.addLayout(self.regression_choosedata_hlayout)
        # choose variables
        self.regression_choosevars_hlayout = QtGui.QHBoxLayout()
        self.regression_choosevars_hlayout.setObjectName(_fromUtf8("regression_choosevars_hlayout"))
        self.regression_choosexvars_vlayout = QtGui.QVBoxLayout()
        self.regression_chooseyvars_vlayout = QtGui.QVBoxLayout()
        self.regression_choosevars_hlayout.addLayout(self.regression_choosexvars_vlayout)
        self.regression_choosevars_hlayout.addLayout(self.regression_chooseyvars_vlayout)
        # choose x variables
        self.regression_train_choosex_label = QtGui.QLabel(self.regression_train)
        self.regression_train_choosex_label.setObjectName(_fromUtf8("regression_train_choosex_label"))
        self.regression_train_choosex_label.setText('X variable:')
        self.regression_choosexvars_vlayout.addWidget(self.regression_train_choosex_label)
        try:
            xvarchoices = self.pysat_fun.data[self.regression_choosedata.currentText()].df.columns.levels[0].values
            xvarchoices = [i for i in xvarchoices if not 'Unnamed' in i]  # remove unnamed columns from choices
        except:
            xvarchoices = ['None']
        self.regression_train_choosex = make_listwidget(xvarchoices)
        self.regression_train_choosex.setObjectName(_fromUtf8("regression_train_choosex"))
        self.regression_choosexvars_vlayout.addWidget(self.regression_train_choosex)

        # choose y variables
        self.regression_train_choosey_label = QtGui.QLabel(self.regression_train)
        self.regression_train_choosey_label.setObjectName(_fromUtf8("regression_train_choosey_label"))
        self.regression_train_choosey_label.setText('Y variable:')
        self.regression_chooseyvars_vlayout.addWidget(self.regression_train_choosey_label)
        try:
            yvarchoices = self.pysat_fun.data[self.regression_choosedata.currentText()].df['comp'].columns.values
            yvarchoices = [i for i in yvarchoices if not 'Unnamed' in i]  # remove unnamed columns from choices
        except:
            yvarchoices = ['None']
        self.regression_train_choosey = make_listwidget(yvarchoices)
        self.regression_chooseyvars_vlayout.addWidget(self.regression_train_choosey)
        self.regression_yvarlimits_hlayout = QtGui.QHBoxLayout()
        self.yvarmin_label = QtGui.QLabel(self.regression_train)
        self.yvarmin_label.setText('Min:')
        self.regression_yvarlimits_hlayout.addWidget(self.yvarmin_label)
        self.yvarmin_spin = QtGui.QDoubleSpinBox()
        # TODO: eventually we may want the ability to handle values outside 0-100 for regressions not dealing with wt.%
        self.yvarmin_spin.setMaximum(99999)
        self.yvarmin_spin.setMinimum(0)
        self.regression_yvarlimits_hlayout.addWidget(self.yvarmin_label)
        self.regression_yvarlimits_hlayout.addWidget(self.yvarmin_spin)

        self.yvarmax_label = QtGui.QLabel(self.regression_train)
        self.yvarmax_label.setText('Max:')
        self.regression_yvarlimits_hlayout.addWidget(self.yvarmax_label)
        self.yvarmax_spin = QtGui.QDoubleSpinBox()
        self.yvarmax_spin.setMaximum(99999)
        self.yvarmax_spin.setMinimum(0)
        self.yvarmax_spin.setValue(100)
        self.regression_yvarlimits_hlayout.addWidget(self.yvarmax_label)
        self.regression_yvarlimits_hlayout.addWidget(self.yvarmax_spin)
        self.regression_chooseyvars_vlayout.addLayout(self.regression_yvarlimits_hlayout)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.regression_choosevars_hlayout.addItem(spacerItem1)
        self.regression_vlayout.addLayout(self.regression_choosevars_hlayout)

        # ransac options
        self.ransac_hlayout = QtGui.QHBoxLayout()
        self.regression_ransac_checkbox = QtGui.QCheckBox(self.regression_train)
        self.regression_ransac_checkbox.setObjectName(_fromUtf8("regression_ransac_checkbox"))
        self.regression_ransac_checkbox.setText('RANSAC')
        self.ransac_hlayout.addWidget(self.regression_ransac_checkbox)
        self.regression_vlayout.addLayout(self.ransac_hlayout)

        # choose regression algorithm
        self.regression_choosealg_hlayout = QtGui.QHBoxLayout()
        self.regression_choosealg_hlayout.setObjectName(_fromUtf8("regression_choosealg_hlayout"))
        self.regression_choosealg_label = QtGui.QLabel(self.regression_train)
        self.regression_choosealg_label.setObjectName(_fromUtf8("regression_choosealg_label"))
        self.regression_choosealg_hlayout.addWidget(self.regression_choosealg_label)
        self.regression_alg_choices = ['Choose an algorithm', 'PLS', 'GP', 'OLS', 'OMP', 'Lasso', 'More to come...']
        self.regression_choosealg = make_combobox(self.regression_alg_choices)
        self.regression_choosealg.setIconSize(QtCore.QSize(50, 20))
        self.regression_choosealg.setObjectName(_fromUtf8("regression_choosealg"))
        self.regression_choosealg_hlayout.addWidget(self.regression_choosealg)
        regression_choosealg_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                        QtGui.QSizePolicy.Minimum)
        self.regression_choosealg_hlayout.addItem(regression_choosealg_spacer)
        self.regression_vlayout.addLayout(self.regression_choosealg_hlayout)

        self.module_layout.addWidget(self.regression_train)
        self.regression_train.raise_()
        self.regression_train.setTitle(_translate("regression_train", "Regression - Train", None))

        self.regression_choosedata.currentIndexChanged.connect(lambda: self.get_regression_parameters())
        self.regression_choosealg.currentIndexChanged.connect(lambda: self.get_regression_parameters())
        self.regression_train_choosex.currentItemChanged.connect(lambda: self.get_regression_parameters())
        self.regression_train_choosey.currentItemChanged.connect(lambda: self.get_regression_parameters())
        self.yvarmin_spin.valueChanged.connect(lambda: self.get_regression_parameters())
        self.yvarmax_spin.valueChanged.connect(lambda: self.get_regression_parameters())
        self.regression_choosedata.activated[int].connect(
            lambda: self.regression_change_vars(self.regression_train_choosey))

    def regression_change_vars(self, obj):
        obj.clear()
        try:
            choices = self.pysat_fun.data[self.regression_choosedata.currentText()].df[['comp']].columns.values
            for i in choices:
                obj.addItem(i[1])
        except:
            obj.addItem('None')
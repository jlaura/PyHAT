from PyQt4 import QtCore, QtGui
from pysat_func import pysat_func
import PYSAT_UI_MODULES
import pickle

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


class pysat_ui(object):
    def __init__(self):
        self.pysat_fun = pysat_func()
        self.ui_list = []
        self.restore_list = None
        self.flag = False
        self.restore_flag = False

    """ =============================================
    This is the backbone of the UI, without this portion we have nothing to work with
    ============================================== """

    def main_window(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 1000)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.scrollarea_layout = QtGui.QVBoxLayout(self.centralWidget)
        self.scrollarea_layout.setMargin(11)
        self.scrollarea_layout.setSpacing(6)
        self.scrollarea_layout.setObjectName(_fromUtf8("scrollarea_layout"))
        self.scrollArea = QtGui.QScrollArea(self.centralWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        #self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 557, 800))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.scrollAreaWidgetContents_2.setFont(font)
        self.scrollAreaWidgetContents_2.setStyleSheet(_fromUtf8("QGroupBox {\n"
                                                                "  border: 2px solid gray;\n"
                                                                "  border-radius: 6px;\n"
                                                                "  margin-top: 0.5em;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QGroupBox::title {\n"
                                                                "\n"
                                                                "  padding-top: -14px;\n"
                                                                "  padding-left: 8px;\n"
                                                                "}\n"
                                                                ""))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.module_layout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.module_layout.setMargin(11)
        self.module_layout.setSpacing(6)
        self.module_layout.setObjectName(_fromUtf8("module_layout"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollarea_layout.addWidget(self.scrollArea)
        self.OK = QtGui.QGroupBox(self.centralWidget)
        self.OK.setObjectName(_fromUtf8("OK"))
        self.ok = QtGui.QHBoxLayout(self.OK)
        self.ok.setMargin(11)
        self.ok.setSpacing(6)
        self.ok.setObjectName(_fromUtf8("ok"))
        self.progressBar = QtGui.QProgressBar(self.OK)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.ok.addWidget(self.progressBar)
        self.delButton = QtGui.QPushButton(self.OK)
        self.okButton = QtGui.QPushButton(self.OK)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.delButton.setFont(font)
        self.delButton.setMouseTracking(False)
        self.delButton.setObjectName("delButton")
        self.ok.addWidget(self.delButton)
        self.okButton.setFont(font)
        self.okButton.setMouseTracking(False)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.ok.addWidget(self.okButton)
        self.scrollarea_layout.addWidget(self.OK)



        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 581, 26))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPreprocessing = QtGui.QMenu(self.menuBar)
        self.menuPreprocessing.setObjectName(_fromUtf8("menuPreprocessing"))
        self.menuRegression = QtGui.QMenu(self.menuBar)
        self.menuRegression.setObjectName(_fromUtf8("menuRegression"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuVisualization = QtGui.QMenu(self.menuBar)
        self.menuVisualization.setObjectName(_fromUtf8("menuVisualization"))
        MainWindow.setMenuBar(self.menuBar)

        #set up data actions
        self.actionRead_ccam = QtGui.QAction(MainWindow)
        self.actionRead_ccam.setObjectName(_fromUtf8("actionRead_ccam"))
        self.actionLoad_reference_Data = QtGui.QAction(MainWindow)
        self.actionLoad_reference_Data.setObjectName(_fromUtf8("actionLoad_reference_Data"))
        self.actionLoad_Unknown_Data = QtGui.QAction(MainWindow)
        self.actionLoad_Unknown_Data.setObjectName(_fromUtf8("actionLoad_Unknown_Data"))
        self.actionSave_Current_Workflow = QtGui.QAction(MainWindow)
        self.actionSave_Current_Workflow.setObjectName(_fromUtf8("actionSave_Current_Workflow"))
        self.actionSave_Current_Data = QtGui.QAction(MainWindow)
        self.actionSave_Current_Data.setObjectName(_fromUtf8("actionSave_Current_Data"))
        self.actionCreate_New_Workflow = QtGui.QAction(MainWindow)
        self.actionCreate_New_Workflow.setObjectName(_fromUtf8("actionCreate_New_Workflow"))
        self.actionOpen_Workflow = QtGui.QAction(MainWindow)
        self.actionOpen_Workflow.setObjectName(_fromUtf8("actionOpen_Workflow"))
        self.actionSet_output_location = QtGui.QAction(MainWindow)
        self.actionSet_output_location.setObjectName(_fromUtf8("actionSet_output_location"))

        #set up preprocessing actions
        self.actionRemoveNull = QtGui.QAction(MainWindow)
        self.actionRemoveNull.setObjectName(_fromUtf8("actionRemoveNull"))
        self.actionApply_Mask = QtGui.QAction(MainWindow)
        self.actionApply_Mask.setObjectName(_fromUtf8("actionApply_Mask"))
        self.actionInterpolate = QtGui.QAction(MainWindow)
        self.actionInterpolate.setObjectName(_fromUtf8("actionInterpolate"))
        self.actionStratified_Folds = QtGui.QAction(MainWindow)
        self.actionStratified_Folds.setObjectName(_fromUtf8("actionStratified_Folds"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout_QtCreator = QtGui.QAction(MainWindow)
        self.actionAbout_QtCreator.setObjectName(_fromUtf8("actionAbout_QtCreator"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionNormalization = QtGui.QAction(MainWindow)
        self.actionNormalization.setObjectName(_fromUtf8("actionNormalization"))
        self.actionDimRed=QtGui.QAction(MainWindow)
        self.actionDimRed.setObjectName(_fromUtf8("actionDimRed"))

#set up regression actions
        self.actionCross_Validation = QtGui.QAction(MainWindow)
        self.actionCross_Validation.setObjectName(_fromUtf8("actionCross_Validation"))
        self.actionTrain = QtGui.QAction(MainWindow)
        self.actionTrain.setObjectName(_fromUtf8("actionTrain"))
        self.actionPredict = QtGui.QAction(MainWindow)
        self.actionPredict.setObjectName(_fromUtf8("actionPredict"))

#set up plotting actions
        self.actionPlot = QtGui.QAction(MainWindow)
        self.actionPlot.setObjectName(_fromUtf8("actionPlot"))
        self.actionPlotDimRed = QtGui.QAction(MainWindow)
        self.actionPlotDimRed.setObjectName(_fromUtf8("actionPlot"))

        self.actionTrain_Submodels = QtGui.QAction(MainWindow)
        self.actionTrain_Submodels.setObjectName(_fromUtf8("actionTrain_Submodels"))
        self.actionSubmodelPredict = QtGui.QAction(MainWindow)
        self.actionSubmodelPredict.setObjectName(_fromUtf8("actionSubmodelPredict"))

        #add actions to file menu
        self.menuFile.addAction(self.actionRead_ccam)
        self.menuFile.addAction(self.actionLoad_reference_Data)
        self.menuFile.addAction(self.actionLoad_Unknown_Data)
        self.menuFile.addAction(self.actionSet_output_location)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Current_Data)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionCreate_New_Workflow)
        self.menuFile.addAction(self.actionOpen_Workflow)
        self.menuFile.addAction(self.actionSave_Current_Workflow)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        #add actions to preprocessing
        self.menuPreprocessing.addAction(self.actionRemoveNull)
        self.menuPreprocessing.addAction(self.actionInterpolate)
        self.menuPreprocessing.addAction(self.actionApply_Mask)
        self.menuPreprocessing.addAction(self.actionNormalization)
        self.menuPreprocessing.addAction(self.actionDimRed)
        self.menuPreprocessing.addAction(self.actionStratified_Folds)

        #add actions to regression menu
        self.menuRegression.addAction(self.actionCross_Validation)
        self.menuRegression.addAction(self.actionTrain)
        self.menuRegression.addAction(self.actionSubmodelPredict)
        self.menuRegression.addAction(self.actionPredict)

        #add actions to help menu
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_QtCreator)

        #add actions to plot menu
        self.menuVisualization.addAction(self.actionPlot)
        self.menuVisualization.addAction(self.actionPlotDimRed)

        #add menu actions
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuPreprocessing.menuAction())
        self.menuBar.addAction(self.menuRegression.menuAction())
        self.menuBar.addAction(self.menuVisualization.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setWindowTitle(_translate("MainWindow", "PYSAT", None))
        self.okButton.setText(_translate("MainWindow", "OK", None))
        self.delButton.setText(_translate("MainWindow", "Delete Module", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuPreprocessing.setTitle(_translate("MainWindow", "Preprocessing", None))
        self.menuRegression.setTitle(_translate("MainWindow", "Regression", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuVisualization.setTitle(_translate("MainWindow", "Visualization", None))
        self.actionRead_ccam.setText(_translate("MainWindow","Read ChemCam Data",None))
        self.actionLoad_reference_Data.setText(_translate("MainWindow", "Load Reference Data", None))
        self.actionLoad_Unknown_Data.setText(_translate("MainWindow", "Load Unknown Data", None))
        self.actionSave_Current_Workflow.setText(_translate("MainWindow", "Save Current Workflow", None))
        self.actionSave_Current_Data.setText(_translate("MainWindow", "Save Current Data", None))
        self.actionCreate_New_Workflow.setText(_translate("MainWindow", "Create New Workflow", None))
        self.actionOpen_Workflow.setText(_translate("MainWindow", "Restore Workflow", None))
        self.actionApply_Mask.setText(_translate("MainWindow", "Apply Mask", None))
        self.actionInterpolate.setText(_translate("MainWindow", "Interpolate", None))
        self.actionRemoveNull.setText(_translate("MainWindow", "Remove Null Data", None))
        self.actionDimRed.setText((_translate("MainWindow","Dimensionality Reduction",None)))
        self.actionAbout.setText(_translate("MainWindow", "About...", None))
        self.actionAbout_QtCreator.setText(_translate("MainWindow", "About Qt...", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionNormalization.setText(_translate("MainWindow", "Normalization", None))
        self.actionCross_Validation.setText(_translate("MainWindow", "Cross Validation", None))
        self.actionTrain.setText(_translate("MainWindow", "Train", None))
        self.actionSubmodelPredict.setText(_translate("MainWindow", "Submodel Predict", None))
        self.actionPredict.setText(_translate("MainWindow", "Predict", None))
        self.actionPlot.setText(_translate("MainWindow", "Plot", None))
        self.actionPlotDimRed.setText(_translate("MainWindow", "Plot ICA/PCA", None))

        self.actionSet_output_location.setText(_translate("MainWindow", "Set Output Path", None))

        self.actionStratified_Folds.setText(_translate("MainWindow", "Stratified Folds", None))
        self.okButton.clicked.connect(lambda: self.on_okButton_clicked())
        self.delButton.clicked.connect(lambda: self.pysat_fun.del_layout())

    def get_known_data(self, arg_list=None, kw_list=None):
        self.flag = PYSAT_UI_MODULES.get_data_k_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def get_unknown_data(self, arg_list=None, kw_list=None):
        self.flag = PYSAT_UI_MODULES.get_data_u_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_read_ccam(self,arg_list=None,kw_list=None):
        self.flag = PYSAT_UI_MODULES.read_ccam_(self.pysat_fun,self.module_layout,arg_list,kw_list)

    def do_mask(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.get_mask_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_write_data(self):
        self.flag = PYSAT_UI_MODULES.write_data_(self.pysat_fun,self.module_layout)

    def file_outpath(self, arg_list=None, kw_list=None):
        self.flag = PYSAT_UI_MODULES.file_outpath_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_removenull(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.removenull_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def normalization(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.normalization_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_strat_folds(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.strat_folds_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_dim_red(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.dim_reduction_(self.pysat_fun, self.module_layout,arg_list,kw_list)

    def do_regression_train(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.regression_train_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_regression_predict(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.regression_predict_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_submodel_predict(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.sm_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_plot(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.plot_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_plot_dim_red(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.dim_red_plot_(self.pysat_fun, self.module_layout,arg_list,kw_list)

    def do_cv(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.cv_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    def do_interp(self, arg_list=None, kw_list=None):
        PYSAT_UI_MODULES.interpolation_(self.pysat_fun, self.module_layout, arg_list, kw_list)

    """ =============================================
    Please do not delete the functions below this line!
    These functions are the working functions
    that allow the UI to operate and do work!
    ============================================== """

    def menu_item_shortcuts(self):
        self.actionExit.setShortcut("ctrl+Q")
        self.actionCreate_New_Workflow.setShortcut("ctrl+N")
        self.actionOpen_Workflow.setShortcut("ctrl+O")
        self.actionSave_Current_Workflow.setShortcut("ctrl+S")

    def menu_item_functions(self, MainWindow):
        self.actionRead_ccam.triggered.connect(lambda: pysat_ui.do_read_ccam(self))
        self.actionSet_output_location.triggered.connect(lambda: pysat_ui.file_outpath(self))  # output location
        self.actionLoad_Unknown_Data.triggered.connect(lambda: pysat_ui.get_unknown_data(self))  # unknown data
        self.actionLoad_reference_Data.triggered.connect(lambda: pysat_ui.get_known_data(self))  # known data
        self.actionSave_Current_Data.triggered.connect(lambda: pysat_ui.do_write_data(self))
        self.actionNormalization.triggered.connect(lambda: pysat_ui.normalization(self))  # submodel
        self.actionApply_Mask.triggered.connect(lambda: pysat_ui.do_mask(self))  # get_mask
        self.actionRemoveNull.triggered.connect(lambda: pysat_ui.do_removenull(self))
        self.actionStratified_Folds.triggered.connect(lambda: pysat_ui.do_strat_folds(self))  # strat folds
        self.actionTrain.triggered.connect(lambda: pysat_ui.do_regression_train(self))  # regression train
        self.actionPredict.triggered.connect(lambda: pysat_ui.do_regression_predict(self))  # regression predict
        self.actionInterpolate.triggered.connect(lambda: pysat_ui.do_interp(self))
        self.actionPlot.triggered.connect(lambda: pysat_ui.do_plot(self))
        self.actionPlotDimRed.triggered.connect(lambda: pysat_ui.do_plot_dim_red(self))
        self.actionCross_Validation.triggered.connect(lambda: pysat_ui.do_cv(self))
        self.actionSubmodelPredict.triggered.connect(lambda:pysat_ui.do_submodel_predict(self))
        self.actionDimRed.triggered.connect(lambda: pysat_ui.do_dim_red(self))
        self.actionOpen_Workflow.triggered.connect(lambda: self.on_load_clicked())
        self.actionSave_Current_Workflow.triggered.connect(lambda: self.on_save_clicked())
        self.set_greyed_out_items(True)
#        self.set_visible_items()

        # TODO add auto scroll down feature
        # self.scrollArea.findChildren().triggered.connect(self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value()+10))

        # These are the Restore functions
        #self.actionPredict.triggered.connect(lambda: self.set_ui_list("do_regression_predict"))  # regression predict
        # self.actionPlot.triggered.connect(lambda: self.set_ui_list("do_plot"))
        # self.actionCross_Validation.triggered.connect(lambda: self.set_ui_list("do_cv"))

    def set_greyed_out_items(self, bool):
        self.actionTrain.setDisabled(bool)
        self.actionPredict.setDisabled(bool)
        self.actionNormalization.setDisabled(bool)
        self.actionApply_Mask.setDisabled(bool)
        self.actionStratified_Folds.setDisabled(bool)
        self.actionTrain.setDisabled(bool)
        self.actionPredict.setDisabled(bool)
        self.actionInterpolate.setDisabled(bool)
        self.actionPlot.setDisabled(bool)
        self.actionRemoveNull.setDisabled(bool)
        self.actionCross_Validation.setDisabled(bool)
        self.actionSubmodelPredict.setDisabled(bool)
        self.actionSave_Current_Data.setDisabled(bool)

#    def set_visible_items(self):
#    def set_visible_items(self):
        # self.actionNoise_Reduction.setVisible(False)
        # self.actionInstrument_Response.setVisible(False)
        # self.menuBaseline_Removal.deleteLater()
        # self.menuCalibration_Transfer.deleteLater()
        # self.actionICA.setVisible(False)
        # self.actionPCA.setVisible(False)
        # self.actionICA_2.setVisible(False)
        # self.actionPCA_2.setVisible(False)
        # self.menuClassification.setTitle("")

    def handleMenuHovered(self, action):
        QtGui.QToolTip.showText(self, None, action, None)

    def on_okButton_clicked(self):
        if self.flag:
            self.set_greyed_out_items(False)
            self.onStart()
            self.pysat_fun.taskFinished.connect(self.onFinished)

    ################# Restoration toolset below

    def on_save_clicked(self):
        try:
            filename = QtGui.QFileDialog.getSaveFileName(None, "Choose where you want save your file", '.', '(*.wrf)')
            print(filename)
            with open(filename, 'wb') as fp:
                pickle.dump(self.pysat_fun.get_list(), fp)
        except:
            print("File not loaded")

    def on_load_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open Workflow File", '.', "(*.wrf)")
        print(filename)
        try:
            with open(filename, 'rb') as fp:
                self.restore_list = pickle.load(fp)
        except:
            PYSAT_UI_MODULES.error_print("File was not loaded")
        self.restore_first()

    def restore_first(self):
        # first run a single or double instance of getattr depending on what data is in the queue
        #   We'll need to remember 'i' so we don't accidentally run the instance too many times
        # then press ok
        # then we'll have another loop continue on it's merry way adding everything in.

        #TODO: Don't run the function until the UI has been loaded
        #TODO: allow set outpath to be run before loading data
        try:
            self.r_list = self.restore_list.pop()
            while self.r_list[1] == "get_unknown_data" or self.r_list[1] == "get_known_data" or self.r_list[1] == 'do_read_ccam':
                getattr(pysat_ui, self.r_list[1])(self, self.r_list[3], self.r_list[4])
                print(self.r_list)
                self.r_list = self.restore_list.pop()
            self.on_okButton_clicked()
            self.pysat_fun.taskFinished.connect(self.restore_rest)
        except Exception as e:
            print(e)

    def restore_rest(self):
        if self.restore_flag is False:
            getattr(pysat_ui, self.r_list[1])(self, self.r_list[3], self.r_list[4])
            for i in range(len(self.restore_list)):
                self.r_list = self.restore_list.pop()
                print(self.r_list)
                getattr(pysat_ui, self.r_list[1])(self, self.r_list[3], self.r_list[4])
            self.restore_flag = True

    ################# Progress bar toolset below

    def onStart(self):  # onStart function
        self.progressBar.setRange(0, 0)  # make the bar pulse green
        self.pysat_fun.start()  # TaskThread.start()
        # This is multithreading thus run() == start()

    def onFinished(self):  # onFinished function
        self.progressBar.setRange(0, 1)  # stop the bar pulsing green
        self.progressBar.setValue(1)  # displays 100% after process is finished.

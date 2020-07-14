from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction

STYLESHEET2 = open("assets/styleSheet2.stylesheet").read()

class ui_Settings(object):
    
    def setupUi(self, Settings):
        
        ## SETTINGS FOR SETTINGS, hehe
        Settings.setObjectName("Settings")
        Settings.resize(824, 565)
        Settings.setStyleSheet(STYLESHEET2)
        
        ## FONT
        font = QtGui.QFont()
        font.setFamily("MingLiU_HKSCS-ExtB")
        font.setPointSize(12)
        Settings.setFont(font)
        
        #_quit = QAction("Quit", Settings)
        #_quit.triggered.connect(self._exit)
        
        ## BUTTON BOX
        
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(10, 510, 781, 51))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        
        #TAB WIDGET
        self.tabWidget = QtWidgets.QTabWidget(Settings)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 861, 491))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        
        ## TABS, LABELS AND LINES
        ##-----------------------
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QtCore.QRect(0, -10, 831, 121))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(210, 10, 391, 91))
        
        font = QtGui.QFont()
        font.setFamily("NSimSun")
        font.setPointSize(24)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(0, 20, 101, 81))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap("assets/settings(1).png"))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 420, 211, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setGeometry(QtCore.QRect(0, 110, 821, 301))
        
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(9)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(160, 0, 461, 31))
        self.label_2.setObjectName("label_2")
        
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(0, 0, 101, 31))
        self.checkBox.setObjectName("checkBox")
        
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_2.setGeometry(QtCore.QRect(0, 40, 121, 51))
        self.checkBox_2.setTristate(False)
        self.checkBox_2.setObjectName("checkBox_2")
        
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setGeometry(QtCore.QRect(160, 60, 391, 20))
        self.label_15.setObjectName("label_15")
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame)
        self.textEdit_2.setGeometry(QtCore.QRect(0, 250, 121, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(130, 250, 450, 31))
        self.label_16.setObjectName("label_16")
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_3.setGeometry(QtCore.QRect(0, 90, 141, 31))
        self.checkBox_3.setObjectName("checkBox_3")
        
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setGeometry(QtCore.QRect(160, 80, 391, 51))
        self.label_17.setObjectName("label_17")
        self.checkBox_4 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_4.setGeometry(QtCore.QRect(0, 140, 161, 21))
        self.checkBox_4.setObjectName("checkBox_4")
        
        self.label_18 = QtWidgets.QLabel(self.frame)
        self.label_18.setGeometry(QtCore.QRect(160, 140, 461, 20))
        self.label_18.setObjectName("label_18")
        
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(-40, 30, 851, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setGeometry(QtCore.QRect(-30, 80, 821, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setGeometry(QtCore.QRect(0, 120, 851, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        
        self.line_4 = QtWidgets.QFrame(self.frame)
        self.line_4.setGeometry(QtCore.QRect(-50, 161, 881, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(0, -10, 831, 121))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(210, 10, 391, 91))
        
        font = QtGui.QFont()
        font.setFamily("NSimSun")
        font.setPointSize(24)
        
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(0, 20, 101, 81))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("assets/settings.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        
        self.groupBox = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox.setGeometry(QtCore.QRect(0, -10, 831, 111))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(210, 10, 391, 91))
        
        font = QtGui.QFont()
        font.setFamily("NSimSun")
        font.setPointSize(24)
        
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(0, 20, 101, 81))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("assets/volume.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        
        self.label_35 = QtWidgets.QLabel(self.tab_3)
        self.label_35.setGeometry(QtCore.QRect(170, 190, 381, 41))
        self.label_35.setObjectName("label_35")
        
        self.checkBox_9 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_9.setGeometry(QtCore.QRect(0, 190, 141, 31))
        self.checkBox_9.setObjectName("checkBox_9")
        
        self.label_36 = QtWidgets.QLabel(self.tab_3)
        self.label_36.setGeometry(QtCore.QRect(170, 160, 471, 16))
        self.label_36.setObjectName("label_36")
        
        self.checkBox_10 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_10.setGeometry(QtCore.QRect(0, 110, 131, 21))
        self.checkBox_10.setObjectName("checkBox_10")
        
        self.label_37 = QtWidgets.QLabel(self.tab_3)
        self.label_37.setGeometry(QtCore.QRect(170, 110, 461, 21))
        self.label_37.setObjectName("label_37")
        
        self.checkBox_11 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_11.setGeometry(QtCore.QRect(0, 140, 141, 51))
        self.checkBox_11.setTristate(False)
        self.checkBox_11.setObjectName("checkBox_11")
        
        self.line_9 = QtWidgets.QFrame(self.tab_3)
        self.line_9.setGeometry(QtCore.QRect(-40, 130, 851, 20))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        
        self.line_10 = QtWidgets.QFrame(self.tab_3)
        self.line_10.setGeometry(QtCore.QRect(-30, 180, 851, 16))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.tabWidget.addTab(self.tab_3, "")
        
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_4.setGeometry(QtCore.QRect(-10, -10, 831, 121))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(210, 10, 391, 91))
        
        font = QtGui.QFont()
        font.setFamily("NSimSun")
        font.setPointSize(24)
        
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(10, 20, 101, 81))
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap("assets/play-button(1).png"))
        self.label_12.setScaledContents(True)
        self.label_12.setObjectName("label_12")
        
        self.tabWidget.addTab(self.tab_4, "")
        
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        
        self.groupBox_16 = QtWidgets.QGroupBox(self.tab_11)
        self.groupBox_16.setGeometry(QtCore.QRect(-10, -10, 831, 121))
        self.groupBox_16.setTitle("")
        self.groupBox_16.setObjectName("groupBox_16")
        
        self.label_57 = QtWidgets.QLabel(self.groupBox_16)
        self.label_57.setGeometry(QtCore.QRect(210, 20, 391, 91))
        
        font = QtGui.QFont()
        font.setFamily("NSimSun")
        font.setPointSize(24)
        
        self.label_57.setFont(font)
        self.label_57.setObjectName("label_57")
        
        self.label_58 = QtWidgets.QLabel(self.groupBox_16)
        self.label_58.setGeometry(QtCore.QRect(30, 20, 101, 71))
        self.label_58.setText("")
        self.label_58.setPixmap(QtGui.QPixmap("assets/keyboard.png"))
        self.label_58.setScaledContents(True)
        self.label_58.setObjectName("label_58")
        
        self.tabWidget.addTab(self.tab_11, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_5.setGeometry(QtCore.QRect(0, -10, 831, 121))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        
        self.label_13 = QtWidgets.QLabel(self.groupBox_5)
        self.label_13.setGeometry(QtCore.QRect(210, 10, 391, 91))
        
        font = QtGui.QFont()
        font.setFamily("NSimSun")
        font.setPointSize(24)
        
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        
        self.label_14 = QtWidgets.QLabel(self.groupBox_5)
        self.label_14.setGeometry(QtCore.QRect(0, 20, 101, 81))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap("assets/comment.png"))
        self.label_14.setScaledContents(True)
        self.label_14.setObjectName("label_14")
        
        self.label = QtWidgets.QLabel(self.tab_5)
        self.label.setGeometry(QtCore.QRect(40, 210, 771, 101))
        
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.tab_5)
        self.pushButton.setGeometry(QtCore.QRect(590, 320, 201, 91))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.tab_5)
        self.textEdit.setGeometry(QtCore.QRect(150, 320, 421, 91))
        self.textEdit.setObjectName("textEdit")
        self.tabWidget.addTab(self.tab_5, "")

        self.retranslateUi(Settings)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.label_9.setText(_translate("Settings", "General settings"))
        self.pushButton_2.setText(_translate("Settings", "Log out"))
        self.label_2.setText(_translate("Settings", "Enable a clock displaying how long you have been connected to a meeting."))
        self.checkBox.setText(_translate("Settings", "Display clock"))
        self.checkBox_2.setText(_translate("Settings", "Hide your name"))
        self.label_15.setText(_translate("Settings", "Automatically hide your username when joining a meeting"))
        self.label_16.setText(_translate("Settings", "Set your username here. By default it will be \'guest\' if this field is empty"))
        self.checkBox_3.setText(_translate("Settings", "Display username"))
        self.label_17.setText(_translate("Settings", "Display your username in the window title when logged in"))
        self.checkBox_4.setText(_translate("Settings", "Block sensitive content"))
        self.label_18.setText(_translate("Settings", "Automatically block content that most people may find sensitive from chats"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Settings", "General"))
        self.label_7.setText(_translate("Settings", "Preferences"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Settings", "Preferences"))
        self.label_3.setText(_translate("Settings", "Audio settings"))
        self.label_35.setText(_translate("Settings", "Display your username in the window title when logged in"))
        self.checkBox_9.setText(_translate("Settings", "Display username"))
        self.label_36.setText(_translate("Settings", "Disable your microphone. By doing this you wont be able to speak in meetings"))
        self.checkBox_10.setText(_translate("Settings", "Automatic mute"))
        self.label_37.setText(_translate("Settings", "Automatically mute yourself when joining a meeting"))
        self.checkBox_11.setText(_translate("Settings", "Disable microphone"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Settings", "Audio"))
        self.label_11.setText(_translate("Settings", "Video settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Settings", "Video"))
        self.label_57.setText(_translate("Settings", "Keyboard shortcuts"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_11), _translate("Settings", "Shortcuts"))
        self.label_13.setText(_translate("Settings", "Feedback"))
        self.label.setText(_translate("Settings", "Care about making Chatvio better? Please send some feedback so we can improve!"))
        self.pushButton.setText(_translate("Settings", "Send"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Settings", "Feedback"))
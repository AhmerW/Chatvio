"""
Main Application for the Chatvio Video conference software.
"""

import sys 
import os 
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction

from client import client

STYLESHEET = open("assets/styleSheet.stylesheet").read()
STYLESHEET2 = open("assets/styleSheet2.stylesheet").read()

class chatvio(object):
    """
    'main' chatvio class.
    This class will be a gateway and connection point
    between all other classes
    """
    def __init__(self):
        self.client = client()
        self.client.start()
        
        ## temp 
        self.sent_first = False
        
        ## user variables
        self.username = ""
        self.logged_in = False 
        self.in_meeting = False


## BELOW HERE IS GUI

class ui_Chatvio(object):
    def __init__(self):
        self.chatvio = chatvio()
        
        
    def on_press(self, name):
        if name == "actionSettings":

            window = QtWidgets.QDialog()
            window.ui = ui_Settings()
            window.ui.setupUi(window)
            window.exec_()
            window.show()
            return
            
            
        ## one time-case where the server receives from this class
        if not self.chatvio.sent_first:
            self.chatvio.sent_first = True
            info = \
                """
                username:{0.username}/
                logged_in:{0.logged_in}
                """.format(self.chatvio)
            self.chatvio.client.connection.send(bytes(
                info, 
                "utf-8"
            ))
            
        ## 'create a meeting' button was pressed
        if name == "pushButton_3":
            args = () #code, etc, will make prompt for that..
            self.chatvio.client.send_command(
                'create_meeting', 
                args
            )
        
    def setupUi(self, Chatvio):
        ## Main window
        Chatvio.setObjectName("Chatvio")
        width, height = 800, 600
        Chatvio.resize(width, height)
        
        ## Font(s)
        
        Chatvio.setFixedSize(width, height)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Chatvio.setFont(font)
        

        
        ## STYLESHEET
        Chatvio.setStyleSheet(STYLESHEET) #credits to https://github.com/sommerc
        
        ## CENTRAL WIDGET
        
        self.centralwidget = QtWidgets.QWidget(Chatvio)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 10, 331, 91))
        
        ## Pallette 
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(224, 119, 20))
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.label.setPalette(palette)
        
        ## FONT
        font = QtGui.QFont()
        font.setFamily("Sitka Subheading")
        font.setPointSize(48)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        
        ## LABEL
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        ## GROUP BOX
        
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(240, 120, 341, 361))
        self.groupBox.setPalette(palette)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        
        ## BUTTONS
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 40, 241, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 280, 241, 51))
        self.pushButton_2.setStyleSheet("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 130, 241, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        Chatvio.setCentralWidget(self.centralwidget)
        
        ## MENUBAR
        self.menubar = QtWidgets.QMenuBar(Chatvio)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuabout = QtWidgets.QMenu(self.menubar)
        self.menuabout.setObjectName("menuabout")
        self.menudonate = QtWidgets.QMenu(self.menubar)
        self.menudonate.setObjectName("menudonate")
        Chatvio.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Chatvio)
        self.statusbar.setObjectName("statusbar")
        Chatvio.setStatusBar(self.statusbar)

        ## MENUBAR ACTIONS
        
        self.actionSettings = QtWidgets.QAction(Chatvio)
        self.actionSettings.setObjectName("actionSettings")
        self.menuSettings.addAction(self.actionSettings)
        
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuabout.menuAction())
        self.menubar.addAction(self.menudonate.menuAction())


        

        self.retranslateUi(Chatvio)
        QtCore.QMetaObject.connectSlotsByName(Chatvio)
    
        ## ADD CLICK EVENT

        ALL_EVENTS = [
            self.actionSettings,
            self.pushButton_2,
            self.pushButton_3,
            self.pushButton_4
        ]
        
        values = list(self.__dict__.values())
        keys = list(self.__dict__.keys())    

        for x in range(len(ALL_EVENTS)):
            event = ALL_EVENTS[x]
            name = keys[values.index(event)] 
            if hasattr(event, 'clicked'):
                event.clicked.connect(lambda ch, i=name: self.on_press(i))
            else:
                event.triggered.connect(lambda ch, i=name: self.on_press(i))

    def retranslateUi(self, Chatvio):
        ## set text n stuff
        _translate = QtCore.QCoreApplication.translate
        if self.chatvio.logged_in:
            text = f"Chatvio - Logged in as {self.chatvio.username}"
        else:
            text = "Chatvio - Not logged in"
        
        Chatvio.setWindowTitle(_translate("Chatvio", text))
        
        Chatvio.setWhatsThis(_translate("Chatvio", "Create a public or private meeting"))
        self.label.setText(_translate("Chatvio", "Chatvio"))
        
        ## BUTTONS
        self.pushButton_3.setWhatsThis(_translate("Chatvio", "Create a public or private meeting"))
        self.pushButton_3.setText(_translate("Chatvio", "Create a meeting"))
        self.pushButton_2.setText(_translate("Chatvio", "Sign up"))
        self.pushButton_4.setText(_translate("Chatvio", "Join a meeting"))

        ## ACTIONS
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.setStatusTip(_translate("Chatvio", "Edit settings"))
        self.actionSettings.setShortcut(_translate("Chatvio", "Ctrl+S"))
        
        ## menus
        self.menuSettings.setTitle(_translate("Chatvio", "Settings"))
        self.menuabout.setTitle(_translate("Chatvio", "about"))
        self.menudonate.setTitle(_translate("Chatvio", "donate"))
        
        
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

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Chatvio = QtWidgets.QMainWindow()
    ui = ui_Chatvio()
    ui.setupUi(Chatvio)
    Chatvio.show()
    sys.exit(app.exec_())

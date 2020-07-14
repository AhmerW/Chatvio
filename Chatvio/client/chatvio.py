"""
Main Application for the Chatvio Video conference software.
"""

import sys 
import os 
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction

from client import client
from ui_Settings import ui_Settings

STYLESHEET = open("assets/styleSheet.stylesheet").read()

class chatvio(object):
    """
    'main' chatvio class.
    This class will be a gateway and connection point
    between all other classes
    """
    def __init__(self):
        self.client = client()
        self.setting = ui_Settings()
        self.client.start()
        
        ## temp 
        self.sent_first = False
        
        ## user variables
        self.username = "guest"
        self.logged_in = False 
        self.in_meeting = False
        
    def update_values(self):
        username = self.setting.textEdit_2.toPlainText()
        print("username: ", username.strip())


## THE GUI

class ui_Chatvio(object):
    def __init__(self):
        self.chatvio = chatvio()
        
        
    def on_press(self, name):
        if name == "actionSettings":

            window = QtWidgets.QDialog()
            window.ui = self.chatvio.setting
            window.ui.setupUi(window)
            window.exec_()
            window.show()
            self.chatvio.update_values()
            return
            
            
        ## one time-case where the server receives from this class
        if not self.chatvio.sent_first:
            self.chatvio.sent_first = True
            info = \
                "username:{0.username}/logged_in:{0.logged_in}".format(self.chatvio)
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
        
        


        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Chatvio = QtWidgets.QMainWindow()
    ui = ui_Chatvio()
    ui.setupUi(Chatvio)
    Chatvio.show()
    sys.exit(app.exec_())

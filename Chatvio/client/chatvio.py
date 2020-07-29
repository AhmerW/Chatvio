"""
Main Application for the Chatvio Video conference software.
"""

import sys 
import os 
import re
from time import sleep
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QAction
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import (
    Tk,
    Toplevel,
    Entry,
    Button,
    Label,
    DISABLED,
    NORMAL,
    END
) 
from client import Client
from dialogs.Settings import ui_Settings
from dialogs.CreateMeeting import Ui_CreateMeetingDialog

# default stylesheet for pyqt5
STYLESHEET = open("assets/styleSheet.stylesheet").read()
STYLESHEET2 = open("assets/styleSheet2.stylesheet").read()

# client instance 
client = Client()

class Chatvio(object):
    """
    The Main Chatvio class.
    This class will be a gateway and connection point
    between all other classes
    """
    def __init__(self):
        """Constructor method"""
        ## instances
        self.setting = ui_Settings() #settings window
        self.createMeeting = Ui_CreateMeetingDialog() #create a meeting dialog
                
        self.sent_first = False
        
        ## user variables
        self.username = "guest"
        self.logged_in = False 
        self.in_meeting = False
        self.hosted_meeting = False
    
        
    def updateValues(self):
        """
        Update the values from the settings window
        """
        username = self.setting.textEdit_2.toPlainText().strip()
        if re.match(r'\w+', username):
            self.username = username

## Graphical user interfaces

class JoinMeeting(Chatvio):
    def __init__(self):
        super().__init__()
        
        self.master = Tk()
        
        ## configure the main window
        self.master.title("Enter your meeting ID")
        self.master.configure(bg='#2d2d2d')
        self.master.resizable(0, 0)
        self.width, self.height = 500, 300
        self.master.geometry("{0.width}x{0.height}".format(self))
        
        self.state = False
        self.success = False
        self.code = 0
        
    def processInfo(self, code):
        status = client.sendCommand(
            "validateid",
            (code)
        )
        if status == "false" or status == None:
            self.window_label.configure(text="Invalid meeting ID")
            self.entry.configure(state=NORMAL)
            self.entry.delete(0, END)
            self.state = False
        else:
            self.success = True
            self.window.destroy()
            self.master.destroy()
        
        
    def validate(self, event = None):
        if self.state:
            return
        self.state = True
        code = str(self.entry.get()).strip()
        self.code = code
        
        ## Entry
        self.entry.delete(0, END)
        self.entry.insert(0, "Validating...")
        self.entry.configure(fg='#3d3c3c')
        self.entry.configure(state=DISABLED)
        
        ## Top level
        self.window = Toplevel()
        self.window.title("Loading...")
        self.window.configure(bg='#2d2d2d')
        self.window.geometry('280x100')
        self.window.resizable(0, 0)
        
        #label 
        self.window_label = Label(self.window, text="Validating meeting ID")
        self.window_label.place(x=100, y=30)
        
        self.window.after(1, lambda : self.processInfo(code))
        self.window.mainloop()
        

        
    def createWidgets(self):
        ## entry
        self.entry = Entry(bg="white", fg="black")
        self.entry.place(x=90, y=50, height=40, width=310)
        self.entry.bind("<Return>", self.validate)
        
        ## button
        self.button = Button(
            bg="#2d2d2d", text="Submit meeting ID", fg="orange", command=self.validate
        )
        self.button.place(x=90, y=150, height=30, width=310)

    def start(self):
        self.createWidgets()
        self.master.mainloop()

class UiChatvio(object):
    """
    User Interface for the Chatvio.
    This is the main gui application.
    """
    def __init__(self):
        self.chatvio = Chatvio()
        
    def _connect(self):
        """
        Starts connecting to the server via TCP
        """
        client.start()
        ## update text
        self.label2.setText("Connected to server")
        self.label2.adjustSize()
        
    def on_press(self, name):
        """
        On-key press. This method gets called when one of the
        three main buttons gets pressed.
        (
            create meeting button,
            join meeting button,
            login buton
        )
        """
        ## update the server with the current valeues
        if not self.chatvio.sent_first:
            self.chatvio.sent_first = True
            info = "username:{0.username}/logged_in:{0.logged_in}".format(self.chatvio)
            client.connection.send(bytes(
                info, 
                "utf-8"
            ))
        
        ## the settings button (in the action menu bar) was pressed
        if name == "actionSettings":
            window = QtWidgets.QDialog()
            window.ui = self.chatvio.setting
            window.ui.setupUi(window)
            window.exec_()
            window.show()
            self.chatvio.updateValues()
            return
        
            
            
        ## 'create a meeting' button is pressed
        if name == "pushButton_3":
            if self.chatvio.hosted_meeting:
                return
                
            ## initialize
            window = QtWidgets.QDialog()
            window.ui = self.chatvio.createMeeting
            window.ui.setupUi(window)
            window.exec_()
            window.show()
            
            ## get checkbox data
            required_pass = self.chatvio.createMeeting.checkBox.isChecked()
            auto_mute = self.chatvio.createMeeting.checkBox_2.isChecked()
         
            
            
    
            _id = client.sendCommand(
                'create_meeting', 
                (required_pass, auto_mute)
            )
            print(f"Created meeting with ID: {_id} ")
            self.chatvio.hosted_meeting = True
            
            self.MeetingWindow = QtWidgets.QMainWindow()
            QtWidgets.QMainWindow()
            ui = UiMeetingWindow()
            ui.setupUi(self.MeetingWindow)
            self.MeetingWindow.show()
            return
        
        ## 'join a meeting' button is pressed
        if name == "pushButton_4":
            joinMeeting = JoinMeeting() #join a meeting dialog
            joinMeeting.start()
            if joinMeeting.success:
                status = client.sendCommand('join_meeting', joinMeeting.code)
                if status == "true":
                    print(f"Joined meeting : {joinMeeting.code}")
                    return
                
            print("Failed to start meeting")


    def setupUi(self, Chatvio):
        ## Main window
        Chatvio.setObjectName("Chatvio")
        width, height = 800, 600
        Chatvio.resize(width, height)
        
        QTimer.singleShot(1, self._connect)
        
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
      
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(0, 515, 50, 50))
        
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
        self.label2.setText(_translate("Chatvio", "Connecting to server.."))
        
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
        
        

class UiMeetingWindow(object):
    def setupUi(self, MeetingWindow):
        MeetingWindow.setObjectName("MeetingWindow")
        MeetingWindow.resize(1226, 844)
        MeetingWindow.setStyleSheet(STYLESHEET2)
        self.centralwidget = QtWidgets.QWidget(MeetingWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/microphone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setShortcut("")
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 4, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/team.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon1)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("assets/logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("assets/chat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 2, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setToolTip("")
        self.tabWidget.setObjectName("tabWidget")
        self.Home = QtWidgets.QWidget()
        self.Home.setObjectName("Home")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Home)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.Home)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("assets/none.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.tabWidget.addTab(self.Home, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.settings)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.groupBox_3 = QtWidgets.QGroupBox(self.settings)
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_7.setGeometry(QtCore.QRect(430, 10, 161, 31))
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_8.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.settings)
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(430, 10, 161, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setGeometry(QtCore.QRect(10, 130, 571, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(10, 90, 161, 20))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_8.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.tabWidget.addTab(self.settings, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_5)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout_4.addWidget(self.pushButton_14, 4, 0, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout_4.addWidget(self.pushButton_12, 7, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox_5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 2, 0, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout_4.addWidget(self.pushButton_11, 5, 0, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout_4.addWidget(self.pushButton_13, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_5)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_6.addWidget(self.pushButton_9, 2, 0, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.notes = QtWidgets.QLabel(self.groupBox_6)
        self.notes.setText("")
        self.notes.setObjectName("notes")
        self.gridLayout_7.addWidget(self.notes, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.groupBox_6)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_7.addWidget(self.line_2, 2, 0, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_6)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setTabChangesFocus(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_7.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_6, 3, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.tab)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_6.addWidget(self.pushButton_8, 0, 0, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.tab)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_6.addWidget(self.pushButton_10, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 5)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("assets/share.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon4)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 3, 1, 1)
        MeetingWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MeetingWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1226, 26))
        self.menubar.setObjectName("menubar")
        MeetingWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MeetingWindow)
        self.statusbar.setObjectName("statusbar")
        MeetingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MeetingWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MeetingWindow)

    def retranslateUi(self, MeetingWindow):
        _translate = QtCore.QCoreApplication.translate
        MeetingWindow.setWindowTitle(_translate("MeetingWindow", "MainWindow"))
        MeetingWindow.setWhatsThis(_translate("MeetingWindow", "Mute your microphone"))
        self.pushButton_2.setText(_translate("MeetingWindow", "Mute microphone"))
        self.pushButton_5.setText(_translate("MeetingWindow", "View participants"))
        self.pushButton_6.setText(_translate("MeetingWindow", "Leave meeting"))
        self.pushButton_4.setText(_translate("MeetingWindow", "Open chat"))
        self.tabWidget.setWhatsThis(_translate("MeetingWindow", "Take notes of your meeting"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Home), _translate("MeetingWindow", "Home"))
        self.groupBox_3.setTitle(_translate("MeetingWindow", "User settings"))
        self.pushButton_7.setText(_translate("MeetingWindow", "Rest settings"))
        self.groupBox_2.setTitle(_translate("MeetingWindow", "Admin settings"))
        self.pushButton.setText(_translate("MeetingWindow", "Rest settings"))
        self.lineEdit.setPlaceholderText(_translate("MeetingWindow", "Require  password to join? Leave empty if not"))
        self.checkBox.setText(_translate("MeetingWindow", "Others are able to join?"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MeetingWindow", "Settings"))
        self.label_4.setText(_translate("MeetingWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; color: white;\">Meeting tools</span></p></body></html>"))
        self.pushButton_14.setText(_translate("MeetingWindow", "Generate random password"))
        self.pushButton_12.setText(_translate("MeetingWindow", "Roll a dice"))
        self.pushButton_11.setText(_translate("MeetingWindow", "Random number"))
        self.pushButton_13.setText(_translate("MeetingWindow", "Random participant"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MeetingWindow", "Tools"))
        self.pushButton_9.setText(_translate("MeetingWindow", "Clear notes"))
        self.plainTextEdit.setDocumentTitle(_translate("MeetingWindow", "Your notes"))
        self.plainTextEdit.setPlaceholderText(_translate("MeetingWindow", "Type your notes here"))
        self.pushButton_8.setText(_translate("MeetingWindow", "Save notes as .txt file"))
        self.pushButton_10.setText(_translate("MeetingWindow", "Load notes from .txt file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MeetingWindow", "Notes"))
        self.pushButton_3.setText(_translate("MeetingWindow", "Share screen"))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    chatvio = QtWidgets.QMainWindow()
    ui = UiChatvio()
    ui.setupUi(chatvio)
    chatvio.show()
    sys.exit(app.exec_())

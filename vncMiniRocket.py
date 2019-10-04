#!/usr/bin/python3
import sys
import time
from PyQt5 import QtCore, QtWidgets, QtGui, Qt, uic
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from PyQt5.QtGui import QTextCursor
#import RPi.GPIO as GPIO

#When Connected to RP Router OpenWrt 192.168.1.1:
#karl's computer 192.168.1.115
piAddress = "192.168.1.186"

print('Imported Packages and Starting Launch VI')

qtCreatorFile = "miniRocketv2.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.showMaximized()
        self.connection_status = False
        #self.HOST = "localhost"
        self.HOST = piAddress
        self.TOPIC_1 = "control/client"
        self.TOPIC_2 = "control/server"
        self.initUI()
        self.sec = 4

    def initUI(self):
        print('initUI')

        self.connection_status = False  # initialzing to a false connection state
        self.arm_status = False
        self.connectBut.clicked.connect(self.connect_app)
        self.launchBut.clicked.connect(self.launchDef)
        self.startCountBut.clicked.connect(self.startCountDef)
        self.resetBut.clicked.connect(self.resetDef)

        # time display
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        #self.timer.start()

    def launch():
        #GPIO.output(launchPin, True)
        time.sleep(1)
        closeMainValve()
        print('launch function called')

    def closeMainValve():
        GPIO.output(launchPin, False)

    def startCountDef(self):
        self.timeLabel.setText('00:05')
        self.timer.start()

    def resetDef(self):
        self.timeLabel.setText('00:05')

    def displayTime(self):
        self.timeLabel.setText('00:0'+str(self.sec))
        if self.sec == 0:
            self.timer.stop()
            self.sec = 4
            print(self.sec)
        else:
            print(self.sec)
            self.sec = self.sec - 1

    def launchDef(self):
        #GPIO.output(launchPin, True)
        time.sleep(1)
        #GPIO.output(launchPin, False)
        self.timeLabel.setText('00:05')
        print('Launch Function Called')

    def send_info(self, command):
        if command == 'launch':
            message = b'launch'
            print('Message Sent')
        else:
            print('Incorrect Command Sent')
        self.client.publish(self.TOPIC_1,message)

    def on_connect(self,client,userdata,flags,rc):
        print('Ran On Connect')
        self.client.subscribe(self.TOPIC_1)
        self.client.subscribe(self.TOPIC_2)
        self.error = rc
        return self.error

    def on_disconnect(client, userdata,rc=0):
        print('Ran On Disconnect')
        print('Disconnected')
        client.loop_stop()

    def on_message_response(self,client,userdata,msg):
        self.button_data = str(msg.payload)
        print(self.button_data)

    def connect_app(self):
        print('Ran Connect App')
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.message_callback_add(self.TOPIC_2,self.on_message_response)
        self.client.on_disconnect = self.on_disconnect
        try:
            self.client.connect(self.HOST,1883,60)
            self.statusLabel.setText('Connected!')
            self.connection_status = True
            self.client.loop_start()
        except:
            self.statusLabel.setText('Failed To Connect')
            print('Failed to Connect')

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

import sys
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO

print('Imported Packages and Starting Launch Server')

HOST = "localhost"
TOPIC_1 = "control/client"
TOPIC_2 = "control/server"

print (("Please connect client software to: %s at port: %d \n") % (HOST, 1883))
print ("Waiting to establish connection........ \n")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print ("Connection established.")
    #print ('Connection address: ',addr)
    #logger.debug("Connection established at {}".format(time.asctime())) #find what the ip is
    print ("Awaiting commands... \n")
    error = rc
    client.subscribe(TOPIC_1)
    return error

def on_disconnect(client, userdata,rc=0):
	print("Connection Lost.")
	client.loop_stop()

def on_message(client, userdata, msg):
    calldata(str(msg.payload))
    print(str(msg.payload))
    #print('On Message')

client = mqtt.Client("server",True)
client.on_connect = on_connect
client.on_message = on_message
#client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.connect(HOST, 1883, 60)

#Setup GPIO on PI
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
launchPin = 18
GPIO.setup(launchPin,GPIO.OUT)
GPIO.output(launchPin, GPIO.input(launchPin))

def calldata(data):
    if 'launch' in data:
        print('Sending Launch Codes!')
        launch()
    else:
        print('Call Data Did Not Work')

def launch():
    GPIO.output(launchPin, True)
    client.publish(TOPIC_2, "Launch Code Sent")
    time.sleep(1)
    closeMainValve()
    #print('launch function called')

def closeMainValve():
    GPIO.output(launchPin, False)
    print('Closed Main Valve')
    client.publish(TOPIC_2, "Closed Main Valve")

client.loop_forever()

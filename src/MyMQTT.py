import time
import paho.mqtt.client as mqtt # 1.5.1

class MyMQTT:
    def __init__(self, clientName, host, user, password, qos = 0):
        # define variables
        self.host = host
        self.user = user
        self.password = password
        self.qos = qos
        self.clientName = clientName
        self.client = None
        self.printPrefix = f"MQTT::{self.clientName}:"
        # setup client
        self.client = mqtt.Client( self.clientName )
        self.client.username_pw_set( self.user, self.password )
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_publish = self.on_publish

    ## callbacks ##
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(self.printPrefix + ":on_connect:", "Connected OK")
        else:
            print(self.printPrefix + ":on_connect:", "Bad connection return code =", rc)

    def on_disconnect(self, client, userdata, flags, rc = 0):
        print(self.printPrefix + ":on_disconnect:", "Disconnected result code", str(rc))

    def on_log(self, client, userdata, level, buf):
        print(self.printPrefix + ":on_log:", buf)

    def on_publish(self, client,userdata,result):
        print(self.printPrefix + ":on_publish:", result)

    ## callable funcions ##
    def start(self):
        print(self.printPrefix, "start connection and loop...")
        self.client.connect(self.host)
        self.client.loop_start()
        time.sleep(2)
        print(self.printPrefix, "start successful")
    
    def stop(self):
        print(self.printPrefix, "terminating connection and loop...")
        self.client.loop_stop()
        self.client.disconnect()
        print(self.printPrefix, "client disconnected, terminated")

    def publish(self, topic, data):
        print(self.printPrefix, "publishing ", topic, " = ", data, " ...")
        self.client.publish(topic, data, self.qos, True)
    
    def publishWithCallback(self, topic, _callback = None):
        data = _callback()
        self.publish(topic, data)

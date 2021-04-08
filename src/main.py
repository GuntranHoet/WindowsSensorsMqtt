
import time
import datetime

from MyMQTT.src import MyMQTT as myqtt
from YamlSecrets.src import YamlSecrets as secrets

##########################################################################################

DOMAIN = "chronosphere"

SUB_HEARTBEAT = DOMAIN + "/heartbeat"

TOPIC_HB_DATE = SUB_HEARTBEAT + "/date"
TOPIC_HB_TIME = SUB_HEARTBEAT + "/time"
TOPIC_HB_PING = SUB_HEARTBEAT + "/ping"

##########################################################################################


def heartbeat():
    print("> heartbeat...")

    x = datetime.datetime.now()
    print("> datetime (raw):", x)
    outDate = str(x.strftime("%Y-%m-%d")) # 2020/12/30
    print("> date:", outDate)
    outTime = str(x.strftime("%H:%M:%S")) # 23:01:01
    print("> time:", outTime)

    client.publish(TOPIC_HB_DATE, outDate)
    client.publish(TOPIC_HB_TIME, outTime)

    client.publish(TOPIC_HB_PING, "")


##########################################################################################

# Load secret values from yaml file
# This is to hide personal data from the public repo
s = secrets.YamlSecrets("C:\Python\Projects\WindowsSensorsMqtt\secrets\secrets.yaml")
name = s.find("name")
host = s.find("host")
user = s.find("user")
pasw = s.find("pass")
print("Secrets:", name, host, user, pasw)

# Setup client connection
client = myqtt.MyMQTT(name, host, user, pasw)
client.start()
print("> setup complete.")

# Call functions & loop
while True:
    heartbeat()
    time.sleep(60*5) #5 minutes

# End of program, clean shutdown
print("> stopping program.")
client.stop()
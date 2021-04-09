import time

from MyMQTT.src import MyMQTT as myqtt
from YamlSecrets.src import YamlSecrets as secrets

##########################################################################################

DOMAIN = "chronosphere"

client = None

##########################################################################################


def main():
    # Load secret values from yaml file
    # This is to hide personal data from the public repo
    s = secrets.YamlSecrets("C:\Python\Projects\WindowsSensorsMqtt\secrets\secrets.yaml")
    name = s.find("name")
    host = s.find("host")
    user = s.find("user")
    pasw = s.find("pass")
    print("Secrets:", name, host, user, pasw)

    # Setup client connection
    global client
    client = myqtt.MyMQTT(name, host, user, pasw)
    client.start()
    print("> setup complete.")

    # Call functions & loop
    while True:
        heartbeat()
        storage()
        time.sleep(60*5) # 5 minutes

    # End of program, clean shutdown
    print("> stopping program.")
    client.stop()


def heartbeat():
    import datetime

    SUB_HEARTBEAT = DOMAIN + "/heartbeat"
    TOPIC_PING = SUB_HEARTBEAT + "/ping"

    print("> heartbeat...")
    client.publish(TOPIC_PING, "")


def storage():
    import wmi

    # https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-logicaldisk
    # .Caption      : disk name
    # .Size         : disk total size
    # .FreeSpace    : available disk space
    
    SUB_STORAGE = DOMAIN + "/storage/"
    TOPIC_TOTAL = "/total"
    TOPIC_USED = "/used"
    TOPIC_FREE = "/free"
    TOPIC_PERCENT = "/percent"

    print("> storage...")

    c = wmi.WMI()
    for d in c.Win32_LogicalDisk():
        diskName = d.Caption.replace(":", "")
        print("  > disk:", diskName)

        SUB_DRIVE = SUB_STORAGE + diskName.lower()
        to_gigabytes = 1 / 1024 / 1024 / 1024

        value = int(d.Size) * to_gigabytes
        print("    >", diskName, "total:", value)
        client.publish(SUB_DRIVE + TOPIC_TOTAL, value)

        value = (int(d.Size) - int(d.FreeSpace)) * to_gigabytes
        print("    >", diskName, "used:", value)
        client.publish(SUB_DRIVE + TOPIC_USED, value)

        value = int(d.FreeSpace) * to_gigabytes
        print("    >", diskName, "free:", value)
        client.publish(SUB_DRIVE + TOPIC_FREE, value)

        value = (int(d.Size) - int(d.FreeSpace)) / int(d.Size) 
        print("    >", diskName, "percent:", value)
        client.publish(SUB_DRIVE + TOPIC_PERCENT, value)

##########################################################################################

main()
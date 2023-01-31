from django.shortcuts import render
import time
import paho.mqtt.client as paho
from paho import mqtt
import paho.mqtt.client as mqtt
from time import sleep
import certifi


# Create your views here.
def index(request):
    return render(request, 'CameraInspector/index.html')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_publish(client, userdata, mid):
    print(client, userdata, mid)


def on_log(mqttc, obj, level, string):
    print(string)


def publish(request):
    print("publishing")
    pan = request.GET["pan"]
    tilt = request.GET["tilt"]
    zoom = request.GET["zoom"]
    client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

    client.tls_set(ca_certs=certifi.where())

    # client.tls_set(cert_reqs=ssl.CERT_NONE)

    client.on_publish = on_publish
    client.on_connect = on_connect
    client.on_log = on_log

    # setting password and username
    host = "2be1374228c54154bc14422981467fff.s2.eu.hivemq.cloud"
    client.username_pw_set("admin", "Lumsadmin@n1")
    client.connect(host, 8883, 60)
    client.loop_start()
    client.publish("PTZ/PAN", pan, 1)
    client.publish("PTZ/TILT", tilt, 1)
    client.publish("PTZ/ZOOM", zoom, 1)
    sleep(1)
    pub = 0
    client.disconnect()
    client.loop_stop()

    return render(request, 'CameraInspector/index.html')

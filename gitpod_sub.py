
import paho.mqtt.client as mqtt
from time import sleep
import threading
import json


# Global variables used as configurations
mqtt_host = "mqtt.eclipseprojects.io"
mqtt_port = 1883
mqtt_main_topic = "inesoliveira"
keepalive = 60
mqtt_client = None

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if client.is_connected():
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")
        
def on_disconnect(client, userdata, flags):
    print("MQTT client disconnected")
    mqtt_client.connect(mqtt_host,mqtt_port,keepalive=60);
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_publish = on_publish
    
    mqtt_client.subscribe(f"{mqtt_main_topic}/dados",1)
    
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"MQTT topic subscribed {mid}")
    
def on_publish(client, userdata, mid):
    print(f"MQTT topic published {mid}")

def on_message(client:mqtt.Client, userdata, message):
    global mqtt_client
    resposta = message.payload.decode()
    
    if (message.topic == f"{mqtt_main_topic}/dados"):
        print("File decoded")
        
    

def app_main():
    global mqtt_client
    mqtt_client.connect(mqtt_host,mqtt_port,keepalive=60);
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_publish = on_publish
    
    mqtt_client.subscribe(f"{mqtt_main_topic}/dados",1)
    
    mqtt_client.loop_forever()
    
    
    
    

# Good practices of python
if __name__ == "__main__":
    app_main()
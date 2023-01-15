"""
    Librosa
    Recebe comandos por MQTT
    Envia dados descodificados por MQTT
"""

import paho.mqtt.client as mqtt
from time import sleep
import threading
import json
import numpy as np
import librosa
import librosa.display
#import pyaudio
#import wave
import time 
import matplotlib.pyplot as plt


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
    
    mqtt_client.subscribe(f"{mqtt_main_topic}/comandos",1)
    
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"MQTT topic subscribed {mid}")
    
def on_publish(client, userdata, mid):
    print(f"MQTT topic published {mid}")

def on_message(client:mqtt.Client, userdata, message):
    global mqtt_client
    comando = message.payload.decode()
    
    if (message.topic == f"{mqtt_main_topic}/comandos" and comando == "decode"):
        # Do the librosa stuff 
        
        # Gravação de voz através do microfone do pc (Aquisição de som)

        #CHUNK = 1024
        #FORMAT = pyaudio.paInt16
        #CHANNELS = 2
        RATE = 44100
        #RECORD_SECONDS = 10
        WAVE_OUTPUT_FILENAME = ("test_file.wav")

        #p = pyaudio.PyAudio()

        #stream = p.open(format=FORMAT,
        #                channels=CHANNELS,
        #                rate=RATE,
        #                input=True,
        #                frames_per_buffer=CHUNK)

        #print(f"Mic is recording for {RECORD_SECONDS} seconds")

        #frames = []

        #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #    data = stream.read(CHUNK)
        #    frames.append(data)

        #print("Mic finished recording")

        #stream.stop_stream()
        #stream.close()
        #p.terminate()
        
        #wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb') 
        #wf.setnchannels(CHANNELS)
        #wf.setsampwidth(p.get_sample_size(FORMAT))
        #wf.setframerate(RATE)
        #wf.writeframes(b''.join(frames))
        #wf.close()
        
        
        data, fs = librosa.load(WAVE_OUTPUT_FILENAME,sr=RATE)
        
        data_list = data.tolist()
        data_json = json.dumps(data_list)
        
        with open("decoded.txt", "w") as file:
            file.write(data_json)
        
        print("Reached the end")
        print(mqtt_client.publish(f"{mqtt_main_topic}/dados", "Done"))
    

def app_main():
    global mqtt_client
    mqtt_client.connect(mqtt_host,mqtt_port,keepalive=60);
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_publish = on_publish
    
    mqtt_client.subscribe(f"{mqtt_main_topic}/comandos",1)
    
    mqtt_client.loop_forever()
    
    
    
    

# Good practices of python
if __name__ == "__main__":
    app_main()
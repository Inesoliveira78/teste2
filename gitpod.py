"""
    Streamlit
    Envia comandos por MQTT
    Recebe os dados descodificados por MQTT
"""


import paho.mqtt.client as mqtt
from time import sleep
import threading
import json
import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os


# Global variables used as configurations
mqtt_host = "mqtt.eclipseprojects.io"
mqtt_port = 1883
mqtt_main_topic = "inesoliveira"
keepalive = 60
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if client.is_connected():
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")
        
def on_disconnect(client, userdata, flags):
    print("MQTT disconnected")
    mqtt_client.connect(mqtt_host,mqtt_port,keepalive=60)
    
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"MQTT topic subscribed")
    
def on_publish(client, userdata, mid):
    print(f"MQTT topic published")

def on_message(client:mqtt.Client, userdata, message):
    global mqtt_client
    resposta = message.payload.decode()
    
    if (message.topic == f"{mqtt_main_topic}/dados"):
        len(resposta)
    

def mqtt_thread():
    global mqtt_client
    mqtt_client.connect(mqtt_host,mqtt_port,keepalive=60)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_publish = on_publish
    
    mqtt_client.subscribe(f"{mqtt_main_topic}/dados",1)
    
    mqtt_client.loop_forever()

ticker = threading.Event()

def start_decoding():
    if(os.path.exists("decoded.txt")):
        os.remove("decoded.txt")

    global mqtt_client
    print("Sending decoding command")
    if not mqtt_client.is_connected():
        mqtt_client.connect(mqtt_host,mqtt_port,keepalive=60)
        sleep(1)
    print(mqtt_client.publish(f"{mqtt_main_topic}/comandos", "decode"))

    response = False
    time_passed = 0
    while (not response) and time_passed < 10:
        if(os.path.exists("decoded.txt")):
            response = True
            break
        sleep(1)
        time_passed = time_passed + 1

    if(response):
        print(f"Data received - {time_passed}")
        dados=None
        with open("decoded.txt", "r") as file:
            dados = np.array(file.read().replace('[','').replace(']','').split(','),dtype=np.float64)
        
        col1, col2 = st.columns([1, 2])

        with col1:
            st.audio("test_file.wav")
        



        data, sr = librosa.load("test_file.wav", sr=44100)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # chromagram
        st.subheader('Chromagram')

        plt.figure(figsize=(15, 3))
        chromagram = librosa.feature.chroma_stft(dados,sr=sr)
        librosa.display.specshow(chromagram)
        plt.xlabel('Time [m]')
        plt.ylabel('Frequência [Hz]')
        plt.title("Chromogram")
        st.pyplot()
        
        col1, col2 = st.columns(2)

        with col1:
            # espetrograma
            st.subheader('Espectograma')
            #usar módulo para tirar os imaginários

            D=librosa.amplitude_to_db(abs(librosa.stft(dados)))

            #amplitude em db para o espectograma
            plt.figure(figsize=(12,5))
            D=librosa.amplitude_to_db(np.abs(librosa.stft(dados)))
            librosa.display.specshow(D,x_axis='time',y_axis='linear', sr=sr)
            plt.xlabel('Time')
            plt.ylabel('Frequência [Hz]')
            plt.colorbar()
            plt.title("Espectograma")
            st.pyplot()

        with col2:
            #mel spectograms
            st.subheader('Mel spectogram')
            
            plt.figure(figsize=(12, 5))
            s_audio = librosa.feature.melspectrogram(dados, sr=sr)
            librosa.display.specshow(librosa.power_to_db(s_audio, ref=np.max), y_axis='mel', fmax=8000, x_axis='time', cmap="inferno")
            plt.xlabel('Time')
            plt.ylabel('Frequência [Hz]')
            plt.colorbar(format='%+2.0f dB')
            plt.title("Espectograma")
            st.pyplot()

        # Magnitude total do sinal (sonoridade / parametro de energia)
        st.subheader('Sonoridade')

        plt.figure(figsize=(12, 5))
        librosa.display.waveshow(data, sr=sr)
        plt.xlabel('Time [s]')
        plt.ylabel('Frequência [Hz]')
        plt.title("Sonograma")
        st.pyplot()
        
        # Valor de RMS para cada valor de magnitude
        S, phase = librosa.magphase(librosa.stft(dados)) #frequencia e fase
        rms = librosa.feature.rms(S=S) #root mean square da gravacao
        
        # Grafico
        plt.figure(figsize=(15, 5))
        times = librosa.times_like(rms)
        plt.semilogy(times, rms[0], label='Energia RMS')
        plt.title("Energia RMS")
        st.pyplot()
        
        #zero crossing rate
        st.subheader('Zero Crossing Rate')
        
        zcrs = librosa.feature.zero_crossing_rate(dados)
        print(f"Zero crossing rate: {sum(librosa.zero_crossings(dados))}")
        plt.figure(figsize=(15, 3))
        plt.plot(zcrs[0])
        plt.title('Zero Crossing Rate')
        st.pyplot()
        
    else:
        print("Data not received in time")
        

def app_main():
    thread = threading.Thread(target=mqtt_thread, args=())
    thread.start()

    # Streamlit stuff

    with st.sidebar:
        st.image('imagem.jpg')
        st.title(':blue[Projeto 2º Teste AAIB]')
        st.text('Inês Oliveira')
        st.text('62277')

    if st.button('Start'):
        start_decoding()

    
    
    
    

# Good practices of python
if __name__ == "__main__":
    app_main()
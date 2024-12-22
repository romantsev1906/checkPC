import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import numpy as np
import threading
import time

# Глобальные переменные
is_running = True
keyboard_key = ""
mouse_button = ""

# Функция для проверки микрофона и отображения уровня громкости
def check_microphone():
    global is_running
    try:
        with sd.InputStream(callback=audio_callback):
            while is_running:
                time.sleep(0.1)
    except Exception as e:
        print(f"Ошибка микрофона: {e}")

# Callback для обработки аудио данных
def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    microphone_volume.set(int(volume_norm))

# Функция для проверки клавиатуры
def check_keyboard(event):
    global keyboard_key
    keyboard_key = event.keysym
    keyboard_status.config(text=f"Клавиатура работает (Нажата клавиша: {keyboard_key})", fg="green")

# Функция для проверки мыши
def check_mouse(event):
    global mouse_button
    if event.num == 1:
        mouse_button = "Левая кнопка"
    elif event.num == 3:
        mouse_button = "Правая кнопка"
    else:
        mouse_button = f"Кнопка {event.num}"
    mouse_status.config(text=f"Мышь работает (Нажата кнопка: {mouse_button})", fg="green")

# Функция для завершения тестирования
def stop_testing():
    global is_running
    is_running = False
    messagebox.showinfo("Тестирование завершено", "Тестирование оборудования завершено.")
    root.destroy()

# Создание главного окна
root = tk.Tk()
root.title("Проверка оборудования")
root.geometry("500x400")
root.configure(bg="#f0f0f0")  # Светлый фон для современного UI

# Метки для отображения статусов
keyboard_status = tk.Label(root, text="Проверка клавиатуры...", fg="black", font=("Arial", 12), bg="#f0f0f0")
keyboard_status.pack(pady=10)

mouse_status = tk.Label(root, text="Проверка мыши...", fg="black", font=("Arial", 12), bg="#f0f0f0")
mouse_status.pack(pady=10)

microphone_status = tk.Label(root, text="Проверка микрофона...", fg="black", font=("Arial", 12), bg="#f0f0f0")
microphone_status.pack(pady=10)

# Шкала громкости микрофона
microphone_volume = tk.DoubleVar()
volume_label = tk.Label(root, text="Уровень громкости микрофона:", font=("Arial", 12), bg="#f0f0f0")
volume_label.pack(pady=5)
volume_bar = ttk.Progressbar(root, variable=microphone_volume, maximum=100)
volume_bar.pack(pady=10, fill=tk.X, padx=20)

# Кнопка для завершения тестирования
stop_button = tk.Button(root, text="Завершить тестирование", command=stop_testing, font=("Arial", 12), bg="#ff6347", fg="white")
stop_button.pack(pady=20)

# Обработчики событий для клавиатуры и мыши
root.bind("<Key>", check_keyboard)
root.bind("<Button>", check_mouse)

# Запуск проверки микрофона в отдельном потоке
microphone_thread = threading.Thread(target=check_microphone, daemon=True)
microphone_thread.start()

# Запуск главного цикла
root.mainloop()

import subprocess

def check_wifi():
    try:
        result = subprocess.check_output(["iwgetid"]).decode("utf-8")
        return f"Подключен к Wi-Fi: {result.strip()}"
    except Exception:
        return "Wi-Fi не подключен"

# Пример использования
print(check_wifi())

import platform

def check_system_info():
    info = {
        "Операционная система": platform.system(),
        "Версия ОС": platform.release(),
        "Архитектура": platform.machine(),
        "Версия Python": platform.python_version()
    }
    return "\n".join([f"{key}: {value}" for key, value in info.items()])

# Пример использования
print(check_system_info())

import sounddevice as sd
import numpy as np

def check_speakers():
    try:
        # Воспроизводим звук
        duration = 1  # Длительность звука в секундах
        frequency = 440  # Частота звука (A4)
        samplerate = 44100  # Частота дискретизации
        t = np.linspace(0, duration, int(samplerate * duration), False)
        audio_data = np.sin(frequency * 2 * np.pi * t)
        sd.play(audio_data, samplerate)
        sd.wait()
        return True
    except Exception as e:
        print(f"Ошибка динамиков: {e}")
        return False

# Пример использования
if check_speakers():
    print("Динамики работают")
else:
    print("Динамики не работают")
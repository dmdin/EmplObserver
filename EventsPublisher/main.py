from pynput import keyboard, mouse
import getpass
import win32gui
import win32api
import win32con
import win32process
import time
from KafkaProducer import kafkaPublisher
from Models.WindowsEventModel import WindowsEventModel
import os
from dotenv import load_dotenv

load_dotenv()


username = getpass.getuser()

kafkaHost = os.getenv('KAFKA_HOST')
kafkaPort = os.getenv('KAFKA_PORT')
kafkaUser = os.getenv('KAFKA_USERNAME')
kafkaPassword = os.getenv('KAFKA_PASSWORD')

kafkaServer = f'{kafkaHost}:{kafkaPort}'


kafkaPublisher = kafkaPublisher.kafkaEventsProducer([kafkaServer], kafkaUser, kafkaPassword)

def get_active_file_name():
    active_window = win32gui.GetForegroundWindow()
    process_id = win32process.GetWindowThreadProcessId(active_window)[1]
    handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | 
                                  win32con.PROCESS_VM_READ, False, process_id)
    executable = win32process.GetModuleFileNameEx(handle, 0)

    return  executable.split("\\")[-1]


def on_mouse_click(_,__,___, pressed):
    try:
        if pressed:
            kafkaPublisher.publish_message("winEvents", "event", 
                        WindowsEventModel(UserName=username, AppName=get_active_file_name()).json())
    except Exception as err:
        print(f"Error: {err}")


def on_key_press(_):
    try:
        kafkaPublisher.publish_message("winEvents", "event", 
            WindowsEventModel(UserName=username, AppName=get_active_file_name()).json())
    except Exception as err:
        print(f"Error: {err}")

def start_listener():
    with mouse.Listener(on_click=on_mouse_click) as mouse_listener, \
        keyboard.Listener(on_press=on_key_press) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()

try:
    start_listener()
except Exception as err:
    print(f'Ошибка: {err}')
    time.sleep(500)
    start_listener()
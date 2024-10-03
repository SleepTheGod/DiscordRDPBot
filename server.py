import socket
import pyautogui
import threading
import os
from PIL import ImageGrab
import io
import time

SERVER_PORT = 8080

def perform_mouse_move(x, y):
    pyautogui.moveTo(x, y)

def perform_mouse_click(button):
    if button == 'LEFT':
        pyautogui.click(button='left')
    elif button == 'RIGHT':
        pyautogui.click(button='right')

def perform_key_press(key):
    pyautogui.press(key)

def capture_screenshot():
    screenshot = ImageGrab.grab()
    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def handle_client_commands(client_socket):
    while True:
        command = client_socket.recv(1024).decode('utf-8')
        if not command:
            break
        
        if command.startswith('MOUSE_MOVE'):
            _, x, y = command.split()
            perform_mouse_move(int(x), int(y))
        elif command.startswith('MOUSE_CLICK'):
            _, button = command.split()
            perform_mouse_click(button)
        elif command.startswith('KEY_PRESS'):
            _, key = command.split()
            perform_key_press(key)
        elif command == 'SCREENSHOT':
            screenshot_data = capture_screenshot()
            client_socket.sendall(screenshot_data)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', SERVER_PORT))
        server_socket.listen()
        print('Remote control server started...')
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f'Connected by {addr}')
            client_handler = threading.Thread(target=handle_client_commands, args=(client_socket,))
            client_handler.start()

if __name__ == '__main__':
    start_server()

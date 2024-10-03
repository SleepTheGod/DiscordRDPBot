import socket
import subprocess
import psutil

# IP address and port the server will listen on
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5555       # Arbitrary port number

# Function to start RDP session on the server
def start_rdp():
    command = "mstsc"
    subprocess.run(command, shell=True)

# Function to retrieve system information
def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    uptime = psutil.boot_time()
    return f'CPU: {cpu_percent}%\nMemory: {memory.percent}%\nUptime: {uptime}'

# Main server loop
def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server started, listening on {HOST}:{PORT}...')

        while True:
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                data = conn.recv(1024).decode()

                # Handle incoming commands
                if data == 'start_rdp':
                    start_rdp()
                    conn.sendall(b'RDP session started.')
                elif data == 'system_info':
                    system_info = get_system_info()
                    conn.sendall(system_info.encode())
                else:
                    conn.sendall(b'Unknown command.')

if __name__ == '__main__':
    server()

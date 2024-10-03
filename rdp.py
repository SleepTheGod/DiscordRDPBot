import discord
import socket
import subprocess
import psutil
import asyncio
import json
import threading

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # Replace with your Discord bot token
AUTHORIZED_USERS = ['your_discord_user_id']  # Replace with your Discord user ID(s)

HOST = '0.0.0.0'  # Listen on all interfaces for the server-side
PORT = 5555       # Arbitrary port number for the server-side

# Load RDP configuration (server IPs)
with open('rdp_config.json') as f:
    rdp_config = json.load(f)

# Discord client setup
client = discord.Client()

# Helper function to send commands to remote servers
def send_command(server_ip, command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, PORT))
            s.sendall(command.encode())
            response = s.recv(1024).decode()
            return response
    except Exception as e:
        return f'Error: {e}'

# Server-side function to start RDP session
def start_rdp():
    command = "mstsc"
    subprocess.run(command, shell=True)

# Server-side function to retrieve system information
def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    uptime = psutil.boot_time()
    return f'CPU: {cpu_percent}%\nMemory: {memory.percent}%\nUptime: {uptime}'

# Server-side listener
def server_listener():
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

# Discord bot functionality
@client.event
async def on_ready():
    print(f'Bot is ready. Logged in as {client.user}')

@client.event
async def on_message(message):
    # Only process commands from authorized users
    if str(message.author.id) not in AUTHORIZED_USERS:
        return

    if message.content.startswith('!rdp'):
        _, machine_name = message.content.split()

        # Find the machine in the configuration file
        machine = next((m for m in rdp_config['machines'] if m['name'] == machine_name), None)

        if machine:
            response = send_command(machine['ip'], 'start_rdp')
            await message.channel.send(f'Response from {machine_name}: {response}')
        else:
            await message.channel.send(f'Machine "{machine_name}" not found in the configuration.')

    elif message.content.startswith('!status'):
        _, machine_name = message.content.split()

        # Find the machine in the configuration file
        machine = next((m for m in rdp_config['machines'] if m['name'] == machine_name), None)

        if machine:
            response = send_command(machine['ip'], 'system_info')
            await message.channel.send(f'System info for {machine_name}:\n{response}')
        else:
            await message.channel.send(f'Machine "{machine_name}" not found in the configuration.')

# Start both the Discord bot and the server listener
if __name__ == '__main__':
    # Start the server listener in a separate thread
    server_thread = threading.Thread(target=server_listener)
    server_thread.daemon = True
    server_thread.start()

    # Start the Discord bot
    client.run(TOKEN)

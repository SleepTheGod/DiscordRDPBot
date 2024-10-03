import discord
import socket
import json

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # Replace with your bot token
AUTHORIZED_USERS = ['your_discord_user_id']  # Replace with your Discord user ID(s)

# Load RDP configuration (server IPs)
with open('rdp_config.json') as f:
    rdp_config = json.load(f)

client = discord.Client()

# Helper function to send commands to the server
def send_command(server_ip, command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, 5555))
            s.sendall(command.encode())
            response = s.recv(1024).decode()
            return response
    except Exception as e:
        return f'Error: {e}'

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

client.run(TOKEN)

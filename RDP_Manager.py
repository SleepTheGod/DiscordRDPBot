import discord
import subprocess
import psutil
import json
import os

# Load RDP configuration
with open('rdp_config.json') as f:
    rdp_config = json.load(f)

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # Replace with your bot token
AUTHORIZED_USERS = ['your_discord_user_id']  # Replace with your Discord user ID(s)
RDP_COMMAND = 'mstsc /v:'  # RDP command

client = discord.Client()

# Helper function to start RDP session
def start_rdp(ip, username, password):
    command = f'cmdkey /generic:{ip} /user:{username} /pass:{password} && {RDP_COMMAND}{ip}'
    subprocess.run(command, shell=True)

# Helper function to get system information
def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    uptime = psutil.boot_time()
    return f'CPU: {cpu_percent}%\nMemory: {memory.percent}%\nUptime: {uptime}'

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
            await message.channel.send(f'Connecting to {machine["name"]} ({machine["ip"]})...')
            start_rdp(machine['ip'], machine['username'], machine['password'])
        else:
            await message.channel.send(f'Machine "{machine_name}" not found in the configuration.')

    elif message.content.startswith('!status'):
        system_info = get_system_info()
        await message.channel.send(f'System Info:\n{system_info}')

client.run(TOKEN)

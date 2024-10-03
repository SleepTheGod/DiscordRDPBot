import discord
import socket
import asyncio
import io
from PIL import Image
from discord.ext import tasks

# Discord Bot Token
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # Replace with your bot token
SERVER_IP = '192.168.1.100'  # Replace with your laptop's IP
SERVER_PORT = 8080

client = discord.Client()

async def send_command_to_server(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(command.encode('utf-8'))
        except Exception as e:
            print(f"Error sending command: {e}")

async def get_screenshot():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(b'SCREENSHOT')
            screenshot_data = s.recv(1000000)  # Adjust the buffer size if necessary
            return screenshot_data
        except Exception as e:
            print(f"Error getting screenshot: {e}")
            return None

@client.event
async def on_ready():
    print(f'Bot is ready. Logged in as {client.user}')
    start_screenshot_task.start()  # Start screenshot streaming

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Mouse move
    if message.content.startswith('!mouse_move'):
        _, x, y = message.content.split()
        await send_command_to_server(f'MOUSE_MOVE {x} {y}')
        await message.channel.send(f"Mouse moved to {x}, {y}")

    # Mouse click
    elif message.content.startswith('!mouse_click'):
        _, button = message.content.split()
        await send_command_to_server(f'MOUSE_CLICK {button}')
        await message.channel.send(f"Mouse {button} clicked.")

    # Key press
    elif message.content.startswith('!key_press'):
        _, key = message.content.split()
        await send_command_to_server(f'KEY_PRESS {key}')
        await message.channel.send(f"Key '{key}' pressed.")

@tasks.loop(seconds=5)  # Adjust the interval for how often to get screenshots
async def start_screenshot_task():
    screenshot_data = await get_screenshot()
    if screenshot_data:
        with io.BytesIO(screenshot_data) as img_io:
            img_io.seek(0)
            img = Image.open(img_io)
            with io.BytesIO() as output:
                img.save(output, format="PNG")
                output.seek(0)
                screenshot_file = discord.File(fp=output, filename="screenshot.png")
                channel = client.get_channel(YOUR_CHANNEL_ID)  # Replace with your channel ID
                await channel.send(file=screenshot_file)

client.run(TOKEN)

# Discord RDP Bot

Welcome to DiscordRDPBot, a Python-based Discord bot for controlling Remote Desktop Protocol (RDP) sessions between multiple machines over a network. 
This tool enables you to manage your machines via Discord commands, facilitating remote system administration.

# Features
Remote Desktop Control Start an RDP session to the target machine via Discord commands.
System Information Retrieval Fetch CPU, memory usage, and uptime details remotely.
Full Automation Automate RDP sessions and system commands without direct machine access.
Client-Server Architecture Client and server-side scripts for communicating between machines.

# Files in This Repo
RDP_Manager.py The main manager script for handling all functionalities.
clientside.py Client-side script responsible for sending requests to the server.
rdp.py Handles the execution of RDP-related commands.
rdp_config.json Configuration file that stores machine details (IP, name) for RDP control.
remote.py Additional script for performing remote actions on the system.
server.py Server-side script that listens for incoming commands from clients.
serverside.py Extension of the server-side functionality.
requirements.txt Dependencies required to run the Discord bot and other scripts.

# Setup Instructions

# Prerequisites
Python 3.x installed on both client and server machines.
RDP enabled on target machines.
A Discord account and bot token.

# Step 1 Clone the Repository
```bash
git clone https://github.com/SleepTheGod/DiscordRDPBot
cd DiscordRDPBot
```
# Step 2 Install Required Dependencies
Run the following command to install all required dependencies
```bash
pip install -r requirements.txt
```

# Step 3 Setup the RDP Configuration
Edit the rdp_config.json file to include the details of your machines
```json
{
  "machines": [
    {
      "name": "Server1",
      "ip": "192.168.1.10"
    },
    {
      "name": "Server2",
      "ip": "192.168.1.11"
    }
  ]
}
```

# Step 4 Configure Your Discord Bot
Go to Discord Developer Portal and create a new application.
Generate a bot token under the "Bot" section.
Copy the bot token and paste it into the TOKEN variable inside RDP_Manager.py

```python
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
```

# Step 5 Run the Server-Side Script
On the machine that will act as the server (the machine being controlled)
```bash
python serverside.py
```

The server will now listen for commands from the Discord bot.

# Step 6 Run the Client-Side Script
On your controlling machine (client)
```bash
python clientside.py
```

# Step 7 Run the Main Bot
Finally, run the Discord bot to handle incoming commands
```bash
python RDP_Manager.py
```

# Usage
Once everything is set up, you can control your machines via Discord commands.

# Commands
!rdp <machine_name> Start an RDP session to the target machine.
Example !rdp Server1
!status <machine_name> Retrieve system information (CPU, memory, uptime) from the machine.
Example !status Server1

# Contributions
Feel free to fork this repository, submit issues, or send pull requests. Any contributions to enhance the project are welcome.

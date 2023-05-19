import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
DISCORD_GUILD = int(os.environ['DISCORD_GUILD'])
DISCORD_LOGGING_CHANNEL = int(os.environ['DISCORD_LOGGING_CHANNEL'])
DISCORD_ALLOWED_USER = set(map(int, os.environ['DISCORD_ALLOWED_USERS'].split(',')))

RCON_HOST = os.environ['RCON_HOST']
RCON_PORT = int(os.environ['RCON_PORT'])
RCON_PASSWORD = os.environ['RCON_PASSWORD']

FTP_HOST = os.environ['FTP_HOST']
FTP_PORT = int(os.environ['FTP_PORT'])
FTP_USERNAME = os.environ['FTP_USERNAME']
FTP_PASSWORD = os.environ['FTP_PASSWORD']

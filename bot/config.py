import os
from dotenv import load_dotenv

load_dotenv() # Loads environment variables

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
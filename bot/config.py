import os
from dotenv import load_dotenv

load_dotenv() # Loads environment variables

TOKEN = os.getenv("DISCORD_TOKEN")
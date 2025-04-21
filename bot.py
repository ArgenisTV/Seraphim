import os
import discord
from discord import FFmpegPCMAudio
import yt_dlp 
from discord.ext import commands # Allows commands creation
from dotenv import load_dotenv # Just loads variables from the .env file

load_dotenv() # Loads environment variables
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default() # Indicates the type of events the bot can listen to. For now, default events
intents.message_content = True # This is needed for the bot to be able to read messages

bot = commands.Bot(command_prefix="s!", intents=intents) # Rules how commands should start. "s!"

@bot.event
async def on_ready():
    print(f"{bot.user} Be not afraid!")

@bot.command()
async def ping(ctx): # Mainly a test command. CTX is the command context, such as who wrote, on which channel, etc.
    await ctx.send("Use me, will you?") 

# Execute bot
bot.run(TOKEN) # 


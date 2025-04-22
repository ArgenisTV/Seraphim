import discord
from config import DISCORD_TOKEN
from discord.ext import commands # Allows commands creation
from dotenv import load_dotenv # Just loads variables from the .env file
from player import MusicPlayer
from providers.youtube import YoutubeProvider

intents = discord.Intents.default() # Indicates the type of events the bot can listen to. For now, default events
intents.message_content = True # This is needed for the bot to be able to read messages

bot = commands.Bot(command_prefix="s!", intents=intents) # Rules how commands should start. "s!"
player = MusicPlayer(bot, audio_provider=YoutubeProvider()) # Dependency injection

@bot.event
async def on_ready():
    print(f"Heed {bot.user}! Be not afraid!")

@bot.command()
async def ping(ctx): 
    await ctx.send("Use me, will you?") # Mainly a test command. CTX is the command context, such as who wrote, on which channel, etc.

@bot.command()
async def play(ctx, *, url:str):
    await player.play(ctx, url)

@bot.command()
async def pause(ctx):
    await player.pause(ctx)
    
@bot.command()
async def resume(ctx):
    await player.resume(ctx)
    
@bot.command()
async def stop(ctx):
    await player.stop(ctx)

# Execute bot
bot.run(DISCORD_TOKEN)
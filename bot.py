import os
import discord
import yt_dlp # Extracts info and URLs from Youtube
from discord import FFmpegPCMAudio
from discord.ext import commands # Allows commands creation
from dotenv import load_dotenv # Just loads variables from the .env file
from fuzzywuzzy import fuzz # Used to get the best match for a song's name

load_dotenv() # Loads environment variables
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default() # Indicates the type of events the bot can listen to. For now, default events
intents.message_content = True # This is needed for the bot to be able to read messages

bot = commands.Bot(command_prefix="s!", intents=intents) # Rules how commands should start. "s!"

@bot.event
async def on_ready():
    print(f"{bot.user} Be not afraid!")

@bot.command()
async def ping(ctx): 
    await ctx.send("Use me, will you?") # Mainly a test command. CTX is the command context, such as who wrote, on which channel, etc.

@bot.command()
async def play(ctx, url: str): # What happens when the bot recognizes the play command.
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None # Checks if the user is in a voice channel.

    if not voice_channel: 
        await ctx.send("Joined a voice channel, you have not.")
        return # Throws error message if user is not in a voice channel.

    # Connecting to a voice channel
    voice_client = ctx.voice_client
    if not voice_client:
        voice_client = await voice_channel.connect() # If not connected, joins the user's voice channel.
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel) # If connected to a different voice channel, moves to the user's.

    await ctx.send(f"Thy choice shall be considered...") # Message shown while the bot is searching for the audio.

    # Options for audio stream
    ydl_opts ={
        'format' : 'bestaudio/best',
        'quiet': True, # No console logs
        'noplaylist': True, 
        'default_search': 'ytsearch', # Defaults to YouTube search if not using a URL.
        'extract_flat': 'in_playlist',
    }

    # Video info is extracted
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False) 

        # If multiple results are found, the closest match to the requested song's name is chosen.
        if 'entries' in info:
            best_match = None
            highest_score = 0
            for entry in info['entries']: # For each result from the given "URL" (song name), consider how much it matches with the URL and choose the one with the highest score.
                title = entry.get('title', '').lower()
                score = fuzz.partial_ratio(title, url.lower()) # From library FuzzyWuzzy. This measures the similarity between Strings from 0 to 100.
                if score > highest_score: 
                    best_match = entry
                    highest_score = score
            info = best_match

    # Reproduce audio through FFmpeg
    source = FFmpegPCMAudio(audio_url)
    if voice_client.is_playing():
        voice_client.add()
    voice_client.play(source)
    await ctx.send(f" Heed: **{title}**")

# Execute bot
bot.run(TOKEN)




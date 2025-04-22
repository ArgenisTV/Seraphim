from collections import deque # Data structure for the queue.
import asyncio
from discord import FFmpegPCMAudio # Needed to create audio sources
from fuzzywuzzy import fuzz # Used to get the best match for a song's name
import yt_dlp # Extracts info and URLs from Youtube
import re # Will validate if the request is a URL or text search.

class MusicPlayer:
    def __init__(self, bot):
        self.bot = bot
        self.playlist = deque() # The current song and next ones.
        self.previous_songs = deque(maxlen=5) # Previous songs. Used in the !previous command
        
        
    async def play(self, ctx, *, url): # What happens when the bot recognizes the play command.
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None # Checks if the user is in a voice channel.
        
        if not voice_channel: 
            await ctx.send("Thou must join a voice channel before summoning cosmical vibrations!")
            return # Throws error message if user is not in a voice channel.

        # Connecting to a voice channel
        voice_client = ctx.voice_client
        if not voice_client:
            voice_client = await voice_channel.connect() # If not connected, joins the user's voice channel.
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel) # If connected to a different voice channel, moves to the user's.

        await ctx.send(f"Thy choice shall be considered...") # Message shown while the bot is searching for the audio.

        # Options for Youtube audio stream
        ydl_opts ={
            'format' : 'bestaudio/best',
            'quiet': True, # No console logs
            'noplaylist': True, 
            'extractaudio': True,
            'audioformat': 'mp3',
            'default_search': 'ytsearch', # Defaults to YouTube search if not using a URL.
            'extract_flat': 'in_playlist',
        }

        # Video info is extracted
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False) 

            # Obtain URL for the best match
            # audio_url = info.get('url') // Used when the method was defined in bot.py. Not needed anymore

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
            
            # If no valid info is found
            if not info:
                await ctx.send("No tune found worthy of thine ears!")
                return
            
            # Append song to playlist 
            self.playlist.append(info)
            await ctx.send(f"{voice_client.user}! Thy request... is worthy. Will attune to: *{info['title']}*")
            
            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await self.play_next(ctx)

        # Create an audio source through FFmpeg
        # source = FFmpegPCMAudio(audio_url) // Used when the method was defined in bot.py. Not needed anymore

    async def play_next(self, ctx):
        if not self.playlist:
            await ctx.send("Cosmical vibrations' resonance attenuated...")
            return # Message when the queue is empty.
        
        # Pop the next song into the previous songs queue
        info = self.playlist.popleft() 
        self.previous_songs.append(info)

        audio_url = info['url']
        audio_source = FFmpegPCMAudio(audio_url, option='-vn') # VN = No video

        def after_playing(error):
            fut = asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop) # Future. A corroutine is called to handle the asyncronic task of waiting for the song to end. 

            # Try catch for any exceptions during the corroutine execution. 
            try:
                fut.result() 
            except Exception as e:
                print(e)
                
            # Error handling is needed here because the function occurs outside of the bot's main loop.
            # We need an async function to be executed and be disguised as a sync function.  

        ctx.voice_client.play(audio_source, after=after_playing)
        await ctx.send(f"Attuning to: *{info['title']}*") 

    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("{bot.user} *Freezes*")
        else:
            await ctx.send("*Stares*")

    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("*Awakens")
        else:
            await ctx.send("*Fixates on you for a second*")
            
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("{bot.user} *Slumbers*")
        else:
            await ctx.send("{bot.user} *Flaps half its wings*")
from collections import deque # Data structure for the queue.
import asyncio
from discord import FFmpegPCMAudio # Needed to create audio sources
from fuzzywuzzy import fuzz # Used to get the best match for a song's name
import yt_dlp # Extracts info and URLs from Youtube
import re # Will validate if the request is a URL or text search.

# def __init__(self, bot, audio_provider: AudioProvider):
# self.audio_provider = audio_provider

class MusicPlayer:
    def __init__(self, bot, yt_provider, sp_provider):
        self.bot = bot
        self.playlist = deque() # The current song and next ones.
        self.previous_songs = deque(maxlen=5) # Previous songs. Used in the !previous command
        self.yt_provider = yt_provider
        self.sp_provider = sp_provider
        
    async def play(self, ctx, url): # What happens when the bot recognizes the play command.
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None # Checks if the user is in a voice channel.
        
        if not voice_channel: 
            await ctx.send("Thou must join a voice channel before summoning cosmical vibrations!")
            return # Throws error message if user is not in a voice channel.

        # Connecting to a voice channel
        voice_client = ctx.voice_client
        if not voice_client:
            voice_client = await voice_channel.connect() # If not connected, joins the user's voice channel.
            await ctx.send(f"Heed [TDM] Seraphim! Be not afraid!")
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel) # If connected to a different voice channel, moves to the user's.

        await ctx.send(f"Thy choice shall be considered...") # Message shown while the bot is searching for the audio.

        try:
            # This line was from before two providers existed. info = await self.audio_provider.search(url)
            if "open.spotify.com" in url:
                info = await self.sp_provider.search(url)
                info = await self.yt_provider.search(info["title"])
            else:
                info = await self.yt_provider.search(url)
        except Exception as e: # e is not used because if a song is not found, the error message will be the same regardless of the provider.
            await ctx.send("No tune found worthy of thine ears!")
            return
        
        # Append song to playlist 
        self.playlist.append(info)
        
        # Send a message if the song is queued instead of played directly. Else, next song is played.
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            position = len(self.playlist) + 1
            await ctx.send(f"Requested resonance '{info['title']}' fixated in time at #{position}")
        else:
            await self.play_next(ctx)
        
        # Create an audio source through FFmpeg
        # source = FFmpegPCMAudio(audio_url) // Used when the method was defined in bot.py. Not needed anymore

    async def play_next(self, ctx, from_previous=False):
        if not self.playlist:
            await ctx.send("Cosmical vibrations' resonance attenuated...")
            await ctx.voice_client.disconnect()
            return # Message when the queue is empty.
        
        # Pop the next song into the previous songs queue
        info = self.playlist.popleft() 

        audio_url = info['url']
        audio_source = FFmpegPCMAudio(audio_url, options='-vn') # VN = No video

        def after_playing(error):
            if info and not from_previous: 
                self.previous_songs.append(info) # This will store the song after it is finished
                
            fut = asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop) # Future. A corroutine is called to handle the asyncronic task of waiting for the song to end. 
            # Simply put, this will trigger whenever a song ends.
            
            # Try catch for any exceptions during the corroutine execution. 
            try:
                fut.result() 
            except Exception as e:
                print(e)
                
            # Error handling is needed here because the function occurs outside of the bot's main loop.
            # We need an async function to be executed and be disguised as a sync function.  

        ctx.voice_client.play(audio_source, after=after_playing)
        await ctx.send(f"Thy request... is worthy! Attuning to: *{info['title']}*") 

    async def play_previous(self, ctx): # PREVIOUS NOT WORKING CORRECTLY YET
        # If previous_songs is empty
        if not self.previous_songs:
            await ctx.send("No cosmical vibrations hath traversed yet!")
        else:            
            info = self.previous_songs.pop() # Grab the previous song
            current_song = None # Used in if validation later
            
            # If there is a current song, insert it after the one that is about to be played (info)
                
            if ctx.voice_client and ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                # If there's a current song, store it
                if self.playlist:
                    current_song = self.playlist.popleft()
            else:
                await ctx.send(f"Traversing back through the cosmic stream... Reattuning to: *{info['title']}*")
                
            self.playlist.appendleft(info) # Insert song into the start of the queue
            
            if current_song:
                self.playlist.appendleft(current_song) # This will append it next to the song that is about to be played by s!previous so that the order is not lost
            
            if ctx.voice_client and ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                ctx.voice_client.stop()
            else:
                await self.play_next(ctx, from_previous=True)
            
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("*Freezes*")
        else:
            await ctx.send("*Stares*")

    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("*Awakens*")
        else:
            await ctx.send("*Fixates on you for a second*")
            
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("*Slumbers*")
        else:
            await ctx.send("In its slumber, Seraphim flaps half its wings")
            
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            ctx.voice_client.stop() # This will automatically trigger after_playing which will call play_next
        else:
            await ctx.send("Non-existent resonance fixated in the future...")
        
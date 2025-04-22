from base import AudioProvider
from yt_dlp import YoutubeDL
from fuzzywuzzy import fuzz

class YoutubeProvider(AudioProvider):
    
    def __init__(self):
        # Options for Youtube audio stream
        self.ydl_opts = {
            'format' : 'bestaudio/best',
            'quiet': True, # No console logs
            'noplaylist': True, 
            'extractaudio': True,
            'audioformat': 'mp3',
            'default_search': 'ytsearch', # Defaults to YouTube search if not using a URL.
            'extract_flat': 'in_playlist',
        }

    async def search(self, url:str) -> dict:
        # Video info is extracted
        with YoutubeDL(self.ydl_opts) as ydl:
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
                raise Exception("Tune amiss!")
            
            return info
from bot.providers.base import AudioProvider
from yt_dlp import YoutubeDL
from fuzzywuzzy import fuzz
from urllib.parse import urlparse, parse_qs

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
            'extract_flat': 'True',
        }

    def extract_video_id(self, url: str) -> str:
        # If it is a Short URL
        if "youtu.be" in url:
            return url.split("/")[-1]
        
        # If it is a Long URL
        parsed_url = urlparse(url)
        if "youtube.com" in parsed_url.netloc:
            # Search for parameter 'v' which contains the video ID
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        
        # If the URL is not valid or does not contain a video ID
        raise ValueError("Could not extract video ID from given URL")
    
    def is_youtube_url(self, url: str) -> bool:
        # Validates if the given URL is from Youtube
        return "youtube.com" in url or "youtu.be" in url

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
import spotipy # Allows interaction with Spotify's API
from spotipy.oauth2 import SpotifyClientCredentials

from .base import AudioProvider # Imports base interface

class SpotifyProvider(AudioProvider):
    # Seemingly, bots cannot play music from Spotify directly.
    # Thus, music info will be extracted from a Spotify URL and the player will use Youtube.
    
    def __init__(self, sp_client = None):
        # Spotipy client initialization through client auth
        # sp_client allows tests to be ran without needing to validate Spotify Client ID
        self.sp = sp_client or spotipy.Spotify(
            auth_manager=SpotifyClientCredentials())
        
        
    async def search(self, url: str) -> dict:
        # Creates a dictionary using the URL.
        
        if "open.spotify.com" not in url:
            raise ValueError("Given URL is not from Spotify")
        
        # Extract id, info, song and artist name to then return an info type object.
        track_id = self.extract_track_id(url)
        track_info = self.sp.track(track_id)
        track_name = track_info["name"]
        artists = ", ".join([artist["name"] for artist in track_info["artists"]])
        
        # Define a search as "Song - Artist"
        search_url = f"{track_name} - {artists}"
        
        return {
            "title": search_url,
            "url": search_url 
        }
        
    def extract_track_id(self, url: str) -> str:
        parts = url.split("/")
        track_part = parts[-1] # This grabs the last part of the URL
        track_id = track_part.split("?")[0] # This removes extra parameters that are found after "?si"
            
        return track_id
import pytest
from unittest.mock import MagicMock
from bot.providers.spotify import SpotifyProvider

@pytest.fixture
def sp_provider():
    # Initialize an instance of SpotifyProvider for the tests
    provider = SpotifyProvider(sp_client=MagicMock())
    provider.sp = MagicMock() 
    return provider

@pytest.mark.asyncio
async def test_search_valid_spotify_url(sp_provider):
    # Verify correct processing of a valid Spotify URL
    
    # Simulation of the response Spotipy would return
    sp_provider.sp.track.return_value = {
        "name": "Coffin Nails",
        "artists": [{"name": "MF DOOM"}]
    }
    
    url = "https://open.spotify.com/track/0o73cSWmV0YJeHvzDbJDdn"
    result = await sp_provider.search(url)
    
    assert "Coffin Nails" in result["title"]
    assert "MF DOOM" in result["title"]
    assert result["url"] == result["title"] # URL and Title are supposed to end up being the same so as to search on Youtube
    
@pytest.mark.asyncio
async def test_search_invalid_url(sp_provider):
    # Verify if the URL is not from Spotify and throw a ValueError
    
    invalid_url = "https://www.youtube.com/watch?v=6iFbuIpe68k&ab_channel=Z%C3%A0tur"
    
    with pytest.raises(ValueError):
        await sp_provider.search(invalid_url)
        
def test_extract_track_id():
    # Verify that the ID can be properly extracted from a Spotify URL
    
    provider = SpotifyProvider(sp_client=MagicMock())
    
    url = "https://open.spotify.com/track/0o73cSWmV0YJeHvzDbJDdn?si=78ccd10118044b7f"
    track_id = provider.extract_track_id(url)
    
    assert track_id == "0o73cSWmV0YJeHvzDbJDdn"
import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.player import MusicPlayer

class FakeYoutubeProvider:
    async def search(self, url):
        return {
            'title': f"Mock result for {url}",
            'url': "https://www.youtube.com/watch?v=sd-dK8OqtVU&ab_channel=MFDOOM-Topic"
        }
        
class FakeSpotifyProvider:
    async def search(self, url: str) -> dict:
        return {
            "title": "Coffin Nails - MF DOOM",
            "url": "Coffin Nails - MF DOOM" # URL is only used for the Youtube search
        }
            
@pytest.mark.asyncio 
async def test_play_adds_song_to_playlist():
    
    # mock_ctx is a Discord Context (ctx) simulation
    mock_ctx = MagicMock()
        
    # Voice channel simulation 
    mock_channel = AsyncMock()
    
    # Simulate conection to a voice channel
    mock_voice_client = MagicMock()
    
    # The Play method requires "voice_client" to have "is_playing" and "is_paused" attributes
    # For the mock test not to fail, a value must be "returned" for both attributes. In this case, False     
    # *NEW CHANGE* The test fails because assert confirms that the queue length is 1, but the logic is that as soon as the song is played, it leaves the playlist and goes into the previous_playlist.
    # Because of that, the playlist that assert is validating will have a length of 0 at the time of the test.
    # Due to this "limitation", the is_playing attribute will be set to True so that the test does not call play_next(). See line 55 for more info.
    mock_voice_client.is_playing.return_value = True 
    mock_voice_client.is_paused.return_value = False
    
    # Also, since "move_to" is a sync function, the play method could not be called using await as await is reserved for Async functions.
    # Thus, the "move_to" function is defined as AsyncMock() for the sake of the test.
    mock_voice_client.move_to = AsyncMock()
    mock_voice_client.play = MagicMock()
    
    # Returns the mock_voice_client for the connection to be simulated
    mock_channel.connect = AsyncMock(return_value=mock_voice_client)
    
    mock_ctx.author.voice.channel = mock_channel
    
    # Simulates the bot is not yet connected to a voice channel
    mock_ctx.voice_client = mock_voice_client
    
    mock_ctx.send = AsyncMock() # Simulates bot's messages
    
    # A MusicPlayer instance is created using the fake provider
    player = MusicPlayer(bot=MagicMock(), yt_provider=FakeYoutubeProvider(), sp_provider=FakeSpotifyProvider())
    
    # Play method executed with a generic fake query
    await player.play(mock_ctx, url="https://www.youtube.com/watch?v=sd-dK8OqtVU&ab_channel=MFDOOM-Topic")
    
    # Assert helps validate if the song is added to the queue.
    # If I wanted to test that play() is indeed called, but not test its functionality, this line should be "mock_voice_client.play.assert_called_once()"
    assert len(player.playlist) == 1
    assert "Mock result" in player.playlist[0]["title"]
    
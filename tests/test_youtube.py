import pytest
from unittest.mock import MagicMock
from bot.providers.youtube import YoutubeProvider

@pytest.fixture
def yt_provider():
    # Initialize an instance of YoutubeProvider
    provider = YoutubeProvider()
    provider.ydl_opts = MagicMock() # Mock for yt_dlp options
    return provider

@pytest.mark.asyncio
async def test_search_valid_youtube_url(yt_provider):
    yt_provider.ydl_opts.extract_info = MagicMock(return_value={
        'entries': [
        {'title': 'Epic Sax Guy - 10 Hour Version - But when does the beat drop? 🤔', 'url': 'https://www.youtube.com/watch?v=ez8m4PXksQs&t=25730s&ab_channel=EurovisionSongContest'}
        ]
    })

    url = "https://www.youtube.com/watch?v=ez8m4PXksQs&t=25730s&ab_channel=EurovisionSongContest"
    result = await yt_provider.search(url)
    
    assert "Epic Sax Guy - 10 Hour Version - But when does the beat drop? 🤔" in result["title"]
    assert result["url"] == "https://www.youtube.com/watch?v=ez8m4PXksQs&t=25730s&ab_channel=EurovisionSongContest"
    
@pytest.mark.asyncio
async def test_search_invalid_url(yt_provider):
    
    invalid_url = "https://open.spotify.com/track/0o73cSWmV0YJeHvzDbJDdn?si=9c54475206594177"
    
    with pytest.raises(ValueError):
        await yt_provider.search(invalid_url)
        
def test_extract_video_id():
    provider = YoutubeProvider()
    
    url = "https://www.youtube.com/watch?v=ez8m4PXksQs&t=25730s&ab_channel=EurovisionSongContest"
    video_id= provider.extract_video_id(url)
    
    assert video_id == "ez8m4PXksQs"

def test_is_youtube_url():
    # Verify that the provided URL is from Youtube
    provider = YoutubeProvider()
    
    valid_url = "https://www.youtube.com/watch?v=ez8m4PXksQs&t=25730s&ab_channel=EurovisionSongContest"
    invalid_url = "https://open.spotify.com/track/0o73cSWmV0YJeHvzDbJDdn?si=fe6fe74082854de9"
    
    # These throw error "No module named 'termios' because yt-dlp attempts to import library "termios"
    # Which is not available in Windows. It is a Unix system specific module.
    assert provider.is_youtube_url(valid_url) 
    assert not provider.is_youtube_url(invalid_url)
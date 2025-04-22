from abc import ABC, abstractmethod # Abstract Base Class

class AudioProvider(ABC):
    
    # This is a base interface for all audio providers
    # Defines what every provider class should comply with.
    
    @abstractmethod
    async def search (self, query:str) -> dict:
        pass # Runs a search and returns a dict with the audio info.
    
    
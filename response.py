import json
from typing import Generic, List, TypeVar

from scrapers.scraper import ScrapedItem


T = TypeVar('T', bound=List[ScrapedItem])
class Response(Generic[T]):
    def __init__(self, data : T = None, error: bool = False, message: str = None):
        self.data = data
        self.error = error
        self.message = message
        
    def json(self) :
        return json.dumps(
            {
                "error": self.error,
                "message": self.message,
                "data": [item.to_dict() for item in self.data] if self.data else None
            }
        ) 
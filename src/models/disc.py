from dataclasses import dataclass
from typing import Optional


@dataclass
class Disc:
    """Represents a Minecraft music disc."""
    id: str
    name: str
    artist: str
    description: str = ""
    how_to_obtain: str = ""
    protected: bool = False
    image_url: Optional[str] = None
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Disc):
            return False
        return self.id == other.id

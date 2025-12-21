from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.disc import Disc
from src.models.collection import Collection


class IDiscRepository(ABC):
    """Abstract interface for disc data access."""
    
    @abstractmethod
    def get_all(self) -> List[Disc]:
        """Get all available music discs."""
        pass
    
    @abstractmethod
    def get_by_id(self, disc_id: str) -> Optional[Disc]:
        """Get a disc by its ID."""
        pass
    
    @abstractmethod
    def add_disc(self, disc_data: dict) -> Disc:
        """Add a new disc."""
        pass
    
    @abstractmethod
    def delete_disc(self, disc_id: str) -> bool:
        """Delete a disc by ID. Returns True if deleted."""
        pass


class ICollectionRepository(ABC):
    """Abstract interface for user collection persistence."""
    
    @abstractmethod
    def load(self) -> Collection:
        """Load the user's collection from storage."""
        pass
    
    @abstractmethod
    def save(self, collection: Collection) -> None:
        """Save the user's collection to storage."""
        pass

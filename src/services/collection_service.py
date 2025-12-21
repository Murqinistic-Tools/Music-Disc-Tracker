from dataclasses import dataclass
from typing import List, Tuple

from src.models.disc import Disc
from src.models.collection import Collection
from src.repositories.interfaces import IDiscRepository, ICollectionRepository


@dataclass
class DiscWithStatus:
    """A disc combined with its ownership status."""
    disc: Disc
    owned: bool


class CollectionService:
    """Business logic for managing the music disc collection."""
    
    def __init__(
        self, 
        disc_repo: IDiscRepository, 
        collection_repo: ICollectionRepository
    ):
        self._disc_repo = disc_repo
        self._collection_repo = collection_repo
        self._collection = self._collection_repo.load()
    
    def get_all_discs_with_status(self) -> List[DiscWithStatus]:
        """Get all discs with their ownership status."""
        discs = self._disc_repo.get_all()
        return [
            DiscWithStatus(
                disc=disc,
                owned=self._collection.is_owned(disc.id)
            )
            for disc in discs
        ]
    
    def toggle_disc(self, disc_id: str) -> bool:
        """Toggle ownership of a disc. Returns new status."""
        new_status = self._collection.toggle_disc(disc_id)
        self._collection_repo.save(self._collection)
        return new_status
    
    def get_progress(self) -> Tuple[int, int]:
        """Get progress as (owned_count, total_count)."""
        total = len(self._disc_repo.get_all())
        owned = self._collection.get_owned_count()
        return (owned, total)
    
    def get_disc_by_id(self, disc_id: str) -> Disc | None:
        """Get a disc by its ID."""
        return self._disc_repo.get_by_id(disc_id)
    
    def add_disc(self, disc_data: dict) -> Disc:
        """Add a new disc to the collection."""
        return self._disc_repo.add_disc(disc_data)
    
    def delete_disc(self, disc_id: str) -> bool:
        """Delete a disc from the collection."""
        return self._disc_repo.delete_disc(disc_id)

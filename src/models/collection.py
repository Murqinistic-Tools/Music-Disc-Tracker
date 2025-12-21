from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CollectionEntry:
    """Represents a user's ownership record of a disc."""
    disc_id: str
    owned: bool = False
    
    def toggle_ownership(self) -> None:
        """Toggle the ownership status of this disc."""
        self.owned = not self.owned


@dataclass
class Collection:
    """Represents a user's complete music disc collection."""
    entries: Dict[str, CollectionEntry] = field(default_factory=dict)
    
    def get_entry(self, disc_id: str) -> CollectionEntry:
        """Get or create a collection entry for a disc."""
        if disc_id not in self.entries:
            self.entries[disc_id] = CollectionEntry(disc_id=disc_id)
        return self.entries[disc_id]
    
    def toggle_disc(self, disc_id: str) -> bool:
        """Toggle ownership of a disc. Returns new ownership status."""
        entry = self.get_entry(disc_id)
        entry.toggle_ownership()
        return entry.owned
    
    def is_owned(self, disc_id: str) -> bool:
        """Check if a disc is owned."""
        return self.entries.get(disc_id, CollectionEntry(disc_id=disc_id)).owned
    
    def get_owned_count(self) -> int:
        """Get the count of owned discs."""
        return sum(1 for entry in self.entries.values() if entry.owned)
    
    def to_dict(self) -> dict:
        """Convert collection to dictionary for JSON serialization."""
        return {
            "entries": {
                disc_id: {
                    "disc_id": entry.disc_id,
                    "owned": entry.owned
                }
                for disc_id, entry in self.entries.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Collection":
        """Create a Collection from a dictionary."""
        collection = cls()
        for disc_id, entry_data in data.get("entries", {}).items():
            collection.entries[disc_id] = CollectionEntry(
                disc_id=entry_data.get("disc_id", disc_id),
                owned=entry_data.get("owned", False)
            )
        return collection

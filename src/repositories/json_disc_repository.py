import json
from pathlib import Path
from typing import List, Optional

from src.models.disc import Disc
from src.repositories.interfaces import IDiscRepository


class JsonDiscRepository(IDiscRepository):
    """JSON-based implementation of disc repository."""
    
    def __init__(self, data_path: Path):
        self._data_path = data_path
        self._discs: List[Disc] = []
        self._load_discs()
    
    def _load_discs(self) -> None:
        """Load disc data from JSON file."""
        if not self._data_path.exists():
            self._discs = []
            return
        
        with open(self._data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self._discs = [
            Disc(
                id=disc["id"],
                name=disc["name"],
                artist=disc.get("artist", ""),
                description=disc.get("description", ""),
                how_to_obtain=disc.get("how_to_obtain", ""),
                protected=disc.get("protected", False),
                image_url=disc.get("image_url")
            )
            for disc in data.get("discs", [])
        ]
    
    def get_all(self) -> List[Disc]:
        """Get all available music discs."""
        return self._discs.copy()
    
    def get_by_id(self, disc_id: str) -> Optional[Disc]:
        """Get a disc by its ID."""
        for disc in self._discs:
            if disc.id == disc_id:
                return disc
        return None
    
    def add_disc(self, disc_data: dict) -> Disc:
        """Add a new disc to the repository and save to JSON."""
        new_disc = Disc(
            id=disc_data["id"],
            name=disc_data["name"],
            artist=disc_data.get("artist", ""),
            description=disc_data.get("description", ""),
            how_to_obtain=disc_data.get("how_to_obtain", ""),
            image_url=disc_data.get("image_url")
        )
        
        self._discs.append(new_disc)
        self._save_discs()
        
        return new_disc
    
    def _save_discs(self) -> None:
        """Save all discs to JSON file."""
        data = {
            "discs": [
                {
                    "id": disc.id,
                    "name": disc.name,
                    "artist": disc.artist,
                    "description": disc.description,
                    "how_to_obtain": disc.how_to_obtain,
                    "protected": disc.protected
                }
                for disc in self._discs
            ]
        }
        
        with open(self._data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def delete_disc(self, disc_id: str) -> bool:
        """Delete a disc by ID."""
        for i, disc in enumerate(self._discs):
            if disc.id == disc_id:
                self._discs.pop(i)
                self._save_discs()
                return True
        return False

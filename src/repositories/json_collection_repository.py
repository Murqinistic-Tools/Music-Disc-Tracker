import json
import threading
from pathlib import Path

from src.models.collection import Collection
from src.repositories.interfaces import ICollectionRepository


class JsonCollectionRepository(ICollectionRepository):
    """JSON-based implementation of collection repository."""
    
    def __init__(self, data_path: Path):
        self._data_path = data_path
    
    def load(self) -> Collection:
        """Load the user's collection from JSON file."""
        if not self._data_path.exists():
            return Collection()
        
        try:
            with open(self._data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Collection.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return Collection()
    
    def save(self, collection: Collection) -> None:
        """Save the user's collection to JSON file (Debounced)."""
        self._collection_cache = collection
        
        if hasattr(self, "_save_timer") and self._save_timer:
            self._save_timer.cancel()
        
        self._save_timer = threading.Timer(0.5, self._perform_save)
        self._save_timer.start()
    
    def _perform_save(self) -> None:
        """Actually write to disk."""
        if not hasattr(self, "_collection_cache"):
            return
            
        self._data_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self._data_path, "w", encoding="utf-8") as f:
                json.dump(self._collection_cache.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving collection: {e}")

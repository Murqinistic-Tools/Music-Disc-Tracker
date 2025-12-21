from pathlib import Path
from typing import Optional


from functools import lru_cache

class ImageLoader:
    """Service for loading disc images from cache."""
    
    def __init__(self, cache_dir: Path):
        self._cache_dir = cache_dir
        self._cache_dir.mkdir(parents=True, exist_ok=True)
    
    @lru_cache(maxsize=128)
    def get_image_path(self, disc_id: str, image_url: Optional[str] = None) -> Optional[Path]:
        """Get the local path for a disc image.
        
        Images should be placed in data/disc-icons/ with filename: {disc_id}.png
        """
        cache_path = self._cache_dir / f"{disc_id}.png"
        
        if cache_path.exists():
            return cache_path
        
        return None

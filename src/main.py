"""
Minecraft Music Disc Tracker
A GUI application to track your Minecraft music disc collection.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.repositories import JsonDiscRepository, JsonCollectionRepository
from src.services import CollectionService, ImageLoader
from src.gui import App


def main():
    """Entry point for the application."""
    # Paths
    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"
    disc_icons_path = data_path / "disc-icons"
    
    # Initialize repositories (Dependency Injection)
    disc_repo = JsonDiscRepository(data_path / "discs.json")
    collection_repo = JsonCollectionRepository(data_path / "collection.json")
    
    # Initialize services
    image_loader = ImageLoader(disc_icons_path)
    collection_service = CollectionService(disc_repo, collection_repo)
    
    # Create and run app
    app = App(collection_service, image_loader)
    app.mainloop()


if __name__ == "__main__":
    main()

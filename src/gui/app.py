from typing import Dict
from pathlib import Path
import customtkinter as ctk

from src.services.collection_service import CollectionService
from src.services.image_loader import ImageLoader
from src.gui.components.disc_card import DiscCard
from src.gui.components.add_disc_dialog import AddDiscDialog
from src.services.collection_service import DiscWithStatus


# Geist-like Design System Colors
GEIST_BG = "#000000"
GEIST_CARD = "#111111"
GEIST_BORDER = "#333333"
GEIST_TEXT = "#EDEDED"
GEIST_TEXT_SECONDARY = "#888888"
GEIST_ACCENT = "#FFFFFF"


class App(ctk.CTk):
    """Main application window."""
    
    def __init__(
        self,
        collection_service: CollectionService,
        image_loader: ImageLoader
    ):
        super().__init__()
        
        self._service = collection_service
        self._image_loader = image_loader
        self._disc_cards: Dict[str, DiscCard] = {}
        self._all_discs: list = []
        self._search_after_id = None
        
        self._setup_window()
        self._setup_ui()
        self._load_images()
    
    def _setup_window(self) -> None:
        """Configure the main window."""
        self.title("Music Disc Tracker")
        self.geometry("900x650")
        self.minsize(700, 500)
        
        icon_path = Path(__file__).parent.parent.parent / "data" / "app-icon" / "icon.ico"
        if icon_path.exists():
            self.iconbitmap(str(icon_path))
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=GEIST_BG)
    
    def _setup_ui(self) -> None:
        """Set up the main UI layout."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self._create_header()
        self._create_search_bar()
        self._create_progress_section()
        self._create_disc_grid()
        self._refresh_ui()
    
    def _create_header(self) -> None:
        """Create the header section."""
        header_frame = ctk.CTkFrame(
            self, 
            fg_color=GEIST_CARD, 
            corner_radius=0,
            border_width=1,
            border_color=GEIST_BORDER
        )
        header_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Music Disc Tracker",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=GEIST_TEXT
        )
        title.grid(row=0, column=0, padx=24, pady=20, sticky="w")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="Add Disc",
            width=100,
            height=32,
            corner_radius=6,
            fg_color="transparent",
            hover_color=GEIST_CARD,
            border_width=1,
            border_color=GEIST_BORDER,
            text_color=GEIST_TEXT,
            font=ctk.CTkFont(size=13),
            command=self._show_add_disc_dialog
        )
        add_btn.grid(row=0, column=1, padx=24, pady=20, sticky="e")
    
    def _create_search_bar(self) -> None:
        """Create the search bar."""
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, padx=24, pady=(16, 8), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search discs...",
            height=36,
            fg_color=GEIST_CARD,
            border_color=GEIST_BORDER,
            text_color=GEIST_TEXT,
            placeholder_text_color=GEIST_TEXT_SECONDARY,
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._on_search_keyrelease)
    
    def _create_progress_section(self) -> None:
        """Create the progress bar section."""
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.grid(row=2, column=0, padx=24, pady=8, sticky="ew")
        progress_frame.grid_columnconfigure(1, weight=1)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="0/0",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=GEIST_TEXT
        )
        self.progress_label.grid(row=0, column=0, padx=(0, 16))
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=4,
            corner_radius=2,
            progress_color=GEIST_ACCENT,
            fg_color=GEIST_BORDER
        )
        self.progress_bar.grid(row=0, column=1, sticky="ew")
        self.progress_bar.set(0)
        
        self.percentage_label = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=ctk.CTkFont(size=13),
            text_color=GEIST_TEXT_SECONDARY
        )
        self.percentage_label.grid(row=0, column=2, padx=(16, 0))
    
    def _create_disc_grid(self) -> None:
        """Create the scrollable disc grid."""
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=GEIST_BORDER,
            scrollbar_button_hover_color=GEIST_TEXT_SECONDARY
        )
        self.scroll_frame.grid(row=3, column=0, padx=24, pady=(0, 24), sticky="nsew")
        
        for i in range(5):
            self.scroll_frame.grid_columnconfigure(i, weight=1, uniform="disc")
        
        self._all_discs = self._service.get_all_discs_with_status()
        
        # Create all cards once
        for disc_status in self._all_discs:
            image_path = self._image_loader.get_image_path(
                disc_status.disc.id,
                disc_status.disc.image_url
            )
            
            card = DiscCard(
                self.scroll_frame,
                disc_status,
                image_path,
                on_toggle=self._on_disc_toggle,
                on_delete=self._on_disc_delete
            )
            self._disc_cards[disc_status.disc.id] = card
        
        # Initial layout
        self._layout_visible_cards()
    
    def _layout_visible_cards(self, filter_query: str = "") -> None:
        """Layout only visible cards based on filter."""
        query = filter_query.lower().strip()
        
        # Determine which discs match
        visible_discs = []
        for disc_status in self._all_discs:
            matches = not query or query in disc_status.disc.name.lower()
            card = self._disc_cards[disc_status.disc.id]
            
            if matches:
                visible_discs.append(disc_status.disc.id)
            else:
                card.grid_forget()
        
        # Layout visible cards
        for i, disc_id in enumerate(visible_discs):
            row = i // 5
            col = i % 5
            self._disc_cards[disc_id].grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
    
    def _on_search_keyrelease(self, event=None) -> None:
        """Handle search with debouncing."""
        # Cancel previous search
        if self._search_after_id:
            self.after_cancel(self._search_after_id)
        
        # Debounce: wait 150ms after typing stops
        self._search_after_id = self.after(150, self._do_search)
    
    def _do_search(self) -> None:
        """Execute search."""
        query = self.search_entry.get()
        self._layout_visible_cards(query)
    
    def _on_disc_toggle(self, disc_id: str) -> None:
        """Handle disc toggle event."""
        new_status = self._service.toggle_disc(disc_id)
        
        for disc_status in self._all_discs:
            if disc_status.disc.id == disc_id:
                disc_status.owned = new_status
                break
        
        if disc_id in self._disc_cards:
            self._disc_cards[disc_id].update_status(new_status)
        
        self._refresh_ui()
    
    def _on_disc_delete(self, disc_id: str) -> None:
        """Handle disc delete event."""
        # Delete from service
        if self._service.delete_disc(disc_id):
            # Remove from local list
            self._all_discs = [d for d in self._all_discs if d.disc.id != disc_id]
            
            # Destroy and remove card
            if disc_id in self._disc_cards:
                self._disc_cards[disc_id].destroy()
                del self._disc_cards[disc_id]
            
            # Re-layout
            self._do_search()
            self._refresh_ui()
    
    def _refresh_ui(self) -> None:
        """Refresh progress."""
        owned, total = self._service.get_progress()
        
        progress = owned / total if total > 0 else 0
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"{owned}/{total}")
        self.percentage_label.configure(text=f"{int(progress * 100)}%")
    
    def _load_images(self) -> None:
        """Preload images in background."""
        pass
    
    def _show_add_disc_dialog(self) -> None:
        """Show the add disc dialog."""
        AddDiscDialog(self, on_save=self._on_add_disc)
    
    def _on_add_disc(self, disc_data: dict) -> None:
        """Handle adding a new disc."""
        new_disc = self._service.add_disc(disc_data)
        
        disc_with_status = DiscWithStatus(disc=new_disc, owned=False)
        self._all_discs.append(disc_with_status)
        
        # Create card for new disc
        image_path = self._image_loader.get_image_path(new_disc.id, new_disc.image_url)
        card = DiscCard(
            self.scroll_frame,
            disc_with_status,
            image_path,
            on_toggle=self._on_disc_toggle,
            on_delete=self._on_disc_delete
        )
        self._disc_cards[new_disc.id] = card
        
        # Re-layout
        self._do_search()
        self._refresh_ui()

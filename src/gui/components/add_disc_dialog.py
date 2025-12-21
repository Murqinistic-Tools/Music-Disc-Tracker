from typing import Callable
from pathlib import Path
import customtkinter as ctk


# Geist-like Design System
GEIST_BG = "#000000"
GEIST_CARD = "#111111"
GEIST_BORDER = "#333333"
GEIST_TEXT = "#EDEDED"
GEIST_TEXT_SECONDARY = "#888888"
GEIST_ERROR = "#FF0000"


class AddDiscDialog(ctk.CTkToplevel):
    """Dialog for adding a new music disc."""
    
    def __init__(self, parent, on_save: Callable[[dict], None]):
        super().__init__(parent)
        
        self._on_save = on_save
        
        self.title("Add Disc")
        self.geometry("400x380")
        self.resizable(False, False)
        self.configure(fg_color=GEIST_BG)
        
        # Set custom icon
        icon_path = Path(__file__).parent.parent.parent.parent / "data" / "app-icon" / "icon.ico"
        if icon_path.exists():
            self.after(200, lambda: self.iconbitmap(str(icon_path)))
        
        self.transient(parent)
        self.grab_set()
        
        self._setup_ui()
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def _setup_ui(self) -> None:
        """Set up the dialog UI."""
        self.grid_columnconfigure(0, weight=1)
        
        # Form frame
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.grid(row=0, column=0, padx=24, pady=24, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)
        
        # ID
        ctk.CTkLabel(form_frame, text="ID", text_color=GEIST_TEXT_SECONDARY, 
                     font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=(0, 16), pady=6, sticky="e")
        self.id_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="disc_id",
            fg_color=GEIST_CARD,
            border_color=GEIST_BORDER,
            text_color=GEIST_TEXT
        )
        self.id_entry.grid(row=0, column=1, pady=6, sticky="ew")
        
        # Name
        ctk.CTkLabel(form_frame, text="Name", text_color=GEIST_TEXT_SECONDARY,
                     font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=(0, 16), pady=6, sticky="e")
        self.name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Disc Name",
            fg_color=GEIST_CARD,
            border_color=GEIST_BORDER,
            text_color=GEIST_TEXT
        )
        self.name_entry.grid(row=1, column=1, pady=6, sticky="ew")
        
        # Artist
        ctk.CTkLabel(form_frame, text="Artist", text_color=GEIST_TEXT_SECONDARY,
                     font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=(0, 16), pady=6, sticky="e")
        self.artist_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Artist name",
            fg_color=GEIST_CARD,
            border_color=GEIST_BORDER,
            text_color=GEIST_TEXT
        )
        self.artist_entry.grid(row=2, column=1, pady=6, sticky="ew")
        
        # Description
        ctk.CTkLabel(form_frame, text="Description", text_color=GEIST_TEXT_SECONDARY,
                     font=ctk.CTkFont(size=12)).grid(row=3, column=0, padx=(0, 16), pady=6, sticky="ne")
        self.desc_entry = ctk.CTkTextbox(
            form_frame,
            height=60,
            fg_color=GEIST_CARD,
            border_color=GEIST_BORDER,
            border_width=1,
            text_color=GEIST_TEXT
        )
        self.desc_entry.grid(row=3, column=1, pady=6, sticky="ew")
        
        # How to obtain
        ctk.CTkLabel(form_frame, text="Obtain Method", text_color=GEIST_TEXT_SECONDARY,
                     font=ctk.CTkFont(size=12)).grid(row=4, column=0, padx=(0, 16), pady=6, sticky="e")
        self.obtain_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="e.g. Dungeon Chests",
            fg_color=GEIST_CARD,
            border_color=GEIST_BORDER,
            text_color=GEIST_TEXT
        )
        self.obtain_entry.grid(row=4, column=1, pady=6, sticky="ew")
        
        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=24, pady=(0, 24))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=80,
            height=32,
            corner_radius=6,
            fg_color="transparent",
            hover_color=GEIST_CARD,
            border_width=1,
            border_color=GEIST_BORDER,
            text_color=GEIST_TEXT,
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=8)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            width=80,
            height=32,
            corner_radius=6,
            fg_color=GEIST_TEXT,
            hover_color="#CCCCCC",
            text_color=GEIST_BG,
            command=self._save
        )
        save_btn.pack(side="left", padx=8)
    
    def _save(self) -> None:
        """Save the new disc."""
        disc_id = self.id_entry.get().strip().lower().replace(" ", "_")
        name = self.name_entry.get().strip()
        artist = self.artist_entry.get().strip()
        description = self.desc_entry.get("1.0", "end-1c").strip()
        how_to_obtain = self.obtain_entry.get().strip()
        
        if not disc_id or not name:
            self._show_error("ID and Name are required")
            return
        
        disc_data = {
            "id": disc_id,
            "name": name,
            "artist": artist or "Unknown",
            "description": description,
            "how_to_obtain": how_to_obtain
        }
        
        self._on_save(disc_data)
        self.destroy()
    
    def _show_error(self, message: str) -> None:
        """Show an error message."""
        error_label = ctk.CTkLabel(
            self,
            text=message,
            text_color=GEIST_ERROR,
            font=ctk.CTkFont(size=11)
        )
        error_label.grid(row=2, column=0, pady=8)
        self.after(3000, error_label.destroy)

from typing import Callable, Optional
from pathlib import Path
import customtkinter as ctk
from PIL import Image

from src.services.collection_service import DiscWithStatus


# Geist-like Design System
GEIST_BG = "#000000"
GEIST_CARD = "#111111"
GEIST_CARD_HOVER = "#1A1A1A"
GEIST_BORDER = "#333333"
GEIST_BORDER_ACTIVE = "#FFFFFF"
GEIST_TEXT = "#EDEDED"
GEIST_TEXT_SECONDARY = "#888888"
GEIST_TEXT_DIM = "#666666"
GEIST_SUCCESS = "#45A557"
GEIST_DANGER = "#FF4444"


class DiscCard(ctk.CTkFrame):
    """A card component representing a single music disc."""
    
    def __init__(
        self, 
        parent,
        disc_with_status: DiscWithStatus,
        image_path: Optional[Path],
        on_toggle: Callable[[str], None],
        on_delete: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        self.disc = disc_with_status.disc
        self.owned = disc_with_status.owned
        self._on_toggle = on_toggle
        self._on_delete = on_delete
        self._is_deletable = not self.disc.protected
        self._tooltip_window = None
        self._tooltip_after_id = None
        self._is_hovering = False
        
        border_color = GEIST_BORDER_ACTIVE if self.owned else GEIST_BORDER
        
        super().__init__(
            parent, 
            fg_color=GEIST_CARD,
            corner_radius=8,
            border_width=1,
            border_color=border_color,
            **kwargs
        )
        
        self.configure(cursor="hand2")
        self._setup_ui(image_path)
        self._bind_events()
    
    def _bind_events(self) -> None:
        """Bind events to card and all children."""
        widgets = [self, self.checkbox_label, self.image_label, self.name_label]
        if hasattr(self, 'delete_btn'):
            widgets.append(self.delete_btn)
        for w in widgets:
            w.bind("<Enter>", self._on_card_enter, add="+")
            w.bind("<Leave>", self._on_card_leave, add="+")
            w.bind("<Button-1>", self._handle_click, add="+")
    
    def _setup_ui(self, image_path: Optional[Path]) -> None:
        """Set up the card UI."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Delete button (top-left) - only for custom discs
        if self._is_deletable and self._on_delete:
            self.delete_btn = ctk.CTkButton(
                self,
                text="×",
                width=18,
                height=18,
                corner_radius=4,
                fg_color="transparent",
                hover_color="#331111",
                text_color=GEIST_DANGER,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=self._confirm_delete
            )
            self.delete_btn.grid(row=0, column=0, padx=4, pady=(6, 0), sticky="w")
        
        # Checkbox indicator (top-right)
        checkbox_text = "✓" if self.owned else ""
        checkbox_color = GEIST_SUCCESS if self.owned else GEIST_TEXT_SECONDARY
        self.checkbox_label = ctk.CTkLabel(
            self,
            text=checkbox_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=checkbox_color,
            width=20
        )
        self.checkbox_label.grid(row=0, column=1, padx=8, pady=(8, 0), sticky="e")
        
        # Disc image
        if image_path and image_path.exists():
            try:
                pil_image = Image.open(image_path)
                self.disc_image = ctk.CTkImage(pil_image, size=(36, 36))
                self.image_label = ctk.CTkLabel(self, image=self.disc_image, text="")
                self.image_label.grid(row=1, column=0, columnspan=2, padx=8, pady=(4, 4))
            except Exception:
                self._show_placeholder()
        else:
            self._show_placeholder()
        
        # Disc name
        self.name_label = ctk.CTkLabel(
            self,
            text=self.disc.name,
            font=ctk.CTkFont(size=11),
            text_color=GEIST_TEXT
        )
        self.name_label.grid(row=2, column=0, columnspan=2, padx=8, pady=(0, 10))
    
    def _confirm_delete(self) -> None:
        """Show delete confirmation dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Delete Disc")
        dialog.geometry("280x120")
        dialog.resizable(False, False)
        dialog.configure(fg_color=GEIST_BG)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        # Center on parent
        dialog.update_idletasks()
        parent = self.winfo_toplevel()
        x = parent.winfo_x() + (parent.winfo_width() - dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Message
        ctk.CTkLabel(
            dialog,
            text=f"Delete '{self.disc.name}'?",
            font=ctk.CTkFont(size=14),
            text_color=GEIST_TEXT
        ).pack(pady=(20, 15))
        
        # Buttons
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack()
        
        ctk.CTkButton(
            btn_frame, text="Cancel", width=80, height=30,
            fg_color="transparent", hover_color=GEIST_CARD,
            border_width=1, border_color=GEIST_BORDER,
            text_color=GEIST_TEXT,
            command=dialog.destroy
        ).pack(side="left", padx=8)
        
        def do_delete():
            dialog.destroy()
            self._on_delete(self.disc.id)
        
        ctk.CTkButton(
            btn_frame, text="Delete", width=80, height=30,
            fg_color=GEIST_DANGER, hover_color="#CC3333",
            text_color="#FFFFFF",
            command=do_delete
        ).pack(side="left", padx=8)
    
    def _show_placeholder(self) -> None:
        """Show a placeholder when no image is available."""
        self.image_label = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=28),
            text_color=GEIST_TEXT_SECONDARY
        )
        self.image_label.grid(row=1, column=0, columnspan=2, padx=8, pady=(4, 4))
    
    def _on_card_enter(self, event=None) -> None:
        """Mouse entered card area."""
        if not self._is_hovering:
            self._is_hovering = True
            self.configure(fg_color=GEIST_CARD_HOVER)
            self._schedule_tooltip()
    
    def _on_card_leave(self, event=None) -> None:
        """Mouse left - check if truly left the card."""
        self.after(10, self._check_still_hovering)
    
    def _check_still_hovering(self) -> None:
        """Check if mouse is still over this card or its children."""
        try:
            x = self.winfo_pointerx() - self.winfo_rootx()
            y = self.winfo_pointery() - self.winfo_rooty()
            
            if 0 <= x <= self.winfo_width() and 0 <= y <= self.winfo_height():
                return
            
            self._is_hovering = False
            self.configure(fg_color=GEIST_CARD)
            self._hide_tooltip()
        except:
            pass
    
    def _schedule_tooltip(self) -> None:
        """Schedule tooltip to show after delay."""
        self._cancel_tooltip()
        self._tooltip_after_id = self.after(400, self._show_tooltip)
    
    def _cancel_tooltip(self) -> None:
        """Cancel scheduled tooltip."""
        if self._tooltip_after_id:
            self.after_cancel(self._tooltip_after_id)
            self._tooltip_after_id = None
    
    def _show_tooltip(self) -> None:
        """Show the tooltip."""
        if self._tooltip_window or not self._is_hovering:
            return
        
        x = self.winfo_rootx() + self.winfo_width() + 5
        y = self.winfo_rooty()
        
        self._tooltip_window = tw = ctk.CTkToplevel(self)
        tw.wm_overrideredirect(True)
        tw.configure(fg_color=GEIST_CARD)
        
        frame = ctk.CTkFrame(tw, fg_color=GEIST_CARD, corner_radius=8,
                            border_width=1, border_color=GEIST_BORDER)
        frame.pack(padx=1, pady=1)
        
        ctk.CTkLabel(
            frame, text=self.disc.name,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=GEIST_TEXT
        ).pack(anchor="w", padx=12, pady=(10, 2))
        
        ctk.CTkLabel(
            frame, text=f"by {self.disc.artist}",
            font=ctk.CTkFont(size=11),
            text_color=GEIST_TEXT_SECONDARY
        ).pack(anchor="w", padx=12, pady=(0, 6))
        
        if self.disc.description:
            ctk.CTkLabel(
                frame, text=self.disc.description,
                font=ctk.CTkFont(size=11),
                text_color=GEIST_TEXT_DIM,
                wraplength=180,
                justify="left"
            ).pack(anchor="w", padx=12, pady=(0, 6))
        
        if self.disc.how_to_obtain:
            ctk.CTkLabel(
                frame, text=f"📍 {self.disc.how_to_obtain}",
                font=ctk.CTkFont(size=10),
                text_color=GEIST_TEXT_DIM,
                wraplength=180,
                justify="left"
            ).pack(anchor="w", padx=12, pady=(0, 10))
        
        tw.wm_geometry(f"+{x}+{y}")
    
    def _hide_tooltip(self) -> None:
        """Hide the tooltip."""
        self._cancel_tooltip()
        if self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None
    
    def _handle_click(self, event=None) -> None:
        """Handle card click."""
        if hasattr(self, 'delete_btn'):
            try:
                widget = event.widget
                if widget == self.delete_btn or widget.master == self.delete_btn:
                    return
            except:
                pass
        self._on_toggle(self.disc.id)
    
    def update_status(self, owned: bool) -> None:
        """Update the ownership status display."""
        self.owned = owned
        border_color = GEIST_BORDER_ACTIVE if owned else GEIST_BORDER
        checkbox_text = "✓" if owned else ""
        checkbox_color = GEIST_SUCCESS if owned else GEIST_TEXT_SECONDARY
        
        self.configure(border_color=border_color)
        self.checkbox_label.configure(text=checkbox_text, text_color=checkbox_color)

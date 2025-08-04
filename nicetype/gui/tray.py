"""System tray integration for NiceType."""

import tkinter as tk
import threading
from tkinter import messagebox
import sys
import os

# Try to import pystray for system tray, fallback to menu if not available
try:
    import pystray
    from pystray import MenuItem as Item
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

from ..core.processor import input_processor
from ..config.manager import config
from .settings import SettingsWindow


class SystemTray:
    """System tray integration for NiceType."""
    
    def __init__(self):
        """Initialize system tray."""
        self.icon = None
        self.settings_window = None
        self.running = False
        
        if not TRAY_AVAILABLE:
            print("System tray not available. Please install: pip install pystray pillow")
    
    def create_icon_image(self, enabled=True):
        """Create the system tray icon image."""
        if not TRAY_AVAILABLE:
            return None
            
        # Create a simple icon
        width = 64
        height = 64
        color = (0, 120, 215) if enabled else (128, 128, 128)  # Blue if enabled, gray if disabled
        
        image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a simple "N" for NiceType
        draw.rectangle((10, 10, 15, 54), fill=color)  # Left vertical line
        draw.rectangle((49, 10, 54, 54), fill=color)  # Right vertical line
        draw.polygon([(15, 10), (49, 45), (49, 35), (25, 10)], fill=color)  # Diagonal line
        
        return image
    
    def create_menu(self):
        """Create the system tray menu."""
        if not TRAY_AVAILABLE:
            return None
            
        return (
            Item("Settings", self.show_settings, default=True),
            Item("Enable/Disable", self.toggle_enabled, checked=lambda item: config.is_enabled()),
            pystray.Menu.SEPARATOR,
            Item("Punctuation Conversion", self.toggle_punctuation, 
                 checked=lambda item: config.is_punctuation_conversion_enabled()),
            Item("Auto-Completion", self.toggle_auto_complete, 
                 checked=lambda item: config.is_auto_complete_enabled()),
            pystray.Menu.SEPARATOR,
            Item("Exit", self.quit_application)
        )
    
    def show_settings(self, icon=None, item=None):
        """Show the settings window."""
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
            # Run in a separate thread to avoid blocking
            threading.Thread(target=self._run_settings_window, daemon=True).start()
        else:
            # Bring window to front
            try:
                self.settings_window.window.lift()
                self.settings_window.window.focus_force()
            except tk.TclError:
                # Window was destroyed, create new one
                self.settings_window = SettingsWindow()
                threading.Thread(target=self._run_settings_window, daemon=True).start()
    
    def _run_settings_window(self):
        """Run the settings window in a thread."""
        try:
            self.settings_window.run()
        except Exception as e:
            print(f"Error in settings window: {e}")
        finally:
            self.settings_window = None
    
    def toggle_enabled(self, icon=None, item=None):
        """Toggle NiceType enabled state."""
        current_state = config.is_enabled()
        config.set_enabled(not current_state)
        config.save()
        
        if current_state:
            input_processor.stop()
        else:
            input_processor.start()
        
        # Update icon
        if self.icon:
            self.icon.icon = self.create_icon_image(not current_state)
    
    def toggle_punctuation(self, icon=None, item=None):
        """Toggle punctuation conversion."""
        current_state = config.is_punctuation_conversion_enabled()
        config.set_punctuation_conversion_enabled(not current_state)
        config.save()
    
    def toggle_auto_complete(self, icon=None, item=None):
        """Toggle auto-completion."""
        current_state = config.is_auto_complete_enabled()
        config.set_auto_complete_enabled(not current_state)
        config.save()
    
    def quit_application(self, icon=None, item=None):
        """Quit the application."""
        self.running = False
        input_processor.stop()
        
        if self.settings_window:
            try:
                self.settings_window.destroy()
            except:
                pass
        
        if self.icon:
            self.icon.stop()
        
        sys.exit(0)
    
    def run(self):
        """Run the system tray."""
        if not TRAY_AVAILABLE:
            # Fallback: run settings window directly
            print("Running NiceType in window mode (system tray not available)")
            self.show_settings()
            return
        
        self.running = True
        
        # Start input processor
        if config.is_enabled():
            input_processor.start()
        
        # Create and run system tray icon
        self.icon = pystray.Icon(
            "NiceType",
            self.create_icon_image(config.is_enabled()),
            "NiceType - Chinese Input Enhancement",
            self.create_menu()
        )
        
        try:
            self.icon.run()
        except KeyboardInterrupt:
            self.quit_application()


class MenuFallback:
    """Fallback menu system when system tray is not available."""
    
    def __init__(self):
        """Initialize fallback menu."""
        self.root = tk.Tk()
        self.root.title("NiceType")
        self.root.geometry("300x200")
        self.settings_window = None
        
        self._create_menu()
        
        # Start input processor if enabled
        if config.is_enabled():
            input_processor.start()
    
    def _create_menu(self):
        """Create the fallback menu."""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="NiceType", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        tk.Button(main_frame, text="Settings", command=self.show_settings, width=20).pack(pady=5)
        tk.Button(main_frame, text="Toggle Enable/Disable", command=self.toggle_enabled, width=20).pack(pady=5)
        tk.Button(main_frame, text="Exit", command=self.quit_application, width=20).pack(pady=5)
        
        # Status
        self.status_label = tk.Label(main_frame, text="", font=("Arial", 10))
        self.status_label.pack(pady=(20, 0))
        self._update_status()
    
    def _update_status(self):
        """Update status display."""
        status = "Enabled" if config.is_enabled() else "Disabled"
        self.status_label.config(text=f"Status: {status}")
    
    def show_settings(self):
        """Show settings window."""
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
            # Run in separate thread
            threading.Thread(target=self._run_settings, daemon=True).start()
    
    def _run_settings(self):
        """Run settings window."""
        try:
            self.settings_window.run()
        except Exception as e:
            print(f"Error in settings: {e}")
        finally:
            self.settings_window = None
    
    def toggle_enabled(self):
        """Toggle enabled state."""
        current_state = config.is_enabled()
        config.set_enabled(not current_state)
        config.save()
        
        if current_state:
            input_processor.stop()
        else:
            input_processor.start()
        
        self._update_status()
    
    def quit_application(self):
        """Quit application."""
        input_processor.stop()
        if self.settings_window:
            try:
                self.settings_window.destroy()
            except:
                pass
        self.root.quit()
        sys.exit(0)
    
    def run(self):
        """Run the fallback menu."""
        self.root.mainloop()


# Create global tray instance
if TRAY_AVAILABLE:
    tray = SystemTray()
else:
    tray = MenuFallback()
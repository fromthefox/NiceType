"""Input processor for NiceType."""

import time
from typing import Optional, Callable
from pynput import keyboard
from pynput.keyboard import Key, Listener, Controller
from ..config.manager import config


class InputProcessor:
    """Processes keyboard input for punctuation conversion and auto-completion."""
    
    def __init__(self):
        """Initialize the input processor."""
        self.last_char = ""
        self.last_char_time = 0
        self.char_timeout = 1.0  # 1 second timeout for consecutive characters
        self.listener: Optional[Listener] = None
        self.on_text_change: Optional[Callable[[str], None]] = None
        
    def start(self):
        """Start listening for keyboard input."""
        if self.listener is not None:
            return
            
        self.listener = Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.listener.start()
    
    def stop(self):
        """Stop listening for keyboard input."""
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
    
    def set_text_change_callback(self, callback: Callable[[str], None]):
        """Set callback for text changes."""
        self.on_text_change = callback
    
    def _on_key_press(self, key):
        """Handle key press events."""
        if not config.is_enabled():
            return
            
        # Convert key to character if possible
        char = self._key_to_char(key)
        if char is None:
            return
            
        current_time = time.time()
        
        # Check for punctuation conversion
        if config.is_punctuation_conversion_enabled():
            converted_text = self._check_punctuation_conversion(char, current_time)
            if converted_text:
                self._replace_text(converted_text)
                return
        
        # Check for auto-completion
        if config.is_auto_complete_enabled():
            completion = self._check_auto_completion(char)
            if completion:
                self._insert_text(completion)
        
        # Update last character and time
        self.last_char = char
        self.last_char_time = current_time
    
    def _on_key_release(self, key):
        """Handle key release events."""
        pass
    
    def _key_to_char(self, key) -> Optional[str]:
        """Convert key object to character string."""
        try:
            # Handle regular characters
            if hasattr(key, 'char') and key.char is not None:
                return key.char
            # Handle special keys if needed
            return None
        except AttributeError:
            return None
    
    def _check_punctuation_conversion(self, char: str, current_time: float) -> Optional[str]:
        """Check if current character should trigger punctuation conversion."""
        # Check if we have a previous character within timeout
        if (current_time - self.last_char_time) > self.char_timeout:
            return None
            
        # Check if current char matches last char for conversion
        double_char = self.last_char + char
        punctuation_mapping = config.get_punctuation_mapping()
        
        if double_char in punctuation_mapping:
            return punctuation_mapping[double_char]
            
        return None
    
    def _check_auto_completion(self, char: str) -> Optional[str]:
        """Check if current character should trigger auto-completion."""
        auto_complete_pairs = config.get_auto_complete_pairs()
        
        if char in auto_complete_pairs:
            return auto_complete_pairs[char]
            
        return None
    
    def _replace_text(self, replacement: str):
        """Replace the last two characters with the replacement text."""
        try:
            # Send backspace twice to remove the two characters
            controller = Controller()
            controller.press(Key.backspace)
            controller.release(Key.backspace)
            controller.press(Key.backspace)
            controller.release(Key.backspace)
            
            # Type the replacement character
            controller.type(replacement)
            
            if self.on_text_change:
                self.on_text_change(replacement)
                
        except Exception as e:
            print(f"Error replacing text: {e}")
    
    def _insert_text(self, text: str):
        """Insert text at current cursor position."""
        try:
            controller = Controller()
            controller.type(text)
            
            if self.on_text_change:
                self.on_text_change(text)
                
        except Exception as e:
            print(f"Error inserting text: {e}")


# Global input processor instance
input_processor = InputProcessor()
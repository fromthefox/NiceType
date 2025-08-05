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
        self._inserting_text = False  # Flag to prevent recursive processing
        self._last_completion_char = None  # Track last completion to prevent infinite loops
        
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
            
        # Skip processing if we're currently inserting text to prevent recursion
        if self._inserting_text:
            return
            
        # Convert key to character if possible
        char = self._key_to_char(key)
        if char is None:
            # Reset last char for non-character keys to avoid stale state
            self.last_char = ""
            # Also reset completion state for navigation keys
            self._last_completion_char = None
            return
            
        current_time = time.time()
        
        # Check for punctuation conversion first (higher priority)
        if config.is_punctuation_conversion_enabled():
            converted_text = self._check_punctuation_conversion(char, current_time)
            if converted_text:
                self._replace_text(converted_text)
                # Reset last char after conversion to prevent further processing
                self.last_char = ""
                self.last_char_time = current_time
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
        
        # Try exact match first
        if double_char in punctuation_mapping:
            return punctuation_mapping[double_char]
        
        # Also try case-insensitive matching if configured
        if not config.get("case_sensitive", False):
            for pattern, replacement in punctuation_mapping.items():
                if pattern.lower() == double_char.lower():
                    return replacement
                    
        return None
    
    def _check_auto_completion(self, char: str) -> Optional[str]:
        """Check if current character should trigger auto-completion."""
        auto_complete_pairs = config.get_auto_complete_pairs()
        
        if char in auto_complete_pairs:
            completion_char = auto_complete_pairs[char]
            # Prevent infinite recursion: if the completion is the same as input, 
            # only complete if we haven't just completed the same character
            if completion_char == char:
                # For self-completing characters like quotes, avoid recursion
                # by checking if we just completed this character
                if hasattr(self, '_last_completion_char') and self._last_completion_char == char:
                    # Reset to allow future completions
                    self._last_completion_char = None
                    return None
                self._last_completion_char = char
            else:
                self._last_completion_char = None
            return completion_char
            
        return None
    
    def _replace_text(self, replacement: str):
        """Replace the last two characters with the replacement text."""
        try:
            # Set flag to prevent recursive processing
            self._inserting_text = True
            
            # Small delay to ensure proper timing
            time.sleep(0.01)
            
            # Send backspace twice to remove the two characters
            controller = Controller()
            controller.press(Key.backspace)
            controller.release(Key.backspace)
            time.sleep(0.01)  # Small delay between operations
            controller.press(Key.backspace)
            controller.release(Key.backspace)
            time.sleep(0.01)
            
            # Type the replacement character
            controller.type(replacement)
            
            if self.on_text_change:
                self.on_text_change(replacement)
                
        except Exception as e:
            print(f"Error replacing text: {e}")
        finally:
            # Always clear the flag with a small delay
            time.sleep(0.02)
            self._inserting_text = False
    
    def _insert_text(self, text: str):
        """Insert text at current cursor position."""
        try:
            # Set flag to prevent recursive processing
            self._inserting_text = True
            
            # Small delay to ensure proper timing
            time.sleep(0.01)
            
            controller = Controller()
            
            # For better cursor positioning, especially with quotes,
            # we need to ensure the cursor ends up between the paired characters
            controller.type(text)
            
            # Move cursor back to position between brackets/quotes for better UX
            # For auto-completion pairs, position cursor in the middle
            if len(text) == 1:  # Single character completion
                time.sleep(0.01)  # Small delay before moving cursor
                # Use precise cursor movement to avoid selection issues
                # Ensure no modifier keys are held when moving cursor
                try:
                    controller.press(Key.left)
                    controller.release(Key.left)
                except:
                    # Fallback in case of key press issues
                    pass
            
            if self.on_text_change:
                self.on_text_change(text)
                
        except Exception as e:
            print(f"Error inserting text: {e}")
        finally:
            # Always clear the flag with a small delay
            time.sleep(0.02)
            self._inserting_text = False


# Global input processor instance
input_processor = InputProcessor()
"""Configuration manager for NiceType."""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages configuration settings for NiceType."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.config_dir = Path.home() / ".nicetype"
        self.config_file = self.config_dir / "config.json"
        self._config = self._load_default_config()
        self._ensure_config_dir()
        self.load()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "punctuation_mapping": {
                "，，": ",",  # Chinese comma to English comma
                "。。": ".",  # Chinese period to English period
                "；；": ";",  # Chinese semicolon to English semicolon
                "：：": ":",  # Chinese colon to English colon
                "？？": "?",  # Chinese question mark to English question mark
                "！！": "!",  # Chinese exclamation mark to English exclamation mark
                "\u201c\u201d": '"',  # Chinese double quotes to English double quotes
                "\u2018\u2019": "'",  # Chinese single quotes to English single quotes
            },
            "auto_complete_pairs": {
                "(": ")",
                "[": "]",
                "{": "}",
                '"': '"',
                "'": "'",
                "（": "）",  # Chinese parentheses
                "【": "】",  # Chinese square brackets
                "《": "》",  # Chinese angle brackets
                "\u201c": "\u201d",  # Chinese double quotes
            },
            "enabled": True,
            "punctuation_conversion_enabled": True,
            "auto_complete_enabled": True,
            "case_sensitive": False,
        }
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(exist_ok=True)
    
    def load(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self._config.update(file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self._config[key] = value
    
    def get_punctuation_mapping(self) -> Dict[str, str]:
        """Get punctuation mapping configuration."""
        return self._config.get("punctuation_mapping", {})
    
    def set_punctuation_mapping(self, mapping: Dict[str, str]):
        """Set punctuation mapping configuration."""
        self._config["punctuation_mapping"] = mapping
    
    def get_auto_complete_pairs(self) -> Dict[str, str]:
        """Get auto-complete pairs configuration."""
        return self._config.get("auto_complete_pairs", {})
    
    def set_auto_complete_pairs(self, pairs: Dict[str, str]):
        """Set auto-complete pairs configuration."""
        self._config["auto_complete_pairs"] = pairs
    
    def is_enabled(self) -> bool:
        """Check if NiceType is enabled."""
        return self._config.get("enabled", True)
    
    def set_enabled(self, enabled: bool):
        """Set enabled state."""
        self._config["enabled"] = enabled
    
    def is_punctuation_conversion_enabled(self) -> bool:
        """Check if punctuation conversion is enabled."""
        return self._config.get("punctuation_conversion_enabled", True)
    
    def set_punctuation_conversion_enabled(self, enabled: bool):
        """Set punctuation conversion enabled state."""
        self._config["punctuation_conversion_enabled"] = enabled
    
    def is_auto_complete_enabled(self) -> bool:
        """Check if auto-complete is enabled."""
        return self._config.get("auto_complete_enabled", True)
    
    def set_auto_complete_enabled(self, enabled: bool):
        """Set auto-complete enabled state."""
        self._config["auto_complete_enabled"] = enabled


# Global configuration instance
config = ConfigManager()
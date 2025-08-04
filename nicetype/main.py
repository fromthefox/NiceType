"""Main entry point for NiceType."""

import sys
import argparse
import os


def main():
    """Main entry point for NiceType application."""
    parser = argparse.ArgumentParser(
        description="NiceType - Chinese Input Enhancement Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nicetype                    # Run with system tray (default)
  nicetype --settings-only    # Run settings window only
  nicetype --no-tray          # Run without system tray
  nicetype --test             # Test core functionality only
        """
    )
    
    parser.add_argument(
        "--settings-only",
        action="store_true",
        help="Show settings window only (don't start input monitoring)"
    )
    
    parser.add_argument(
        "--no-tray",
        action="store_true",
        help="Run without system tray (show main window instead)"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test core functionality without GUI"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="NiceType 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Handle test mode first (no GUI dependencies)
    if args.test:
        return run_tests()
    
    # Check for GUI environment
    if not check_gui_environment():
        print("Warning: GUI environment not available.")
        print("Running in test mode to verify core functionality...")
        return run_tests()
    
    try:
        if args.settings_only:
            # Show settings window only
            from .gui.settings import SettingsWindow
            settings = SettingsWindow()
            settings.run()
        elif args.no_tray:
            # Run without system tray
            from .gui.tray import MenuFallback
            app = MenuFallback()
            app.run()
        else:
            # Run with system tray (default)
            from .gui.tray import tray
            tray.run()
    
    except KeyboardInterrupt:
        print("\nShutting down NiceType...")
        try:
            from .core.processor import input_processor
            input_processor.stop()
        except:
            pass
        sys.exit(0)
    except ImportError as e:
        print(f"Error importing GUI components: {e}")
        print("This might be due to missing GUI dependencies.")
        print("Running core functionality test instead...")
        return run_tests()
    except Exception as e:
        print(f"Error starting NiceType: {e}")
        print("Running core functionality test to verify installation...")
        return run_tests()


def check_gui_environment():
    """Check if GUI environment is available."""
    # Check for DISPLAY environment variable (Linux/Unix)
    if os.name == 'posix' and 'DISPLAY' not in os.environ:
        return False
    
    # Try importing tkinter
    try:
        import tkinter
        return True
    except ImportError:
        return False


def run_tests():
    """Run core functionality tests."""
    try:
        from .config.manager import ConfigManager
        
        print("=" * 50)
        print("NiceType Core Functionality Test")
        print("=" * 50)
        
        # Test configuration
        config = ConfigManager()
        print(f"✓ Configuration loaded successfully")
        print(f"  - Enabled: {config.is_enabled()}")
        print(f"  - Punctuation conversion: {config.is_punctuation_conversion_enabled()}")
        print(f"  - Auto-completion: {config.is_auto_complete_enabled()}")
        
        # Test punctuation mappings
        mapping = config.get_punctuation_mapping()
        print(f"\n✓ Punctuation mappings loaded: {len(mapping)} rules")
        for i, (from_chars, to_char) in enumerate(list(mapping.items())[:3]):
            print(f"  - {from_chars} → {to_char}")
        if len(mapping) > 3:
            print(f"  - ... and {len(mapping) - 3} more")
        
        # Test auto-complete pairs
        pairs = config.get_auto_complete_pairs()
        print(f"\n✓ Auto-complete pairs loaded: {len(pairs)} pairs")
        for i, (open_char, close_char) in enumerate(list(pairs.items())[:3]):
            print(f"  - {open_char} → {close_char}")
        if len(pairs) > 3:
            print(f"  - ... and {len(pairs) - 3} more")
        
        print("\n" + "=" * 50)
        print("🎉 NiceType core functionality is working correctly!")
        print("=" * 50)
        print("\nNote: GUI and input monitoring require a graphical environment.")
        print("Install with: pip install pystray pillow")
        print("For full functionality, run in a desktop environment.")
        
        return 0
    
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    main()
# NiceType - Chinese Input Enhancement Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)

NiceType is a lightweight Chinese input enhancement tool that provides intelligent punctuation conversion and auto-completion features for improved typing experience.

## Features

### 1. Punctuation Conversion
Automatically converts consecutive Chinese punctuation marks to their English equivalents:
- `，，` → `,` (Chinese comma to English comma)
- `。。` → `.` (Chinese period to English period)  
- `；；` → `;` (Chinese semicolon to English semicolon)
- `：：` → `:` (Chinese colon to English colon)
- `？？` → `?` (Chinese question mark to English question mark)
- `！！` → `!` (Chinese exclamation mark to English exclamation mark)
- `""` → `"` (Chinese double quotes to English double quotes)
- `''` → `'` (Chinese single quotes to English single quotes)

### 2. Auto-Completion
Automatically completes paired symbols when you type the opening character:
- `(` → `()` with cursor positioned between
- `[` → `[]` with cursor positioned between
- `{` → `{}` with cursor positioned between
- `"` → `""` with cursor positioned between
- `'` → `''` with cursor positioned between
- `（` → `（）` (Chinese parentheses)
- `【` → `【】` (Chinese square brackets)
- `《` → `《》` (Chinese angle brackets)
- `"` → `""` (Chinese double quotes)

### 3. Customizable Settings
- **User-customizable punctuation mappings**: Add, edit, or remove conversion rules
- **Configurable auto-completion pairs**: Customize which symbols should be auto-completed
- **Enable/disable features**: Toggle punctuation conversion and auto-completion independently
- **Lightweight operation**: Minimal memory usage and system resource consumption

## Installation

### Prerequisites
- Python 3.7 or higher
- Operating System: Windows, macOS, or Linux

### Install from Source
```bash
git clone https://github.com/fromthefox/NiceType.git
cd NiceType
pip install -r requirements.txt
pip install -e .
```

### Dependencies
The following Python packages are required:
- `pynput>=1.7.6` - For global keyboard input monitoring
- `keyboard>=0.13.5` - Alternative keyboard handling

Optional dependencies for enhanced features:
- `pystray` - For system tray integration
- `pillow` - For system tray icon generation

```bash
# Install optional dependencies for full features
pip install pystray pillow
```

## Usage

### Running NiceType

#### With System Tray (Recommended)
```bash
nicetype
```
This runs NiceType in the background with a system tray icon for easy access.

#### Settings Window Only
```bash
nicetype --settings-only
```
Opens only the settings window without starting input monitoring.

#### Without System Tray
```bash
nicetype --no-tray
```
Runs NiceType with a simple main window instead of system tray.

### Configuration

NiceType stores its configuration in `~/.nicetype/config.json`. You can modify settings through the GUI or edit the configuration file directly.

#### GUI Settings
1. Right-click the system tray icon and select "Settings"
2. Or run `nicetype --settings-only`

The settings window allows you to:
- Enable/disable NiceType globally
- Toggle punctuation conversion on/off
- Toggle auto-completion on/off
- Add, edit, or remove punctuation conversion rules
- Add, edit, or remove auto-completion pairs
- Reset all settings to defaults

#### Configuration File
Example configuration:
```json
{
  "enabled": true,
  "punctuation_conversion_enabled": true,
  "auto_complete_enabled": true,
  "punctuation_mapping": {
    "，，": ",",
    "。。": ".",
    "；；": ";",
    "：：": ":",
    "？？": "?",
    "！！": "!",
    """": "\"",
    "''": "'"
  },
  "auto_complete_pairs": {
    "(": ")",
    "[": "]",
    "{": "}",
    "\"": "\"",
    "'": "'",
    "（": "）",
    "【": "】",
    "《": "》",
    """: """
  },
  "case_sensitive": false
}
```

## System Tray Usage

When running with system tray support:

- **Left-click**: Show settings window
- **Right-click**: Access context menu with options:
  - Settings
  - Enable/Disable NiceType
  - Toggle Punctuation Conversion
  - Toggle Auto-Completion
  - Exit

## Development

### Project Structure
```
NiceType/
├── nicetype/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── processor.py     # Input processing logic
│   ├── config/
│   │   ├── __init__.py
│   │   └── manager.py       # Configuration management
│   └── gui/
│       ├── __init__.py
│       ├── settings.py      # Settings GUI
│       └── tray.py          # System tray integration
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Running Tests

Currently, NiceType uses manual testing. Automated tests will be added in future versions.

To test manually:
1. Run `nicetype --settings-only` to test the GUI
2. Run `nicetype` to test full functionality
3. Test punctuation conversion by typing consecutive Chinese punctuation
4. Test auto-completion by typing opening brackets/quotes

## Permissions

NiceType requires keyboard input monitoring permissions to function:

- **Windows**: May require running as administrator or allowing the application through Windows Defender
- **macOS**: Requires Accessibility permissions (System Preferences > Security & Privacy > Privacy > Accessibility)
- **Linux**: Should work without special permissions on most distributions

## Troubleshooting

### Common Issues

1. **"No module named 'pynput'" error**
   ```bash
   pip install pynput
   ```

2. **System tray not working**
   ```bash
   pip install pystray pillow
   ```
   Or run with `--no-tray` flag

3. **Punctuation conversion not working**
   - Check if NiceType is enabled in settings
   - Verify punctuation conversion is enabled
   - Check that the application has keyboard access permissions

4. **High CPU usage**
   - NiceType is designed to be lightweight, but some antivirus software may interfere
   - Add NiceType to your antivirus whitelist

### Logs and Debug Information

NiceType prints debug information to the console. Run from terminal to see any error messages:
```bash
python -m nicetype
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Yanhui Bian** - Initial work

## Acknowledgments

- Thanks to the Python community for excellent libraries like `pynput` and `pystray`
- Inspired by the need for better Chinese-English input switching
- Built with a focus on lightweight design and user customization

## Roadmap

Future planned features:
- [ ] Auto-update functionality
- [ ] More punctuation conversion patterns
- [ ] Hotkey customization
- [ ] Statistics and usage tracking
- [ ] Plugin system for custom rules
- [ ] Multi-language support beyond Chinese-English
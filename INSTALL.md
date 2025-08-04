# Installation Guide

## Quick Install

### From Source
```bash
git clone https://github.com/fromthefox/NiceType.git
cd NiceType
pip install -r requirements.txt
pip install -e .
```

### Required Dependencies
- Python 3.7+
- pynput>=1.7.6
- keyboard>=0.13.5

### Optional Dependencies (for full features)
```bash
pip install pystray pillow
```

## System Requirements

### Windows
- Windows 7 or later
- May require running as administrator for input monitoring
- Windows Defender may require allowing the application

### macOS
- macOS 10.9 or later
- Requires Accessibility permissions:
  1. Go to System Preferences > Security & Privacy > Privacy
  2. Select "Accessibility" from the left panel
  3. Click the lock to make changes
  4. Add NiceType to the list of allowed applications

### Linux
- Most modern Linux distributions
- X11 or Wayland display server
- No special permissions required on most distributions

## Verification

After installation, verify NiceType is working:
```bash
nicetype --test
```

This will test the core functionality without requiring a GUI environment.

## Troubleshooting

### "No module named 'tkinter'"
**Linux:**
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo yum install tkinter          # CentOS/RHEL
```

**macOS:**
```bash
brew install python-tk
```

### "this platform is not supported" error
This typically occurs when:
1. Running in a headless environment (no GUI)
2. Missing X11 server on Linux
3. Missing display environment variables

**Solutions:**
- Use `nicetype --test` to verify core functionality
- Install required GUI packages
- Set DISPLAY environment variable on Linux

### Permission Issues
**Windows:**
- Run as administrator
- Add to Windows Defender exceptions

**macOS:**
- Grant Accessibility permissions
- Allow in Privacy settings

**Linux:**
- Ensure user is in input group: `sudo usermod -a -G input $USER`
- May need to logout/login after group changes

### High CPU Usage
- Check antivirus software interference
- Add NiceType to antivirus whitelist
- Ensure only one instance is running
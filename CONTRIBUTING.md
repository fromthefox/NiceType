# Contributing to NiceType

Thank you for your interest in contributing to NiceType! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/NiceType.git
   cd NiceType
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Test your changes:
   ```bash
   python run_nicetype.py --test
   ```
4. Commit your changes:
   ```bash
   git commit -m "Add your meaningful commit message"
   ```
5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Create a Pull Request on GitHub

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and small
- Use type hints where possible

## Project Structure

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
└── README.md
```

## Adding Features

### New Punctuation Rules
1. Add default rules to `nicetype/config/manager.py`
2. Ensure proper Unicode handling
3. Test with various input methods

### New Auto-completion Pairs
1. Add to the default configuration in `ConfigManager._load_default_config()`
2. Consider both opening and closing characters
3. Test cursor positioning

### GUI Improvements
1. Follow tkinter best practices
2. Ensure accessibility (keyboard navigation, screen readers)
3. Test on different screen resolutions
4. Maintain consistent styling

### Input Processing
1. Be mindful of performance - this runs continuously
2. Handle edge cases gracefully
3. Avoid blocking the main thread
4. Test with different input methods and languages

## Testing

### Manual Testing
1. Test core functionality:
   ```bash
   python run_nicetype.py --test
   ```
2. Test GUI (requires graphical environment):
   ```bash
   python run_nicetype.py --settings-only
   ```
3. Test different input scenarios:
   - Various punctuation combinations
   - Different applications (text editors, browsers, etc.)
   - Different keyboard layouts

### Test Cases to Consider
- Consecutive punctuation marks
- Mixed Chinese and English input
- Fast typing scenarios
- Special characters and symbols
- Configuration changes
- System tray functionality

## Submitting Issues

When submitting issues, please include:
- Operating system and version
- Python version
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages (if any)
- Configuration files (if relevant)

## Feature Requests

Feature requests are welcome! Please:
- Explain the use case
- Describe the proposed solution
- Consider backward compatibility
- Think about configuration options

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose. Reviewers will look for:
- Code quality and style
- Functionality and testing
- Documentation updates
- Backward compatibility
- Performance impact

## License

By contributing to NiceType, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:
- Check existing issues and pull requests
- Create a new issue for discussion
- Be specific about what you want to contribute

Thank you for contributing to NiceType!
# NiceType Manual Testing Guide

This guide helps you test the fixes for all four reported issues in your Windows 11 environment.

## Prerequisites

1. Make sure you have Python 3.10 installed
2. Install NiceType dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pystray pillow  # For system tray (optional)
   ```

## Running NiceType

To start NiceType with system tray:
```bash
python -m nicetype
```

To start without system tray (if tray has issues):
```bash
python -m nicetype --no-tray
```

## Testing the Fixes

### ✅ Issue 1: Punctuation Auto-Replacement (；； → ;)

**Test Steps:**
1. Open any text editor (Notepad, Word, VS Code, etc.)
2. Type `；；` (two Chinese semicolons quickly)
3. **Expected Result:** Should automatically convert to `;` (single English semicolon)

**Other punctuation to test:**
- `，，` → `,` (Chinese comma to English comma)
- `。。` → `.` (Chinese period to English period)
- `：：` → `:` (Chinese colon to English colon)
- `？？` → `?` (Chinese question mark to English question mark)
- `！！` → `!` (Chinese exclamation mark to English exclamation mark)

### ✅ Issue 2: Chinese Parenthesis Auto-Completion (（ → ）)

**Test Steps:**
1. Type `（` (Chinese left parenthesis)
2. **Expected Result:** Should auto-complete with `）` (Chinese right parenthesis), not English `)`
3. **Final result:** `（）` with cursor positioned between the parentheses

### ✅ Issue 3: Cursor Positioning After Auto-Completion

**Test Steps:**
1. Type `【` (Chinese left square bracket)
2. **Expected Result:** Should auto-complete to `【】` with cursor positioned **between** the brackets
3. **Verify:** Try typing text - it should appear between the brackets: `【your text】`

**Other brackets to test:**
- `(` → `()` with cursor between
- `[` → `[]` with cursor between  
- `{` → `{}` with cursor between
- `"` → `""` with cursor between
- `《` → `《》` with cursor between

### ✅ Issue 4: Single Quote Infinite Loop Prevention

**Test Steps:**
1. Type `'` (single quote)
2. **Expected Result:** Should auto-complete to `''` with cursor between quotes
3. **Critical Test:** Type another `'` inside the quotes
4. **Expected Result:** Should NOT trigger infinite auto-completion
5. **Verify:** No continuous stream of `'''''''''...` characters

## Troubleshooting

### If NiceType doesn't start:
```bash
# Test core functionality without GUI
python -m nicetype --test
```

### If punctuation conversion doesn't work:
1. Check if NiceType is enabled (system tray icon or console output)
2. Verify you're typing the characters quickly (within 1 second)
3. Make sure you're using the correct Chinese punctuation characters

### If auto-completion doesn't work:
1. Check if auto-completion is enabled in settings
2. Make sure you have keyboard input permissions (Windows may ask)
3. Try in different applications to ensure it's not application-specific

### If you see permission errors:
- On Windows: Run as administrator or allow through Windows Defender
- Make sure NiceType has keyboard input access permissions

## Expected Test Results Summary

| Test Case | Input | Expected Output | Status |
|-----------|-------|----------------|--------|
| Punctuation | `；；` | `;` | ✅ Fixed |
| Chinese Parenthesis | `（` | `（）` (cursor between) | ✅ Fixed |
| Bracket Positioning | `【` | `【】` (cursor between) | ✅ Fixed |
| Quote Loop Prevention | `''''` | `''` then normal chars | ✅ Fixed |

## Settings Access

- **System Tray**: Right-click tray icon → Settings
- **No Tray Mode**: Settings window opens automatically
- **Settings Only**: `python -m nicetype --settings-only`

If you encounter any issues, please report them with:
1. Your exact steps to reproduce
2. What you expected vs. what happened
3. Your Python version and operating system
4. Any error messages from the console
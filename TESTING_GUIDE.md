# NiceType Manual Testing Guide

This guide helps you test the fixes for all issues reported in the Chinese problem statement.

## Prerequisites

1. Make sure you have Python 3.10+ installed
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

### ✅ Issue 1: Chinese Symbol Auto-Completion (（ → ）, 《 → 》)

**Problem:** Only 【】 was working correctly, other Chinese paired symbols like （）、《》 were not auto-completing properly.

**Test Steps:**
1. Open any text editor (Notepad, Word, VS Code, etc.)
2. Type `（` (Chinese left parenthesis)
3. **Expected Result:** Should auto-complete with `）` (Chinese right parenthesis)
4. **Final result:** `（）` with cursor positioned between the parentheses
5. Type `《` (Chinese left angle bracket)
6. **Expected Result:** Should auto-complete with `》` (Chinese right angle bracket)
7. **Final result:** `《》` with cursor positioned between the brackets

**Other symbols to test:**
- `【` → `【】` with cursor between (should still work)
- `(` → `()` with cursor between (English parenthesis)
- `[` → `[]` with cursor between (English bracket)

### ✅ Issue 2: Punctuation Auto-Replacement (；； → ;)

**Problem:** Punctuation replacement was not working at all.

**Test Steps:**
1. Type `；；` (two Chinese semicolons quickly, within 1 second)
2. **Expected Result:** Should automatically convert to `;` (single English semicolon)

**Other punctuation to test:**
- `，，` → `,` (Chinese comma to English comma)
- `。。` → `.` (Chinese period to English period)
- `：：` → `:` (Chinese colon to English colon)
- `？？` → `?` (Chinese question mark to English question mark)
- `！！` → `!` (Chinese exclamation mark to English exclamation mark)

### ✅ Issue 3: Cursor Positioning After Quote Auto-Completion

**Problem:** When typing `"` it auto-completed but also selected the following `"` symbol, preventing direct input.

**Test Steps:**
1. Type `"` (English double quote)
2. **Expected Result:** Should auto-complete to `""` with cursor positioned **between** the quotes
3. **Verify:** Try typing text - it should appear between the quotes: `"your text"`
4. **Critical:** Cursor should NOT select the closing quote

**Quote types to test:**
- `"` → `""` with cursor between (English double quote)
- `'` → `''` with cursor between (English single quote)  
- `"` → `""` with cursor between (Chinese double quote)

### ✅ Bonus: Quote Recursion Prevention

**Test Steps:**
1. Type `'` (single quote)
2. **Expected Result:** Should auto-complete to `''` with cursor between quotes
3. **Critical Test:** Type another `'` inside the quotes
4. **Expected Result:** Should NOT trigger infinite auto-completion
5. **Verify:** No continuous stream of `'''''''''...` characters

## Troubleshooting

### If NiceType doesn't start:
```bash
# Check if dependencies are installed
pip install -r requirements.txt
```

### If punctuation conversion doesn't work:
1. Check if NiceType is enabled (system tray icon or console output)
2. Verify you're typing the characters quickly (within 1 second)
3. Make sure you're using the correct Chinese punctuation characters
4. Check console for any error messages

### If auto-completion doesn't work:
1. Check if auto-completion is enabled in settings
2. Make sure you have keyboard input permissions (Windows may ask)
3. Try in different applications to ensure it's not application-specific

### If you see permission errors:
- On Windows: Run as administrator or allow through Windows Defender
- On macOS: Grant Accessibility permissions in System Preferences
- On Linux: Usually works without special permissions

## Expected Test Results Summary

| Test Case | Input | Expected Output | Status |
|-----------|-------|----------------|--------|
| Chinese Parenthesis | `（` | `（）` (cursor between) | ✅ Fixed |
| Chinese Angle Brackets | `《` | `《》` (cursor between) | ✅ Fixed |
| Punctuation Conversion | `；；` | `;` | ✅ Fixed |
| Quote Positioning | `"` | `""` (cursor between) | ✅ Fixed |
| Quote Loop Prevention | `''''` | `''` then normal chars | ✅ Fixed |

## Settings Access

- **System Tray**: Right-click tray icon → Settings
- **No Tray Mode**: Settings window opens automatically
- **Settings Only**: `python -m nicetype --settings-only`

## Verification Commands

To verify fixes without GUI:
```bash
cd /path/to/NiceType
python3 /tmp/comprehensive_test.py
```

If you encounter any issues, please report them with:
1. Your exact steps to reproduce
2. What you expected vs. what happened
3. Your Python version and operating system
4. Any error messages from the console
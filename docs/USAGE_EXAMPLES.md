# Usage Examples

This document provides detailed examples of using the Square Root Calculator for end users.

## Table of Contents
- [Getting Started](#getting-started)
- [Real Number Examples](#real-number-examples)
- [Complex Number Examples](#complex-number-examples)
- [Precision Control](#precision-control)
- [Custom Translations](#custom-translations)
- [Tips and Tricks](#tips-and-tricks)

## Getting Started

### First Launch

When you first run the application:
1. The interface opens in your system's default language (if supported)
2. Theme is set based on your system preferences (light/dark)
3. Settings are saved to `~/.square_root_calculator/`
4. Automatic update check runs in the background

### Basic Interface

The calculator has two main modes accessible via tabs:
- **Real Numbers**: For calculating square roots of positive real numbers
- **Complex Numbers**: For calculating square roots of complex numbers (including negative reals)

## Real Number Examples

### Example 1: Perfect Squares
**Input:** 16  
**Precision:** 10  
**Result:**
- Positive root: `+√(16) = 4`
- Negative root: `-√(16) = -4`

Perfect squares produce exact integer results.

### Example 2: Irrational Numbers
**Input:** 2  
**Precision:** 50  
**Result:**
- Positive root: `+√(2) = 1.41421356237309504880168872420969807856967187537694...`
- Scientific: `1.414213562373095e+00`
- Fraction: `1414/1000` (approximation)

The calculator displays multiple representations for better understanding.

### Example 3: Large Numbers
**Input:** 123456789  
**Precision:** 20  
**Result:** `11111.11106055555544054166...`

Even very large numbers can be computed accurately with arbitrary precision.

### Example 4: Decimal Input
**Input:** 0.25  
**Precision:** 10  
**Result:** `0.5`

Decimal inputs work seamlessly.

### Example 5: Very Small Numbers
**Input:** 0.000001  
**Precision:** 15  
**Result:** `0.001`

The calculator handles numbers of any magnitude.

## Complex Number Examples

### Example 1: Simple Complex Number
**Real Part:** 3  
**Imaginary Part:** 4  
**Precision:** 10  
**Result:**
- Positive root: `2+1i`
- Negative root: `-2-1i`

This is the classic example: √(3+4i) = 2+i

### Example 2: Pure Imaginary
**Real Part:** 0  
**Imaginary Part:** 4  
**Precision:** 10  
**Result:**
- Positive root: `1.414213562+1.414213562i`
- Negative root: `-1.414213562-1.414213562i`

Square root of pure imaginary numbers.

### Example 3: Negative Real (√-1)
**Real Part:** -1  
**Imaginary Part:** 0  
**Precision:** 10  
**Result:**
- Positive root: `0+1i`
- Negative root: `0-1i`

This demonstrates √(-1) = i, a fundamental result in complex analysis.

### Example 4: Large Complex Numbers
**Real Part:** 100  
**Imaginary Part:** 100  
**Precision:** 15  
**Result:**
- Positive root: `11.09868411346781+4.50665869232206i`

The calculator handles large complex numbers with ease.

## Precision Control

### Using the Slider
- Drag the slider to adjust precision from 1 to 200 decimal places
- Ideal for quick adjustments during exploration
- Visual feedback shows current precision value

### Using the Spinbox
- Type exact values from 1 to 1000 decimal places
- Useful when you need specific precision
- Press Enter or click Calculate to apply

### Low Precision Warning
If precision is too low for a calculation, you'll see an error message:
- **English**: "Precision too low for this calculation. Please increase precision to at least X decimal places."
- **Russian**: "Точность слишком низкая для данного вычисления. Пожалуйста, увеличьте точность минимум до X знаков после запятой."

Example triggering low precision:
- Input: 13+i with precision 1
- Solution: Increase precision to at least 3

## Custom Translations

### Adding a New Language

1. Create `translations` folder in the application directory
2. Create a JSON file named `{language_code}.json` (e.g., `de.json`)
3. Add translations with special `_language_name` field:

```json
{
  "_language_name": "Deutsch",
  "app_title": "Quadratwurzel-Rechner",
  "calculate_button": "Berechnen",
  "clear_button": "Löschen",
  "result_label": "Ergebnis"
}
```

4. Go to **Language → Reload Translations**
5. Your new language appears in the Language menu!

### Overriding Existing Translations

You can customize English or Russian by creating `en.json` or `ru.json` with only the keys you want to change.

See [translations/README.md](../translations/README.md) for complete documentation.

## Tips and Tricks

### Calculation History
- All calculations are automatically saved in the history panel
- Scroll through past calculations
- Use **Clear History** to start fresh

### Theme Selection
- Go to **Settings → Theme** to choose Light or Dark theme
- Theme preference is saved and persists across sessions
- System theme is detected automatically on first launch

### Update Management
- Automatic update checks happen on startup
- Manual check: **Help → Check for Updates**
- Click **Download** to get the latest version
- Click **Skip** to dismiss the notification (won't show again for that version)
- Skipped versions are saved in settings

### Keyboard Shortcuts
- Press Enter in input fields to calculate
- Tab between fields for efficient data entry

### Error Recovery
If you encounter an error:
1. Check input format (numbers only, no text)
2. Try increasing precision
3. For complex mode, enter real and imaginary parts separately
4. Use the history to review what worked before

## Common Use Cases

### Scientific Calculations
Set precision to 50+ for scientific work requiring high accuracy.

### Educational Purposes
Use lower precision (10-20) to demonstrate concepts without overwhelming detail.

### Quick Estimates
Use the slider at low precision (1-5) for fast approximations.

### Exploring Complex Numbers
Switch to Complex mode to visualize and understand complex square roots.

## Need More Help?

- Check the [Custom Translations Guide](../translations/README.md)
- Read the [Developer Documentation](DEVELOPMENT.md) if you want to contribute
- Open an issue on [GitHub Issues](https://github.com/ijo42/square-root-calculator/issues)

---

**[⬆ Back to top](#usage-examples)**

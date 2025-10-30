# Square Root Calculator

A comprehensive, cross-platform square root calculator with support for real numbers, complex numbers, and arbitrary precision calculations.

## Screenshots

### Initial Interface
<div align="center">
  <img src="docs/screenshots/screenshot_01_initial_english.png" alt="Initial Interface (English)" width="600"/>
  <p><i>Initial interface with English language</i></p>
</div>

### Multilingual Support
<div align="center">
  <img src="docs/screenshots/screenshot_02_russian.png" alt="Russian Interface" width="600"/>
  <p><i>Russian language interface</i></p>
</div>

### Real Number Calculations
<div align="center">
  <img src="docs/screenshots/screenshot_03_real_calculation.png" alt="Square Root of 2" width="600"/>
  <p><i>Calculating √2 with 30 decimal places precision</i></p>
</div>

<div align="center">
  <img src="docs/screenshots/screenshot_04_large_number.png" alt="Large Number Calculation" width="600"/>
  <p><i>Computing square root of large numbers (123,456,789)</i></p>
</div>

### Complex Number Support
<div align="center">
  <img src="docs/screenshots/screenshot_05_complex_mode.png" alt="Complex Mode" width="600"/>
  <p><i>Complex number mode interface</i></p>
</div>

<div align="center">
  <img src="docs/screenshots/screenshot_06_complex_calculation.png" alt="Complex Calculation" width="600"/>
  <p><i>Calculating √(3+4i) = 2+1i</i></p>
</div>

<div align="center">
  <img src="docs/screenshots/screenshot_07_negative_complex.png" alt="Square Root of -1" width="600"/>
  <p><i>Computing √(-1) = i in complex mode</i></p>
</div>

## Features

### Core Functionality
- **Real Number Support**: Calculate square roots of positive real numbers
- **Complex Number Support**: Calculate square roots of complex numbers (a + bi)
- **Arbitrary Precision**: Configure calculation precision from 1 to 1000 decimal places
- **Multiple Roots Display**: Shows both positive and negative square roots
- **Multiple Representations**: Decimal, scientific notation, and fractional approximations

### User Interface
- **Modern GUI**: Built with PyQt6 for a native look and feel
- **Tab-Based Navigation**: Intuitive switching between Real and Complex modes
- **Precision Control**: Slider (1-200) for quick adjustments + spinbox (1-1000) for exact values
- **Unified Output Format**: Consistent display across all calculation modes
- **Calculation History**: Side panel showing recent calculations with timestamps

### Additional Features
- **Multilingual Interface**: Support for English and Russian languages
- **Update Checker**: Automatic check for new versions from GitHub
- **Error Handling**: Robust input validation and error messages
- **Cross-Platform**: Works on Windows and Linux
- **Theme Support**: Light and dark themes

## Installation

Download the latest pre-built executable for your platform from the [GitHub Releases](https://github.com/ijo42/square-root-calculator/releases) page:

- **Windows**: Download `square-root-calculator.exe`
- **Linux**: Download `square-root-calculator` (ELF binary)

No Python installation required!

## Usage

### Running the Application

**Windows**: 
- Double-click `square-root-calculator.exe`

**Linux**: 
```bash
chmod +x square-root-calculator
./square-root-calculator
```

### Using the Calculator

1. **Select Calculation Mode**:
   - Use tabs to switch between **Real Numbers** and **Complex Numbers**

2. **Enter Input**:
   - **Real Mode**: Enter a single number in the input field
   - **Complex Mode**: Enter the real and imaginary parts separately

3. **Set Precision**: 
   - Use the slider (1-200) for quick adjustments
   - Use the spinbox (1-1000) for exact precision values

4. **Calculate**: Click the "Calculate" button to compute the result

5. **View Results**:
   - See both positive and negative roots
   - View multiple representations (decimal, scientific, fraction)
   - Check calculation history in the side panel

6. **Change Language**: Use Language menu → English/Русский

### Examples

#### Real Numbers
- Input: `16` → Results:
  - Positive root: `+√(16) = 4`
  - Negative root: `-√(16) = -4`
  
- Input: `2` → Results:
  - Positive root: `+√(2) = 1.4142135623730950488016887242096980785696718753769...`
  - Negative root: `-√(2) = -1.4142135623730950488016887242096980785696718753769...`
  - Scientific: `1.414213562373095e+00`
  - Fraction: `1414/1000` (approximation)

#### Complex Numbers
- Real: `3`, Imaginary: `4` → Results:
  - Positive root: `2+1i`
  - Negative root: `-2-1i`
  
- Real: `-1`, Imaginary: `0` → Results:
  - Positive root: `0+1i` (equivalent to √(-1) = i)
  - Negative root: `0-1i`

## Updating the Application

The application includes an automatic update checker that will notify you when new versions are available.

When an update is detected:
1. A notification dialog will appear with **Download** and **Skip** buttons
2. Click **Download** to open the releases page in your browser
3. Click **Skip** to dismiss the notification and continue using the current version

To manually check for updates: **Help → Check for Updates**

To update manually:
1. Visit the [GitHub Releases](https://github.com/ijo42/square-root-calculator/releases) page
2. Download the latest version for your platform
3. Replace your old executable with the new one

## Custom Translations

The application supports loading custom translations to add new languages or customize existing ones.

### Adding Custom Translations

1. Create a `translations` folder in the application directory
2. Create a JSON file named with your language code (e.g., `de.json` for German)
3. Add your translations in JSON format
4. Use **Language → Reload Translations** to load the new translations

### Example: German Translation (`translations/de.json`)

```json
{
  "app_title": "Quadratwurzel-Rechner",
  "calculate_button": "Berechnen",
  "clear_button": "Löschen",
  "result_label": "Ergebnis"
}
```

For a complete list of translation keys and detailed instructions, see [translations/README.md](translations/README.md).

### Alternative Location

Custom translations can also be placed in:
- `~/.square_root_calculator/translations/` (user-specific)

## Documentation

For more detailed information:
- [Usage Examples](docs/USAGE_EXAMPLES.md) - Detailed usage scenarios and tips
- [Custom Translations Guide](translations/README.md) - How to add or customize translations
- [Developer Documentation](docs/DEVELOPMENT.md) - For contributors and developers

## Support

For issues, feature requests, or questions:
- Open an issue on [GitHub Issues](https://github.com/ijo42/square-root-calculator/issues)
- Read the [Usage Examples](docs/USAGE_EXAMPLES.md) for common scenarios

## License

This project is open source and available under the MIT License.

## See Also

- **[Русская версия](README.ru.md)** - Russian version of this README

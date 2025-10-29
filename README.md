# Square Root Calculator

A comprehensive, cross-platform square root calculator with support for real numbers, complex numbers, and arbitrary precision calculations.

## Features

- **Real Number Support**: Calculate square roots of positive real numbers
- **Complex Number Support**: Calculate square roots of complex numbers (a + bi)
- **Arbitrary Precision**: Configure calculation precision from 1 to 1000 decimal places
- **Multilingual Interface**: Support for English and Russian languages
- **Error Handling**: Robust input validation and error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Modern GUI**: Built with PyQt6 for a native look and feel

## Requirements

- Python 3.12 or higher
- PyQt6
- uv (for package management)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ijo42/square-root-calculator.git
cd square-root-calculator
```

2. Install dependencies using uv:
```bash
uv sync
```

## Usage

### Running the Application

```bash
uv run python main.py
```

Or use the uv virtual environment:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

### Using the Calculator

1. **Select Calculation Mode**:
   - **Real Numbers**: For calculating square roots of positive real numbers
   - **Complex Numbers**: For calculating square roots of complex numbers

2. **Enter Input**:
   - **Real Mode**: Enter a single number in the input field
   - **Complex Mode**: Enter the real and imaginary parts separately

3. **Set Precision**: Use the spinbox to set the desired precision (decimal places)

4. **Calculate**: Click the "Calculate" button to compute the result

5. **Change Language**: Use the language dropdown to switch between English and Russian

### Examples

#### Real Numbers
- Input: `16` → Result: `4`
- Input: `2` → Result: `1.4142135623730950488016887242096980785696718753769...`
- Input: `123456789` → Result: `11111.111106111111061111110617283950617283950617284...`

#### Complex Numbers
- Real: `3`, Imaginary: `4` → Result: `2+1i`
- Real: `-1`, Imaginary: `0` → Result: `0+1i` (equivalent to √(-1) = i)
- Real: `0`, Imaginary: `1` → Result: `0.707...+0.707...i`

## Project Structure

```
square-root-calculator/
├── src/
│   └── square_root_calculator/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── calculator.py      # Core calculation logic
│       ├── ui/
│       │   ├── __init__.py
│       │   └── main_window.py     # PyQt6 GUI
│       └── locales/
│           ├── __init__.py
│           └── translator.py      # Multilingual support
├── main.py                        # Application entry point
├── pyproject.toml                 # Project configuration
├── README.md                      # This file
└── .gitignore                     # Git ignore rules
```

## Architecture

### Core Components

1. **Calculator Module** (`core/calculator.py`):
   - `SquareRootCalculator`: Main calculator class with configurable precision
   - Uses Python's `decimal` module for arbitrary precision arithmetic
   - Supports both real and complex number calculations

2. **UI Module** (`ui/main_window.py`):
   - `MainWindow`: PyQt6-based graphical interface
   - Responsive layout with mode switching
   - Integrated precision control

3. **Localization Module** (`locales/translator.py`):
   - `Translator`: Translation system supporting multiple languages
   - Currently supports English and Russian
   - Easy to extend with additional languages

## Development

### Setting Up Development Environment

```bash
# Install uv if not already installed
pip install uv

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Adding New Languages

To add a new language, edit `src/square_root_calculator/locales/translator.py` and add a new entry to the `TRANSLATIONS` dictionary:

```python
TRANSLATIONS = {
    'en': { ... },
    'ru': { ... },
    'fr': {  # New language
        'app_title': 'Calculatrice de Racine Carrée',
        # ... add all translation keys
    }
}
```

## Technical Details

### Precision Calculation

The calculator uses Python's `decimal` module with configurable precision:
- Default precision: 50 decimal places
- Range: 1 to 1000 decimal places
- Precision affects all intermediate and final calculations

### Complex Number Algorithm

For a complex number z = a + bi, the square root is calculated using:

```
√z = √((|z| + a)/2) + i · sign(b) · √((|z| - a)/2)
```

where |z| = √(a² + b²)

This algorithm ensures accurate results for all complex numbers.

## Error Handling

The application handles various error scenarios:
- Invalid number format
- Negative numbers in real mode
- Invalid precision values
- Calculation overflow/underflow

All errors are displayed in user-friendly dialog boxes with localized messages.

## Cross-Platform Support

The application is built using:
- **PyQt6**: Cross-platform GUI framework
- **Python decimal module**: Standard library, available on all platforms
- **uv**: Modern, cross-platform Python package manager

Tested on:
- Linux (Ubuntu 20.04+)
- Windows 10/11
- macOS 10.15+

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Authors

- Developed as a comprehensive square root calculator solution
- Multilingual support for international users
- High-precision calculations for scientific and educational use
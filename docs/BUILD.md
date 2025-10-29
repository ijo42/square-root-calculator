# Build and Distribution Guide

> **[Русская версия](BUILD.ru.md)** | **English version**

This guide explains how to build standalone executables for the Square Root Calculator application on Linux (ELF) and Windows (.exe).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Building from Source](#building-from-source)
- [Creating Standalone Executables](#creating-standalone-executables)
  - [Linux ELF Executable](#linux-elf-executable)
  - [Windows EXE Executable](#windows-exe-executable)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools

1. **uv** - Modern Python package manager
   ```bash
   # Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Python 3.12+** - Managed by uv automatically

### Clone the Repository

```bash
git clone https://github.com/ijo42/square-root-calculator.git
cd square-root-calculator
```

## Building from Source

### 1. Sync Dependencies

Install all required dependencies including PyInstaller:

```bash
# Install with development dependencies (includes pyinstaller)
uv sync --dev
```

This installs:
- PyQt6 (application framework)
- qt-material (theming)
- pytest, pytest-cov, pytest-qt (testing)
- black, flake8 (code quality)
- **pyinstaller** (building executables)

### 2. Run the Application

Test that the application runs correctly before building:

```bash
# Run directly
uv run python main.py
```

### 3. Run Tests (Optional)

Ensure all tests pass before building:

```bash
# Linux
./run_tests.sh

# Windows
run_tests.bat

# Cross-platform
uv run python run_tests.py
```

## Creating Standalone Executables

### Build Specification File

Create a file named `square_root_calculator.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'qt_material',
        'square_root_calculator',
        'square_root_calculator.core',
        'square_root_calculator.core.calculator',
        'square_root_calculator.core.history',
        'square_root_calculator.core.settings',
        'square_root_calculator.core.update_checker',
        'square_root_calculator.ui',
        'square_root_calculator.ui.main_window',
        'square_root_calculator.locales',
        'square_root_calculator.locales.translator',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SquareRootCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application, no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### Linux ELF Executable

Build a standalone Linux executable:

```bash
# Build using the spec file
uv run pyinstaller square_root_calculator.spec

# The executable will be created in:
#   dist/SquareRootCalculator (ELF binary)

# Make it executable (if needed)
chmod +x dist/SquareRootCalculator

# Test the executable
./dist/SquareRootCalculator
```

**Output**: `dist/SquareRootCalculator` - A single ELF binary that runs on Linux

### Windows EXE Executable

Build a standalone Windows executable:

```powershell
# Build using the spec file
uv run pyinstaller square_root_calculator.spec

# The executable will be created in:
#   dist\SquareRootCalculator.exe

# Test the executable
.\dist\SquareRootCalculator.exe
```

**Output**: `dist\SquareRootCalculator.exe` - A single Windows executable

### Build Options Explained

The spec file uses these important options:

- `--onefile` (implicit in spec): Creates a single executable file
- `--windowed` (console=False): No console window for GUI application
- `hiddenimports`: Explicitly includes PyQt6 and all application modules
- `upx=True`: Compresses the executable to reduce size

## Troubleshooting

### Common Issues

#### "No module named PyQt6" Error

This occurs when PyInstaller doesn't detect PyQt6 dependencies. The spec file includes all necessary hiddenimports to fix this:

```python
hiddenimports=[
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'qt_material',
    # All application modules explicitly listed
]
```

**Solution**: Use the provided spec file which already includes all required imports.

#### Missing Dependencies

```bash
# Ensure all dependencies are installed
uv sync --dev

# Verify imports work
uv run python -c "import PyQt6; import qt_material; print('OK')"
```

#### Clean Build

If you encounter errors, clean build artifacts and rebuild:

```bash
# Linux/macOS
rm -rf build dist __pycache__
rm *.spec  # Only if you want to recreate spec file

# Windows
rmdir /s /q build dist __pycache__
del *.spec  # Only if you want to recreate spec file

# Rebuild
uv run pyinstaller square_root_calculator.spec
```

#### Qt Platform Plugin Error

If you get "Could not find the Qt platform plugin", ensure the spec file includes:

```python
# PyQt6 and qt_material in hiddenimports
hiddenimports=[
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'qt_material',
]
```

#### Application Won't Start

```bash
# Build with console enabled for debugging
# Edit spec file: change console=False to console=True
console=True,  # Shows console window with error messages

# Rebuild and check console output
uv run pyinstaller square_root_calculator.spec
```

#### Size Optimization

Reduce executable size:

```bash
# Install UPX compression tool
# Linux: apt-get install upx-ucl
# Windows: Download from https://upx.github.io/

# The spec file already has upx=True
# This typically reduces size by 50-70%
```

### Testing Builds

Test the built executables on clean systems to ensure all dependencies are included:

```bash
# Linux: Test on different distribution
# Copy dist/SquareRootCalculator to another Linux machine
./SquareRootCalculator

# Windows: Test on clean Windows installation
# Copy dist\SquareRootCalculator.exe to another Windows machine
SquareRootCalculator.exe
```

### Debug Build

For troubleshooting, create a debug build:

```bash
# Add --debug=all flag
uv run pyinstaller --debug=all square_root_calculator.spec

# Or edit spec file:
exe = EXE(
    ...
    debug=True,  # Enable debug mode
    console=True,  # Show console for error messages
    ...
)
```

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [PyQt6 Deployment](https://www.riverbankcomputing.com/static/Docs/PyQt6/deployment.html)

## Support

For build issues or questions:
- Open an issue: https://github.com/ijo42/square-root-calculator/issues
- Check existing issues for solutions
- Review documentation at: https://github.com/ijo42/square-root-calculator

---

**Note**: Building for specific platforms requires building on that platform. Build Linux executables on Linux, Windows executables on Windows.

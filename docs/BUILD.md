# Build and Distribution Guide

> **[Русская версия](BUILD.ru.md)** | **English version**

This guide explains how to build distributable packages for the Square Root Calculator application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Building from Source](#building-from-source)
- [Creating Distributable Packages](#creating-distributable-packages)
  - [Python Wheel Package](#python-wheel-package)
  - [Standalone Executables](#standalone-executables)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools

1. **uv** - Modern Python package manager
   ```bash
   # Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or via pip
   pip install uv
   ```

2. **Python 3.12+** - Already managed by uv
   ```bash
   # Check Python version
   python --version
   ```

3. **PyInstaller** (for standalone executables)
   ```bash
   uv pip install pyinstaller
   ```

### Clone the Repository

```bash
git clone https://github.com/ijo42/square-root-calculator.git
cd square-root-calculator
```

## Building from Source

### 1. Sync Dependencies

Install all required dependencies using uv:

```bash
# Install production dependencies
uv sync

# Install with development dependencies
uv sync --dev
```

### 2. Run the Application

Test that the application runs correctly:

```bash
# Run directly
uv run python main.py

# Or use the installed script
uv run square-root-calculator
```

### 3. Run Tests

Ensure all tests pass before building:

```bash
# Linux/macOS
./run_tests.sh

# Windows
run_tests.bat

# Cross-platform
uv run python run_tests.py
```

## Creating Distributable Packages

### Python Wheel Package

A wheel package (.whl) can be installed on any system with Python.

#### Build the Wheel

```bash
# Using uv
uv build

# This creates files in dist/:
#   - square_root_calculator-0.1.0-py3-none-any.whl
#   - square_root_calculator-0.1.0.tar.gz
```

#### Install the Wheel

```bash
# Install locally
uv pip install dist/square_root_calculator-0.1.0-py3-none-any.whl

# Or with pip
pip install dist/square_root_calculator-0.1.0-py3-none-any.whl

# Run the installed application
square-root-calculator
```

#### Distribute the Wheel

Upload to PyPI (requires account):

```bash
# Install twine
uv pip install twine

# Upload to PyPI
uv run twine upload dist/*

# Upload to TestPyPI first (recommended)
uv run twine upload --repository testpypi dist/*
```

### Standalone Executables

Create platform-specific executables that don't require Python installation.

#### Install PyInstaller

```bash
uv pip install pyinstaller
```

#### Create Build Specification

Create a file `build.spec`:

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
        'square_root_calculator.ui',
        'square_root_calculator.locales',
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
    console=False,  # Set to True for console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Optional: add your icon file
)
```

#### Build the Executable

```bash
# Using the spec file
uv run pyinstaller build.spec

# Or directly (simpler, less control)
uv run pyinstaller --name="SquareRootCalculator" \
    --windowed \
    --onefile \
    main.py

# The executable will be in:
#   dist/SquareRootCalculator (Linux/macOS)
#   dist/SquareRootCalculator.exe (Windows)
```

#### Build Options

- `--onefile`: Create a single executable file
- `--windowed` / `--noconsole`: Don't show console window (GUI only)
- `--console`: Show console window (for debugging)
- `--icon=icon.ico`: Set application icon
- `--add-data`: Include additional data files
- `--hidden-import`: Include modules not automatically detected

## Platform-Specific Instructions

### Linux

#### AppImage

Create a portable Linux application:

```bash
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
mkdir -p SquareRootCalculator.AppDir/usr/bin
mkdir -p SquareRootCalculator.AppDir/usr/share/applications
mkdir -p SquareRootCalculator.AppDir/usr/share/icons

# Copy executable
cp dist/SquareRootCalculator SquareRootCalculator.AppDir/usr/bin/

# Create desktop entry
cat > SquareRootCalculator.AppDir/usr/share/applications/square-root-calculator.desktop << EOF
[Desktop Entry]
Type=Application
Name=Square Root Calculator
Exec=SquareRootCalculator
Icon=square-root-calculator
Categories=Education;Math;
EOF

# Create AppImage
./appimagetool-x86_64.AppImage SquareRootCalculator.AppDir
```

#### Debian Package

```bash
# Create package structure
mkdir -p square-root-calculator_0.1.0/DEBIAN
mkdir -p square-root-calculator_0.1.0/usr/bin
mkdir -p square-root-calculator_0.1.0/usr/share/applications

# Create control file
cat > square-root-calculator_0.1.0/DEBIAN/control << EOF
Package: square-root-calculator
Version: 0.1.0
Architecture: amd64
Maintainer: Square Root Calculator Team
Description: Square root calculator with arbitrary precision
 A comprehensive calculator for square roots supporting real numbers,
 complex numbers, and arbitrary precision calculations.
EOF

# Copy executable
cp dist/SquareRootCalculator square-root-calculator_0.1.0/usr/bin/

# Build package
dpkg-deb --build square-root-calculator_0.1.0
```

### macOS

#### DMG Installer

```bash
# Create DMG
hdiutil create -volname "Square Root Calculator" \
    -srcfolder dist/SquareRootCalculator.app \
    -ov -format UDZO \
    SquareRootCalculator-0.1.0.dmg
```

#### App Bundle

PyInstaller automatically creates .app bundles on macOS:

```bash
uv run pyinstaller --name="SquareRootCalculator" \
    --windowed \
    --onefile \
    main.py

# The app will be in:
#   dist/SquareRootCalculator.app
```

### Windows

#### MSI Installer

Using WiX Toolset:

1. Install WiX Toolset: https://wixtoolset.org/
2. Create `installer.wxs`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" Name="Square Root Calculator" Language="1033" 
             Version="0.1.0" Manufacturer="Square Root Calculator Team"
             UpgradeCode="PUT-GUID-HERE">
        <Package InstallerVersion="200" Compressed="yes" />
        
        <Media Id="1" Cabinet="product.cab" EmbedCab="yes" />
        
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="SquareRootCalculator" />
            </Directory>
        </Directory>
        
        <Component Id="MainExecutable" Directory="INSTALLFOLDER" Guid="PUT-GUID-HERE">
            <File Id="SquareRootCalculatorEXE" Source="dist\SquareRootCalculator.exe" />
        </Component>
        
        <Feature Id="ProductFeature" Title="Square Root Calculator" Level="1">
            <ComponentRef Id="MainExecutable" />
        </Feature>
    </Product>
</Wix>
```

3. Build MSI:

```bash
candle installer.wxs
light installer.wixobj -o SquareRootCalculator-0.1.0.msi
```

#### NSIS Installer

Using NSIS (Nullsoft Scriptable Install System):

1. Install NSIS: https://nsis.sourceforge.io/
2. Create `installer.nsi`:

```nsis
!define APPNAME "Square Root Calculator"
!define COMPANYNAME "Square Root Calculator Team"
!define DESCRIPTION "A comprehensive square root calculator"
!define VERSIONMAJOR 0
!define VERSIONMINOR 1
!define VERSIONBUILD 0

RequestExecutionLevel admin

InstallDir "$PROGRAMFILES\${APPNAME}"

Name "${APPNAME}"
outFile "SquareRootCalculator-Setup-0.1.0.exe"

Page directory
Page instfiles

Section "install"
    SetOutPath $INSTDIR
    File "dist\SquareRootCalculator.exe"
    
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\SquareRootCalculator.exe"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
SectionEnd

Section "uninstall"
    Delete "$INSTDIR\SquareRootCalculator.exe"
    Delete "$INSTDIR\uninstall.exe"
    
    RMDir "$SMPROGRAMS\${APPNAME}"
    RMDir "$INSTDIR"
SectionEnd
```

3. Build installer:

```bash
makensis installer.nsi
```

## Troubleshooting

### Common Issues

#### Missing Dependencies

```bash
# Ensure all dependencies are installed
uv sync --dev

# Check for missing imports
uv run python -c "import PyQt6; import qt_material; print('OK')"
```

#### PyInstaller Errors

```bash
# Clean build artifacts
rm -rf build dist __pycache__
rm *.spec

# Rebuild with verbose output
uv run pyinstaller --debug=all build.spec
```

#### Qt Platform Plugin Error

Add Qt plugins to PyInstaller:

```python
# In build.spec, add to datas:
datas=[
    ('path/to/qt/plugins/platforms', 'platforms'),
],
```

#### Application Won't Start

```bash
# Test with console enabled
uv run pyinstaller --console build.spec

# Check error messages in console output
```

### Size Optimization

Reduce executable size:

```bash
# Use UPX compression
uv run pyinstaller --upx-dir=/path/to/upx build.spec

# Exclude unnecessary packages
uv run pyinstaller --exclude-module matplotlib build.spec
```

### Testing Builds

Always test built packages on clean systems:

```bash
# Linux: Use Docker
docker run -it -v $(pwd)/dist:/dist ubuntu:latest
cd /dist && ./SquareRootCalculator

# Windows: Use VM or clean Windows installation
# macOS: Use another Mac or fresh user account
```

## Continuous Integration

### GitHub Actions

Example workflow for automated builds:

```yaml
name: Build Releases

on:
  release:
    types: [created]

jobs:
  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Build
        run: |
          uv sync
          uv pip install pyinstaller
          uv run pyinstaller build.spec
      - name: Upload
        uses: actions/upload-artifact@v3
        with:
          name: linux-build
          path: dist/SquareRootCalculator

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install uv
        run: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
      - name: Build
        run: |
          uv sync
          uv pip install pyinstaller
          uv run pyinstaller build.spec
      - name: Upload
        uses: actions/upload-artifact@v3
        with:
          name: windows-build
          path: dist/SquareRootCalculator.exe

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Build
        run: |
          uv sync
          uv pip install pyinstaller
          uv run pyinstaller build.spec
      - name: Upload
        uses: actions/upload-artifact@v3
        with:
          name: macos-build
          path: dist/SquareRootCalculator.app
```

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Python Packaging Guide](https://packaging.python.org/)
- [PyQt6 Deployment](https://www.riverbankcomputing.com/static/Docs/PyQt6/deployment.html)

## Support

For build issues or questions:
- Open an issue: https://github.com/ijo42/square-root-calculator/issues
- Check existing issues for solutions
- Review documentation at: https://github.com/ijo42/square-root-calculator

---

**Note**: Building for specific platforms requires that platform (or a cross-compilation setup). For best results, build on the target platform.

# Contributing to Square Root Calculator

Thank you for your interest in contributing to the Square Root Calculator project! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- uv (recommended) or pip

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/square-root-calculator.git
   cd square-root-calculator
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify installation:**
   ```bash
   pytest --version
   python main.py  # Should launch the application
   ```

## Development Workflow

### Making Changes

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow the existing code style
   - Add docstrings to functions and classes
   - Keep changes focused and atomic

3. **Test your changes:**
   ```bash
   # Run quick tests during development
   ./test_quick.sh
   
   # Run full test suite before committing
   ./run_tests.sh
   ```

4. **Check code quality:**
   ```bash
   # If you have make installed
   make lint
   make format
   
   # Or manually
   black src/ tests/
   flake8 src/ tests/
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: Add new feature description"
   ```

### Commit Message Guidelines

Use conventional commit format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting)
- `chore:` - Maintenance tasks

Examples:
```
feat: Add polar form display for complex numbers
fix: Correct precision handling in calculations
docs: Update testing guide with new examples
test: Add tests for settings persistence
```

## Testing Guidelines

### Running Tests

```bash
# Quick test during development
./test_quick.sh

# Full test suite with coverage
./run_tests.sh

# Test specific file
pytest tests/test_calculator.py

# Test specific function
pytest tests/test_calculator.py::TestSquareRootCalculator::test_sqrt_real_perfect_square
```

### Writing Tests

1. **Add tests for new features:**
   - Place tests in appropriate test file
   - Use descriptive test names
   - Test both success and error cases

2. **Use existing fixtures:**
   ```python
   def test_my_feature(calculator, translator_en):
       """Test description."""
       # Test implementation
       assert calculator.sqrt_real(4) == Decimal('2')
   ```

3. **Test structure:**
   ```python
   def test_feature_name():
       """Test description explaining what is tested."""
       # Arrange - set up test data
       calc = SquareRootCalculator(precision=10)
       
       # Act - perform the action
       result = calc.sqrt_real(16)
       
       # Assert - verify the result
       assert result == Decimal('4')
   ```

4. **Coverage requirements:**
   - New features should include tests
   - Aim for >90% coverage for new code
   - Test edge cases and error conditions

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_calculator.py       # Calculator tests
├── test_history.py          # History tests
├── test_translator.py       # Translation tests
└── test_settings.py         # Settings tests
```

## Code Style

### Python Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Maximum line length: 127 characters
- Use descriptive variable names

### Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings:
  ```python
  def calculate_sqrt(value: float, precision: int) -> Decimal:
      """
      Calculate square root with specified precision.
      
      Args:
          value: The number to calculate square root of
          precision: Number of decimal places
          
      Returns:
          Square root as Decimal with specified precision
          
      Raises:
          InvalidInputError: If value is invalid
      """
      # Implementation
  ```

### UI Guidelines

- Keep UI responsive
- Provide user feedback for long operations
- Use consistent styling across components
- Test on different screen sizes

## Adding New Features

### New Calculation Features

1. Add core logic to `src/square_root_calculator/core/calculator.py`
2. Add UI elements to `src/square_root_calculator/ui/main_window.py`
3. Add translations to `src/square_root_calculator/locales/translator.py`
4. Write tests in `tests/test_calculator.py`
5. Update documentation in `README.md` and `docs/`

### New Languages

1. Add translations to `translator.py`:
   ```python
   'es': {
       'app_title': 'Calculadora de Raíz Cuadrada',
       # ... more translations
   }
   ```

2. Update language menu in `main_window.py`
3. Add tests in `test_translator.py`
4. Update documentation

## Pull Request Process

1. **Update documentation:**
   - Update README.md if needed
   - Add or update relevant docs
   - Update CHANGELOG if applicable

2. **Ensure tests pass:**
   ```bash
   ./run_tests.sh
   ```

3. **Check coverage:**
   - Ensure new code has good test coverage
   - Coverage report: `htmlcov/index.html`

4. **Submit pull request:**
   - Provide clear description
   - Reference any related issues
   - Include screenshots for UI changes

5. **CI/CD checks:**
   - GitHub Actions will run automatically
   - All tests must pass
   - Linting checks must pass

## Project Structure

```
square-root-calculator/
├── src/square_root_calculator/    # Main package
│   ├── core/                      # Core calculation logic
│   │   ├── calculator.py          # Calculator engine
│   │   ├── history.py             # History management
│   │   ├── settings.py            # Settings management
│   │   └── update_checker.py     # Update checking
│   ├── ui/                        # User interface
│   │   └── main_window.py         # Main window
│   └── locales/                   # Translations
│       └── translator.py          # Translation system
├── tests/                         # Test suite
├── docs/                          # Documentation
├── .github/workflows/             # CI/CD pipelines
├── main.py                        # Entry point
├── pyproject.toml                 # Project config
├── pytest.ini                     # Test config
└── README.md                      # Main documentation
```

## Useful Commands

### Using Make (Linux/macOS)

```bash
make help       # Show all commands
make install    # Install dependencies
make test       # Run tests with coverage
make coverage   # Open coverage report
make run        # Run application
make lint       # Check code style
make format     # Format code
make clean      # Remove generated files
```

### Using Scripts

```bash
./run_tests.sh      # Full test suite (Linux/macOS)
run_tests.bat       # Full test suite (Windows)
./test_quick.sh     # Quick tests (Linux/macOS)
test_quick.bat      # Quick tests (Windows)
python run_tests.py # Cross-platform test runner
```

## Getting Help

- Open an issue for bug reports or feature requests
- Use discussions for questions
- Check existing issues before creating new ones
- Provide detailed information:
  - Python version
  - Operating system
  - Steps to reproduce
  - Error messages

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the project goals
- Help others learn and grow

## Recognition

Contributors will be acknowledged in:
- GitHub contributors page
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Square Root Calculator! 🎉

"""Tests for calculator core functionality."""

import pytest
from decimal import Decimal
from square_root_calculator.core.calculator import (
    SquareRootCalculator,
    InvalidInputError,
    CalculationResult
)


class TestSquareRootCalculator:
    """Test calculator basic operations."""
    
    def test_sqrt_real_perfect_square(self, calculator):
        """Test square root of perfect squares."""
        result = calculator.sqrt_real(16)
        assert result == Decimal('4')
        
    def test_sqrt_real_irrational(self, calculator):
        """Test square root of irrational numbers."""
        result = calculator.sqrt_real(2)
        # Should start with 1.414...
        assert str(result).startswith('1.414')
        
    def test_sqrt_real_zero(self, calculator):
        """Test square root of zero."""
        result = calculator.sqrt_real(0)
        assert result == Decimal('0')
        
    def test_sqrt_real_negative_raises_error(self, calculator):
        """Test that negative real numbers raise error."""
        with pytest.raises(InvalidInputError):
            calculator.sqrt_real(-1)
    
    def test_sqrt_complex_real_positive(self, calculator):
        """Test complex sqrt with real positive number."""
        real, imag = calculator.sqrt_complex(4, 0)
        assert real == Decimal('2')
        assert imag == Decimal('0')
    
    def test_sqrt_complex_standard(self, calculator):
        """Test complex sqrt of 3+4i = 2+1i."""
        real, imag = calculator.sqrt_complex(3, 4)
        assert abs(float(real) - 2.0) < 0.01
        assert abs(float(imag) - 1.0) < 0.01
    
    def test_sqrt_complex_negative_real(self, calculator):
        """Test complex sqrt of -1 = i."""
        real, imag = calculator.sqrt_complex(-1, 0)
        assert real == Decimal('0')
        assert abs(float(imag) - 1.0) < 0.01
    
    def test_precision_change(self, calculator):
        """Test changing precision."""
        calculator.set_precision(20)
        result = calculator.sqrt_real(2)
        result_str = str(result)
        assert len(result_str.replace('.', '')) >= 15
    
    def test_invalid_input(self, calculator):
        """Test invalid input handling."""
        with pytest.raises(InvalidInputError):
            calculator.sqrt_real("invalid")
    
    def test_format_result(self, calculator):
        """Test result formatting."""
        result = calculator.sqrt_real(2)
        formatted = calculator.format_result(result, max_digits=5)
        assert '1.4142' in formatted


class TestCalculationResult:
    """Test CalculationResult class."""
    
    def test_calculation_result_real(self, calculator):
        """Test CalculationResult for real numbers."""
        result = calculator.calculate(4)
        assert result.input_value == '4'
        assert not result.is_complex
        assert len(result.roots) == 2
        
    def test_calculation_result_complex(self, calculator):
        """Test CalculationResult for complex numbers."""
        result = calculator.calculate(None, 3, 4)
        assert result.is_complex
        assert len(result.roots) == 2
    
    def test_get_formatted_roots(self, calculator):
        """Test getting formatted roots."""
        result = calculator.calculate(4)
        formatted = result.get_formatted_roots()
        assert len(formatted) == 2
        assert '2' in formatted[0]
        assert '-2' in formatted[1]
    
    def test_get_representations_real(self, calculator):
        """Test representations for real numbers."""
        result = calculator.calculate(2)
        reps = result.get_representations()
        assert 'decimal' in reps
        assert 'scientific' in reps
    
    def test_get_representations_complex(self, calculator):
        """Test representations for complex numbers."""
        result = calculator.calculate(None, 3, 4)
        reps = result.get_representations()
        assert 'polar' in reps
        assert 'exponential' in reps

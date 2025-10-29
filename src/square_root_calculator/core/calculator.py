"""Square root calculator with support for real, complex, and high-precision numbers."""

import decimal
from decimal import Decimal, getcontext
from typing import Union


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class InvalidInputError(CalculatorError):
    """Exception raised for invalid input."""
    pass


class SquareRootCalculator:
    """Calculator for computing square roots with configurable precision."""
    
    def __init__(self, precision: int = 50):
        """
        Initialize calculator with specified precision.
        
        Args:
            precision: Number of decimal places for precision (default: 50)
        """
        self.precision = precision
        getcontext().prec = precision
    
    def set_precision(self, precision: int):
        """
        Set the precision for calculations.
        
        Args:
            precision: Number of decimal places
        """
        if precision < 1:
            raise InvalidInputError("Precision must be at least 1")
        self.precision = precision
        getcontext().prec = precision
    
    def sqrt_real(self, value: Union[int, float, str, Decimal]) -> Decimal:
        """
        Calculate square root of a real number.
        
        Args:
            value: The number to calculate square root of
            
        Returns:
            Square root as Decimal
            
        Raises:
            InvalidInputError: If input is invalid or negative
        """
        try:
            num = Decimal(str(value))
        except (ValueError, decimal.InvalidOperation) as e:
            raise InvalidInputError(f"Invalid number format: {e}")
        
        if num < 0:
            raise InvalidInputError("Cannot calculate square root of negative real number. Use complex mode.")
        
        return num.sqrt()
    
    def sqrt_complex(self, real: Union[int, float, str], imag: Union[int, float, str] = 0) -> tuple[Decimal, Decimal]:
        """
        Calculate square root of a complex number.
        
        Args:
            real: Real part of the complex number
            imag: Imaginary part of the complex number
            
        Returns:
            Tuple of (real_part, imaginary_part) of the result
            
        Raises:
            InvalidInputError: If input is invalid
        """
        try:
            a = Decimal(str(real))
            b = Decimal(str(imag))
        except (ValueError, decimal.InvalidOperation) as e:
            raise InvalidInputError(f"Invalid number format: {e}")
        
        # For complex number z = a + bi, sqrt(z) is calculated as:
        # sqrt(z) = sqrt((|z| + a)/2) + i * sign(b) * sqrt((|z| - a)/2)
        # where |z| = sqrt(a^2 + b^2)
        
        magnitude = (a**2 + b**2).sqrt()
        
        real_part = ((magnitude + a) / 2).sqrt()
        
        if b >= 0:
            imag_part = ((magnitude - a) / 2).sqrt()
        else:
            imag_part = -((magnitude - a) / 2).sqrt()
        
        return real_part, imag_part
    
    def format_result(self, value: Decimal, max_digits: int = None) -> str:
        """
        Format a decimal result for display.
        
        Args:
            value: The decimal value to format
            max_digits: Maximum number of digits to display (None for all)
            
        Returns:
            Formatted string representation
        """
        if max_digits is None:
            max_digits = self.precision
        
        # Convert to string and limit digits
        result = str(value)
        
        # Handle scientific notation for very large/small numbers
        if 'E' in result.upper():
            return result
        
        # Limit decimal places
        if '.' in result:
            integer_part, decimal_part = result.split('.')
            if len(decimal_part) > max_digits:
                decimal_part = decimal_part[:max_digits]
            result = f"{integer_part}.{decimal_part}"
        
        return result

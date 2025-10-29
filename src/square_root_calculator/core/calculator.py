"""Square root calculator with support for real, complex, and high-precision numbers."""

import decimal
from decimal import Decimal, getcontext
from typing import Union, Dict, List, Tuple


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class InvalidInputError(CalculatorError):
    """Exception raised for invalid input."""
    pass


class CalculationResult:
    """Container for calculation results with multiple representations."""
    
    def __init__(self, input_value: str, roots: List[Tuple[Decimal, Decimal]], 
                 is_complex: bool, precision: int):
        """
        Initialize calculation result.
        
        Args:
            input_value: Original input as string
            roots: List of (real, imaginary) tuples for each root
            is_complex: Whether this is a complex calculation
            precision: Precision used for calculation
        """
        self.input_value = input_value
        self.roots = roots
        self.is_complex = is_complex
        self.precision = precision
    
    def get_formatted_roots(self, max_digits: int = None) -> List[str]:
        """Get formatted string representations of all roots."""
        formatted = []
        for real, imag in self.roots:
            if max_digits is None:
                max_digits = self.precision
            
            real_str = self._format_decimal(real, max_digits)
            imag_str = self._format_decimal(abs(imag), max_digits)
            
            if imag == 0:
                formatted.append(real_str)
            else:
                sign = '+' if imag >= 0 else '-'
                formatted.append(f"{real_str}{sign}{imag_str}i")
        
        return formatted
    
    def _format_decimal(self, value: Decimal, max_digits: int) -> str:
        """Format a single decimal value."""
        result = str(value)
        
        if 'E' in result.upper():
            return result
        
        if '.' in result:
            integer_part, decimal_part = result.split('.')
            if len(decimal_part) > max_digits:
                decimal_part = decimal_part[:max_digits]
            result = f"{integer_part}.{decimal_part}"
        
        return result
    
    def get_representations(self) -> Dict[str, str]:
        """Get various representations of the result."""
        representations = {}
        
        if not self.is_complex and len(self.roots) > 0:
            real_val = self.roots[0][0]
            
            # Standard decimal
            representations['decimal'] = self._format_decimal(real_val, self.precision)
            
            # Scientific notation
            try:
                exp_notation = f"{float(real_val):.{min(15, self.precision)}e}"
                representations['scientific'] = exp_notation
            except:
                pass
            
            # Fractional approximation (for small numbers)
            if abs(real_val) < 1000:
                try:
                    from fractions import Fraction
                    frac = Fraction(float(real_val)).limit_denominator(10000)
                    if abs(float(frac) - float(real_val)) < 0.0001:
                        representations['fraction'] = f"{frac.numerator}/{frac.denominator}"
                except:
                    pass
        
        return representations


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
    
    def calculate(self, value: Union[int, float, str, Decimal], 
                  real_part: Union[int, float, str] = None,
                  imag_part: Union[int, float, str] = None) -> CalculationResult:
        """
        Calculate square root(s) and return all roots with multiple representations.
        
        Args:
            value: Value for real mode
            real_part: Real part for complex mode
            imag_part: Imaginary part for complex mode
            
        Returns:
            CalculationResult with all roots and representations
        """
        if real_part is not None or imag_part is not None:
            # Complex mode
            if real_part is None:
                real_part = 0
            if imag_part is None:
                imag_part = 0
            
            input_str = self._format_complex_input(real_part, imag_part)
            root1_real, root1_imag = self.sqrt_complex(real_part, imag_part)
            
            # Both roots: +sqrt and -sqrt
            roots = [
                (root1_real, root1_imag),
                (-root1_real, -root1_imag)
            ]
            
            return CalculationResult(input_str, roots, True, self.precision)
        else:
            # Real mode
            input_str = str(value)
            root = self.sqrt_real(value)
            
            # Both roots: +sqrt and -sqrt
            roots = [
                (root, Decimal(0)),
                (-root, Decimal(0))
            ]
            
            return CalculationResult(input_str, roots, False, self.precision)
    
    def _format_complex_input(self, real: Union[int, float, str], 
                              imag: Union[int, float, str]) -> str:
        """Format complex input for display."""
        real_str = str(real)
        imag_str = str(imag)
        
        if imag_str == '0':
            return real_str
        
        if imag_str.startswith('-'):
            return f"{real_str}{imag_str}i"
        else:
            return f"{real_str}+{imag_str}i"
    
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


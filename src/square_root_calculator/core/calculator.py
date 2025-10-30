"""Square root calculator with support for real, complex, and high-precision numbers.

Калькулятор квадратного корня с поддержкой действительных, комплексных чисел и высокой точности.
"""

import decimal
from decimal import Decimal, getcontext
from typing import Union, Dict, List, Tuple


class CalculatorError(Exception):
    """Base exception for calculator errors.

    Базовое исключение для ошибок калькулятора.
    """

    pass


class InvalidInputError(CalculatorError):
    """Exception raised for invalid input.

    Исключение, возникающее при неверных входных данных.
    """

    pass


class CalculationResult:
    """Container for calculation results with multiple representations.

    Контейнер для результатов вычислений с множественными представлениями.
    """

    def __init__(
        self,
        input_value: str,
        roots: List[Tuple[Decimal, Decimal]],
        is_complex: bool,
        precision: int,
    ):
        """Initialize calculation result.

        Инициализировать результат вычисления.

        Args:
            input_value: Original input as string
                        Исходное входное значение в виде строки
            roots: List of (real, imaginary) tuples for each root
                  Список кортежей (действительная, мнимая) для каждого корня
            is_complex: Whether this is a complex calculation
                       Является ли это комплексным вычислением
            precision: Precision used for calculation
                      Точность, используемая для вычисления
        """
        self.input_value = input_value
        self.roots = roots
        self.is_complex = is_complex
        self.precision = precision

    def get_formatted_roots(self, max_digits: int = None) -> List[str]:
        """Get formatted string representations of all roots.

        Получить форматированные строковые представления всех корней.

        Args:
            max_digits: Maximum number of digits to display
                       Максимальное количество отображаемых цифр

        Returns:
            List of formatted root strings
            Список форматированных строк корней
        """
        formatted = []
        for real, imag in self.roots:
            if max_digits is None:
                max_digits = self.precision

            real_str = self._format_decimal(real, max_digits)
            imag_str = self._format_decimal(abs(imag), max_digits)

            if imag == 0:
                formatted.append(real_str)
            else:
                sign = "+" if imag >= 0 else "-"
                formatted.append(f"{real_str}{sign}{imag_str}i")

        return formatted

    def _format_decimal(self, value: Decimal, max_digits: int) -> str:
        """Format a single decimal value.

        Форматировать одно десятичное значение.

        Args:
            value: Decimal value to format
                  Десятичное значение для форматирования
            max_digits: Maximum digits after decimal point
                       Максимум цифр после десятичной точки

        Returns:
            Formatted string
            Форматированная строка
        """
        result = str(value)

        if "E" in result.upper():
            return result

        if "." in result:
            integer_part, decimal_part = result.split(".")
            if len(decimal_part) > max_digits:
                decimal_part = decimal_part[:max_digits]
            result = f"{integer_part}.{decimal_part}"

        return result

    def get_representations(self) -> Dict[str, str]:
        """Get various representations of the result.

        Получить различные представления результата.

        Returns:
            Dictionary with different representations (decimal, scientific, fraction, polar, exponential)
            Словарь с различными представлениями (десятичное, научное, дробное, полярное, экспоненциальное)
        """
        representations = {}

        if not self.is_complex and len(self.roots) > 0:
            real_val = self.roots[0][0]

            # Standard decimal
            representations["decimal"] = self._format_decimal(real_val, self.precision)

            # Scientific notation
            try:
                exp_notation = f"{float(real_val):.{min(15, self.precision)}e}"
                representations["scientific"] = exp_notation
            except:
                pass

            # Fractional approximation (for small numbers)
            if abs(real_val) < 1000:
                try:
                    from fractions import Fraction

                    frac = Fraction(float(real_val)).limit_denominator(10000)
                    if abs(float(frac) - float(real_val)) < 0.0001:
                        representations["fraction"] = (
                            f"{frac.numerator}/{frac.denominator}"
                        )
                except:
                    pass
        elif self.is_complex and len(self.roots) > 0:
            # Alternative forms for complex numbers
            import math

            real_val, imag_val = self.roots[0]

            # Convert to polar form (r, θ)
            try:
                r = math.sqrt(float(real_val) ** 2 + float(imag_val) ** 2)
                theta = math.atan2(float(imag_val), float(real_val))
                theta_deg = math.degrees(theta)

                r_fmt = self._format_decimal(Decimal(str(r)), min(10, self.precision))
                theta_fmt = self._format_decimal(
                    Decimal(str(theta)), min(10, self.precision)
                )

                representations["polar"] = (
                    f"{r_fmt} ∠ {theta_fmt} rad ({theta_deg:.2f}°)"
                )

                # Exponential form: r * e^(iθ)
                representations["exponential"] = f"{r_fmt} * e^(i*{theta_fmt})"
            except:
                pass

        return representations


class SquareRootCalculator:
    """Calculator for computing square roots with configurable precision.

    Калькулятор для вычисления квадратных корней с настраиваемой точностью.
    """

    def __init__(self, precision: int = 50):
        """Initialize calculator with specified precision.

        Инициализировать калькулятор с заданной точностью.

        Args:
            precision: Number of decimal places for precision (default: 50)
                      Количество десятичных знаков для точности (по умолчанию: 50)
        """
        self.precision = precision
        getcontext().prec = precision

    def set_precision(self, precision: int):
        """Set the precision for calculations.

        Установить точность для вычислений.

        Args:
            precision: Number of decimal places
                      Количество десятичных знаков

        Raises:
            InvalidInputError: If precision is less than 1
                              Если точность меньше 1
        """
        if precision < 1:
            raise InvalidInputError("Precision must be at least 1")
        self.precision = precision
        getcontext().prec = precision

    def calculate(
        self,
        value: Union[int, float, str, Decimal],
        real_part: Union[int, float, str] = None,
        imag_part: Union[int, float, str] = None,
    ) -> CalculationResult:
        """Calculate square root(s) and return all roots with multiple representations.

        Вычислить квадратный корень(и) и вернуть все корни с множественными представлениями.

        Args:
            value: Value for real mode
                  Значение для режима действительных чисел
            real_part: Real part for complex mode
                      Действительная часть для режима комплексных чисел
            imag_part: Imaginary part for complex mode
                      Мнимая часть для режима комплексных чисел

        Returns:
            CalculationResult with all roots and representations
            CalculationResult со всеми корнями и представлениями
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
            roots = [(root1_real, root1_imag), (-root1_real, -root1_imag)]

            return CalculationResult(input_str, roots, True, self.precision)
        else:
            # Real mode
            input_str = str(value)
            root = self.sqrt_real(value)

            # Both roots: +sqrt and -sqrt
            roots = [(root, Decimal(0)), (-root, Decimal(0))]

            return CalculationResult(input_str, roots, False, self.precision)

    def _format_complex_input(
        self, real: Union[int, float, str], imag: Union[int, float, str]
    ) -> str:
        """Format complex input for display.

        Форматировать комплексный ввод для отображения.

        Args:
            real: Real part
                 Действительная часть
            imag: Imaginary part
                 Мнимая часть

        Returns:
            Formatted string (e.g., "3+4i" or "3-4i")
            Форматированная строка (напр., "3+4i" или "3-4i")
        """
        real_str = str(real)
        imag_str = str(imag)

        if imag_str == "0":
            return real_str

        if imag_str.startswith("-"):
            return f"{real_str}{imag_str}i"
        else:
            return f"{real_str}+{imag_str}i"

    def sqrt_real(self, value: Union[int, float, str, Decimal]) -> Decimal:
        """Calculate square root of a real number.

        Вычислить квадратный корень действительного числа.

        Args:
            value: The number to calculate square root of
                  Число для вычисления квадратного корня

        Returns:
            Square root as Decimal
            Квадратный корень как Decimal

        Raises:
            InvalidInputError: If input is invalid or negative
                              Если ввод некорректен или отрицателен
        """
        try:
            num = Decimal(str(value))
        except (ValueError, decimal.InvalidOperation) as e:
            raise InvalidInputError(f"Invalid number format: {e}")

        if num < 0:
            raise InvalidInputError(
                "Cannot calculate square root of negative real number. Use complex mode."
            )

        return num.sqrt()

    def sqrt_complex(
        self, real: Union[int, float, str], imag: Union[int, float, str] = 0
    ) -> tuple[Decimal, Decimal]:
        """Calculate square root of a complex number.

        Вычислить квадратный корень комплексного числа.

        Args:
            real: Real part of the complex number
                 Действительная часть комплексного числа
            imag: Imaginary part of the complex number
                 Мнимая часть комплексного числа

        Returns:
            Tuple of (real_part, imaginary_part) of the result
            Кортеж (действительная_часть, мнимая_часть) результата

        Raises:
            InvalidInputError: If input is invalid
                              Если ввод некорректен
            CalculatorError: If precision is too low for the calculation
                           Если точность слишком низкая для вычисления
        """
        try:
            a = Decimal(str(real))
            b = Decimal(str(imag))
        except (ValueError, decimal.InvalidOperation) as e:
            raise InvalidInputError(f"Invalid number format: {e}")

        # For complex number z = a + bi, sqrt(z) is calculated as:
        # sqrt(z) = sqrt((|z| + a)/2) + i * sign(b) * sqrt((|z| - a)/2)
        # where |z| = sqrt(a^2 + b^2)

        try:
            magnitude = (a**2 + b**2).sqrt()

            real_part = ((magnitude + a) / 2).sqrt()

            # Handle the imaginary part calculation which may fail with low precision
            imag_value = (magnitude - a) / 2
            
            # Check if the value is negative (can happen with rounding in low precision)
            if imag_value < 0:
                # With very low precision, rounding errors can make this slightly negative
                # when it should be zero or very small positive. Use absolute value.
                if abs(imag_value) < Decimal(10) ** (-self.precision + 1):
                    # Treat as zero
                    imag_part = Decimal(0)
                else:
                    raise CalculatorError(
                        f"Precision too low for this calculation. Please increase precision to at least {self.precision + 2} decimal places."
                    )
            else:
                if b >= 0:
                    imag_part = imag_value.sqrt()
                else:
                    imag_part = -imag_value.sqrt()
        except decimal.InvalidOperation as e:
            raise CalculatorError(
                f"Calculation error with current precision ({self.precision}). "
                f"Please increase precision to at least {max(10, self.precision + 5)} decimal places for this calculation."
            )

        return real_part, imag_part

    def format_result(self, value: Decimal, max_digits: int = None) -> str:
        """Format a decimal result for display.

        Форматировать десятичный результат для отображения.

        Args:
            value: The decimal value to format
                  Десятичное значение для форматирования
            max_digits: Maximum number of digits to display (None for all)
                       Максимальное количество отображаемых цифр (None для всех)

        Returns:
            Formatted string representation
            Форматированное строковое представление
        """
        if max_digits is None:
            max_digits = self.precision

        # Convert to string and limit digits
        result = str(value)

        # Handle scientific notation for very large/small numbers
        if "E" in result.upper():
            return result

        # Limit decimal places
        if "." in result:
            integer_part, decimal_part = result.split(".")
            if len(decimal_part) > max_digits:
                decimal_part = decimal_part[:max_digits]
            result = f"{integer_part}.{decimal_part}"

        return result

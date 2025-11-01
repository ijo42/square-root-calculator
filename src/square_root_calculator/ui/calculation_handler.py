"""Calculation handler for executing calculations and handling errors.

Обработчик вычислений для выполнения вычислений и обработки ошибок.
"""

from ..core.calculator import (
    InvalidInputError,
    CalculatorError,
    PrecisionError,
)


class CalculationHandler:
    """Handles calculation execution and error reporting.

    Обрабатывает выполнение вычислений и отчеты об ошибках.
    """

    def __init__(self, calculator, translator, input_validator):
        """Initialize calculation handler.

        Args:
            calculator: Calculator instance
            translator: Translator instance for error messages
            input_validator: InputValidator instance for input normalization
        """
        self.calculator = calculator
        self.translator = translator
        self.input_validator = input_validator

    def calculate_real(self, value_text: str):
        """Calculate square root for real mode.

        Вычислить квадратный корень для режима действительных чисел.

        Args:
            value_text: Input value text

        Returns:
            CalculationResult object

        Raises:
            InvalidInputError: If input is invalid
        """
        if not value_text:
            raise InvalidInputError(self.translator.get("invalid_input"))

        # Normalize input (handle comma as decimal separator)
        value = self.input_validator.normalize_number_input(value_text)
        return self.calculator.calculate(value)

    def calculate_complex(self, real_text: str, imag_text: str):
        """Calculate square root for complex mode.

        Вычислить квадратный корень для режима комплексных чисел.

        Args:
            real_text: Real part text
            imag_text: Imaginary part text

        Returns:
            CalculationResult object
        """
        real_str = real_text or "0"
        imag_str = imag_text or "0"

        # Normalize inputs
        real_str = self.input_validator.normalize_number_input(real_str)
        imag_str = self.input_validator.normalize_number_input(imag_str)

        return self.calculator.calculate(None, real_str, imag_str)

    def format_error_message(self, error: Exception) -> str:
        """Format error message based on exception type.

        Форматировать сообщение об ошибке на основе типа исключения.

        Args:
            error: Exception that occurred

        Returns:
            Formatted error message
        """
        if isinstance(error, PrecisionError):
            if error.is_generic:
                return self.translator.get("precision_error_generic").format(
                    error.current_precision, error.required_precision
                )
            else:
                return self.translator.get("precision_too_low").format(
                    error.required_precision
                )
        elif isinstance(error, CalculatorError):
            return self.translator.get("calculation_error").format(str(error))
        else:
            return self.translator.get("calculation_error").format(str(error))

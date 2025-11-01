"""Input validator for number input handling.

Валидатор ввода для обработки числового ввода.
"""

import re
from ..core.calculator import InvalidInputError


class InputValidator:
    """Validates and normalizes number input.

    Проверяет и нормализует числовой ввод.
    """

    def __init__(self, translator):
        """Initialize input validator.

        Args:
            translator: Translator instance for error messages
        """
        self.translator = translator

    def normalize_number_input(self, text: str) -> str:
        """Normalize number input by replacing comma with dot and validating.

        Нормализовать числовой ввод, заменяя запятую на точку и проверяя.

        Args:
            text: Input text to normalize

        Returns:
            Normalized number string

        Raises:
            InvalidInputError: If input contains invalid characters
        """
        if not text:
            return text

        # Check for invalid characters before normalization
        # Allow: digits, comma OR dot, minus, plus, 'i' character, whitespace
        if not re.match(r"^[0-9.,\-+i\s]+$", text):
            raise InvalidInputError(
                self.translator.get("invalid_input")
                + ": "
                + self.translator.get("text_instead_of_numbers")
            )

        # Replace comma with dot for decimal separator
        normalized = text.replace(",", ".")

        # Additional validation: check for multiple decimal points
        self._validate_decimal_separators(normalized)

        return normalized

    def _validate_decimal_separators(self, normalized: str):
        """Validate that there aren't multiple decimal separators.

        Проверить, что нет нескольких десятичных разделителей.

        Args:
            normalized: Normalized input string

        Raises:
            InvalidInputError: If multiple decimal separators found
        """
        # For complex numbers, handle real and imaginary parts separately
        if "i" in normalized:
            # Remove 'i' and split by + or - (keeping the sign)
            temp = normalized.replace("i", "")
            # Split but keep delimiters
            parts = re.split(r"(\+|\-)", temp)
            # Reconstruct parts and check each number component
            current = ""
            for i, part in enumerate(parts):
                if part in ["+", "-"]:
                    if current and current.count(".") > 1:
                        raise InvalidInputError(
                            self.translator.get("invalid_input")
                            + ": Multiple decimal separators"
                        )
                    current = part if i == 0 else ""
                else:
                    current += part
                    if i == len(parts) - 1 and current and current.count(".") > 1:
                        raise InvalidInputError(
                            self.translator.get("invalid_input")
                            + ": Multiple decimal separators"
                        )
        else:
            # Simple number - just check for multiple dots
            if normalized.strip().count(".") > 1:
                raise InvalidInputError(
                    self.translator.get("invalid_input")
                    + ": Multiple decimal separators"
                )

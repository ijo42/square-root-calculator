"""Result formatter for displaying calculation results.

Форматирование результатов для отображения результатов вычислений.
"""

from ..core.calculator import CalculationResult


class ResultFormatter:
    """Formats calculation results as HTML for display.

    Форматирует результаты вычислений в HTML для отображения.
    """

    def __init__(self, translator, settings):
        """Initialize result formatter.

        Args:
            translator: Translator instance for i18n
            settings: Settings instance for display preferences
        """
        self.translator = translator
        self.settings = settings

    def build_result_html(self, result: CalculationResult) -> str:
        """Build HTML output for result display.

        Построить HTML-вывод для отображения результата.

        Args:
            result: Calculation result

        Returns:
            HTML string for display
        """
        html_parts = [
            "<div style='font-family: Courier New; font-size: 13px;'>",
            self._format_input_section(result),
            self._format_roots_section(result),
            self._format_representations_section(result),
            "</div>"
        ]
        return "".join(html_parts)

    def _format_input_section(self, result: CalculationResult) -> str:
        """Format input section of result display.

        Форматировать раздел ввода для отображения результата.

        Args:
            result: Calculation result

        Returns:
            HTML string for input section
        """
        input_label = self.translator.get('input_label')
        return (
            f"<p style='margin: 5px 0;'>"
            f"<b>{input_label}</b> {result.input_value}</p>"
        )

    def _format_roots_section(self, result: CalculationResult) -> str:
        """Format roots section of result display.

        Форматировать раздел корней для отображения результата.

        Args:
            result: Calculation result

        Returns:
            HTML string for roots section
        """
        roots_label = self.translator.get('roots_label')
        output = f"<p style='margin: 10px 0 5px 0;'><b>{roots_label}</b></p>"

        formatted_roots = result.get_formatted_roots()
        show_negative = self.settings.get("show_negative_roots", False)

        if len(formatted_roots) >= 1:
            output += self._format_root_line(
                result.input_value,
                formatted_roots[0],
                is_positive=True
            )

            if show_negative and len(formatted_roots) >= 2:
                output += self._format_root_line(
                    result.input_value,
                    formatted_roots[1],
                    is_positive=False
                )

        return output

    def _format_root_line(
        self, input_value: str, root_value: str, is_positive: bool
    ) -> str:
        """Format a single root line.

        Форматировать строку одного корня.

        Args:
            input_value: Original input value
            root_value: Formatted root value
            is_positive: Whether this is the positive root

        Returns:
            HTML string for root line
        """
        label_key = 'root_positive' if is_positive else 'root_negative'
        sign = '+' if is_positive else '-'
        label = self.translator.get(label_key)

        return (
            f"<p style='margin: 3px 0 3px 20px; color: #0066cc;'>"
            f"<b>{label}</b> {sign}√({input_value}) = {root_value}</p>"
        )

    def _format_representations_section(
        self, result: CalculationResult
    ) -> str:
        """Format representations section of result display.

        Форматировать раздел представлений для отображения результата.

        Args:
            result: Calculation result

        Returns:
            HTML string for representations section
        """
        representations = result.get_representations()
        if not representations:
            return ""

        if result.is_complex:
            return self._format_complex_representations(representations)
        else:
            return self._format_real_representations(representations)

    def _format_complex_representations(self, representations: dict) -> str:
        """Format complex number alternative forms.

        Форматировать альтернативные формы комплексных чисел.

        Args:
            representations: Dictionary of representations

        Returns:
            HTML string for complex representations
        """
        alt_forms = self.translator.get('alternative_forms')
        output = f"<p style='margin: 10px 0 5px 0;'><b>{alt_forms}</b></p>"

        if "polar" in representations:
            polar_label = self.translator.get('polar_form')
            output += (
                f"<p style='margin: 3px 0 3px 20px;'>"
                f"<b>{polar_label}</b> {representations['polar']}</p>"
            )

        if "exponential" in representations:
            exp_label = self.translator.get('exponential_form')
            output += (
                f"<p style='margin: 3px 0 3px 20px;'>"
                f"<b>{exp_label}</b> {representations['exponential']}</p>"
            )

        return output

    def _format_real_representations(self, representations: dict) -> str:
        """Format real number representations.

        Форматировать представления действительных чисел.

        Args:
            representations: Dictionary of representations

        Returns:
            HTML string for real representations
        """
        repr_label = self.translator.get('representations_label')
        output = f"<p style='margin: 10px 0 5px 0;'><b>{repr_label}</b></p>"

        repr_types = [
            ('decimal', 'decimal_repr'),
            ('scientific', 'scientific_repr'),
            ('fraction', 'fraction_repr'),
        ]

        for repr_key, label_key in repr_types:
            if repr_key in representations:
                label = self.translator.get(label_key)
                output += (
                    f"<p style='margin: 3px 0 3px 20px;'>"
                    f"<b>{label}</b> {representations[repr_key]}</p>"
                )

        return output

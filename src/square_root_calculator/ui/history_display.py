"""History display management for the UI.

Управление отображением истории для пользовательского интерфейса.
"""

from PyQt6.QtWidgets import QListWidgetItem
from ..core.calculator import CalculationResult
from ..core.constants import MAX_RESULT_DISPLAY_LENGTH, MAX_HISTORY_ENTRIES


class HistoryDisplayManager:
    """Manages history display in the UI.

    Управляет отображением истории в пользовательском интерфейсе.
    """

    def __init__(self, history_list_widget, history_manager, translator):
        """Initialize history display manager.

        Args:
            history_list_widget: QListWidget for displaying history
            history_manager: HistoryManager instance for data management
            translator: Translator instance for i18n
        """
        self.history_list = history_list_widget
        self.history = history_manager
        self.translator = translator

    @staticmethod
    def _parse_complex_input(input_str: str) -> tuple[str, str]:
        """Parse complex number string into real and imaginary parts.

        Разобрать строку комплексного числа на действительную и мнимую части.

        Args:
            input_str: Complex number string (e.g., "3+4i", "-3-4i")

        Returns:
            Tuple of (real_part, imaginary_part) as strings
        """
        if "i" not in input_str:
            # Just real part
            return input_str, "0"

        # Remove 'i' for parsing
        input_str = input_str.replace("i", "")

        # Handle different complex number formats
        # Format: "a+bi", "-a+bi", "a-bi", "-a-bi", "bi", "-bi"
        
        # Count minus signs to determine format
        minus_count = input_str.count("-")
        has_plus = "+" in input_str
        
        if has_plus:
            # Format: "a+bi" or "-a+bi"
            parts = input_str.split("+")
            real_part = parts[0] if parts[0] else "0"
            imag_part = parts[1] if len(parts) > 1 else "0"
        elif minus_count == 1 and not input_str.startswith("-"):
            # Format: "a-bi" (minus not at start)
            parts = input_str.split("-")
            real_part = parts[0] if parts[0] else "0"
            imag_part = "-" + parts[1] if len(parts) > 1 else "0"
        elif minus_count == 2 and input_str.startswith("-"):
            # Format: "-a-bi" (both negative)
            temp = input_str[1:]  # Remove leading minus
            parts = temp.split("-")
            real_part = "-" + parts[0] if parts[0] else "0"
            imag_part = "-" + parts[1] if len(parts) > 1 else "0"
        elif minus_count == 1 and input_str.startswith("-"):
            # Format: "-bi" (just negative imaginary)
            real_part = "0"
            imag_part = input_str
        else:
            # Just imaginary part without sign
            real_part = "0"
            imag_part = input_str

        return real_part, imag_part

    def add_to_history(self, result: CalculationResult):
        """Add calculation result to history.

        Добавить результат вычисления в историю.

        Args:
            result: CalculationResult to add to history
        """
        # Format the result for display (get first root formatted)
        formatted_roots = result.get_formatted_roots()
        result_text = formatted_roots[0] if formatted_roots else "N/A"

        # Extract real and imaginary parts for complex mode
        real_part = None
        imag_part = None
        if result.is_complex:
            real_part, imag_part = self._parse_complex_input(result.input_value)

        self.history.add_entry(
            input_value=str(result.input_value),
            result_text=result_text,
            precision=result.precision,
            is_complex=result.is_complex,
            real_part=real_part,
            imag_part=imag_part,
        )
        self.update_display()

    def update_display(self):
        """Update history display with latest entries.

        Обновить отображение истории последними записями.
        """
        self.history_list.clear()

        entries = self.history.get_entries(limit=MAX_HISTORY_ENTRIES)

        for entry in entries:
            # Only add "..." if the result is actually truncated
            result_display = entry.result_text[:MAX_RESULT_DISPLAY_LENGTH]
            if len(entry.result_text) > MAX_RESULT_DISPLAY_LENGTH:
                result_display += "..."
            item_text = f"√({entry.input_value}) ≈ {result_display}"

            item = QListWidgetItem(item_text)
            item.setData(1, entry)  # Store entry object for later retrieval
            self.history_list.addItem(item)

    def clear(self):
        """Clear all history.

        Очистить всю историю.
        """
        self.history.clear()
        self.update_display()

    def get_selected_entry(self):
        """Get the currently selected history entry.

        Получить выбранную запись истории.

        Returns:
            HistoryEntry or None if no selection
        """
        current_item = self.history_list.currentItem()
        if current_item:
            return current_item.data(1)
        return None

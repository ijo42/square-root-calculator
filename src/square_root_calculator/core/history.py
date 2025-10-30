"""History manager for storing calculation history.

Менеджер истории для хранения истории вычислений.
"""

from typing import List
from datetime import datetime


class HistoryEntry:
    """Single history entry.

    Одна запись истории.
    """

    def __init__(self, input_value: str, result_text: str, timestamp: datetime = None):
        """Initialize history entry.

        Инициализировать запись истории.

        Args:
            input_value: Input value/expression
                        Входное значение/выражение
            result_text: Formatted result text
                        Форматированный текст результата
            timestamp: When the calculation was performed
                      Когда было выполнено вычисление
        """
        self.input_value = input_value
        self.result_text = result_text
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> dict:
        """Convert to dictionary.

        Преобразовать в словарь.

        Returns:
            Dictionary representation
            Словарное представление
        """
        return {
            "input": self.input_value,
            "result": self.result_text,
            "timestamp": self.timestamp.isoformat(),
        }

    def __str__(self) -> str:
        """String representation.

        Строковое представление.

        Returns:
            Formatted string with timestamp and calculation
            Форматированная строка с меткой времени и вычислением
        """
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] √({self.input_value}) = {self.result_text}"


class HistoryManager:
    """Manages calculation history.

    Управляет историей вычислений.
    """

    def __init__(self, max_entries: int = 50):
        """Initialize history manager.

        Инициализировать менеджер истории.

        Args:
            max_entries: Maximum number of entries to keep
                        Максимальное количество записей для хранения
        """
        self.max_entries = max_entries
        self.entries: List[HistoryEntry] = []

    def add_entry(self, input_value: str, result_text: str):
        """Add a new entry to history.

        Добавить новую запись в историю.

        Args:
            input_value: Input value
                        Входное значение
            result_text: Result text
                        Текст результата
        """
        entry = HistoryEntry(input_value, result_text)
        self.entries.insert(0, entry)  # Add to beginning

        # Keep only max_entries
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[: self.max_entries]

    def get_entries(self, limit: int = None) -> List[HistoryEntry]:
        """Get history entries.

        Получить записи истории.

        Args:
            limit: Maximum number of entries to return
                  Максимальное количество возвращаемых записей

        Returns:
            List of history entries (most recent first)
            Список записей истории (сначала самые последние)
        """
        if limit is None:
            return self.entries.copy()
        return self.entries[:limit]

    def clear(self):
        """Clear all history.

        Очистить всю историю.
        """
        self.entries.clear()

    def is_empty(self) -> bool:
        """Check if history is empty.

        Проверить, пуста ли история.

        Returns:
            True if history is empty
            True, если история пуста
        """
        return len(self.entries) == 0

    def get_formatted_history(self, limit: int = 10) -> str:
        """Get formatted history as string.

        Получить форматированную историю в виде строки.

        Args:
            limit: Maximum number of entries to include
                  Максимальное количество включаемых записей

        Returns:
            Formatted history string
            Форматированная строка истории
        """
        if self.is_empty():
            return "No calculation history"

        entries = self.get_entries(limit)
        lines = [str(entry) for entry in entries]
        return "\n".join(lines)

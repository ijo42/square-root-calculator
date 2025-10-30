"""History display management for the UI.

Управление отображением истории для пользовательского интерфейса.
"""

from PyQt6.QtWidgets import QListWidgetItem
from ..core.calculator import CalculationResult


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
    
    def add_to_history(self, result: CalculationResult):
        """Add calculation result to history.
        
        Добавить результат вычисления в историю.
        
        Args:
            result: CalculationResult to add to history
        """
        self.history.add_entry(
            input_value=str(result.input_value),
            result_value=str(result.roots[0]) if result.roots else "N/A",
            precision=result.precision,
            is_complex=result.is_complex
        )
        self.update_display()
    
    def update_display(self):
        """Update history display with latest entries.
        
        Обновить отображение истории последними записями.
        """
        self.history_list.clear()
        
        entries = self.history.get_entries(limit=50)
        
        for entry in entries:
            mode = self.translator.get('complex_mode') if entry.is_complex else self.translator.get('real_mode')
            item_text = f"{entry.timestamp.strftime('%H:%M:%S')} | {mode} | √({entry.input_value}) ≈ {entry.result_value[:20]}..."
            
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

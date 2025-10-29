"""History manager for storing calculation history."""

from typing import List
from datetime import datetime


class HistoryEntry:
    """Single history entry."""
    
    def __init__(self, input_value: str, result_text: str, timestamp: datetime = None):
        """
        Initialize history entry.
        
        Args:
            input_value: Input value/expression
            result_text: Formatted result text
            timestamp: When the calculation was performed
        """
        self.input_value = input_value
        self.result_text = result_text
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'input': self.input_value,
            'result': self.result_text,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __str__(self) -> str:
        """String representation."""
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] √({self.input_value}) = {self.result_text}"


class HistoryManager:
    """Manages calculation history."""
    
    def __init__(self, max_entries: int = 50):
        """
        Initialize history manager.
        
        Args:
            max_entries: Maximum number of entries to keep
        """
        self.max_entries = max_entries
        self.entries: List[HistoryEntry] = []
    
    def add_entry(self, input_value: str, result_text: str):
        """Add a new entry to history."""
        entry = HistoryEntry(input_value, result_text)
        self.entries.insert(0, entry)  # Add to beginning
        
        # Keep only max_entries
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[:self.max_entries]
    
    def get_entries(self, limit: int = None) -> List[HistoryEntry]:
        """
        Get history entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of history entries (most recent first)
        """
        if limit is None:
            return self.entries.copy()
        return self.entries[:limit]
    
    def clear(self):
        """Clear all history."""
        self.entries.clear()
    
    def is_empty(self) -> bool:
        """Check if history is empty."""
        return len(self.entries) == 0
    
    def get_formatted_history(self, limit: int = 10) -> str:
        """
        Get formatted history as string.
        
        Args:
            limit: Maximum number of entries to include
            
        Returns:
            Formatted history string
        """
        if self.is_empty():
            return "No calculation history"
        
        entries = self.get_entries(limit)
        lines = [str(entry) for entry in entries]
        return '\n'.join(lines)

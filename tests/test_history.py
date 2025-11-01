"""Tests for history manager."""

import pytest  # noqa: F401
from square_root_calculator.core.history import (  # noqa: F401
    HistoryManager,
    HistoryEntry,
)


class TestHistoryEntry:
    """Test HistoryEntry class."""

    def test_create_entry(self):
        """Test creating a history entry."""
        entry = HistoryEntry("2", "1.414...")
        assert entry.input_value == "2"
        assert entry.result_text == "1.414..."
        assert entry.timestamp is not None

    def test_entry_to_dict(self):
        """Test converting entry to dictionary."""
        entry = HistoryEntry("2", "1.414...")
        d = entry.to_dict()
        assert d["input"] == "2"
        assert d["result"] == "1.414..."
        assert "timestamp" in d

    def test_entry_str(self):
        """Test string representation."""
        entry = HistoryEntry("2", "1.414...")
        s = str(entry)
        assert "√(2)" in s
        assert "1.414..." in s


class TestHistoryManager:
    """Test HistoryManager class."""

    def test_create_manager(self, history_manager):
        """Test creating history manager."""
        assert history_manager is not None
        assert history_manager.is_empty()

    def test_add_entry(self, history_manager):
        """Test adding entries."""
        history_manager.add_entry("2", "1.414...")
        assert not history_manager.is_empty()
        assert len(history_manager.get_entries()) == 1

    def test_add_multiple_entries(self, history_manager):
        """Test adding multiple entries."""
        for i in range(5):
            history_manager.add_entry(str(i), str(i * 2))
        assert len(history_manager.get_entries()) == 5

    def test_max_entries_limit(self, history_manager):
        """Test that max entries limit is respected."""
        # history_manager has max_entries=10
        for i in range(15):
            history_manager.add_entry(str(i), str(i * 2))
        assert len(history_manager.get_entries()) == 10

    def test_get_entries_with_limit(self, history_manager):
        """Test getting limited entries."""
        for i in range(10):
            history_manager.add_entry(str(i), str(i * 2))
        entries = history_manager.get_entries(limit=5)
        assert len(entries) == 5

    def test_clear_history(self, history_manager):
        """Test clearing history."""
        history_manager.add_entry("2", "1.414...")
        assert not history_manager.is_empty()
        history_manager.clear()
        assert history_manager.is_empty()

    def test_get_formatted_history(self, history_manager):
        """Test formatted history output."""
        history_manager.add_entry("2", "1.414...")
        history_manager.add_entry("4", "2")
        formatted = history_manager.get_formatted_history()
        assert "√(2)" in formatted
        assert "√(4)" in formatted

    def test_empty_formatted_history(self, history_manager):
        """Test formatted output when empty."""
        formatted = history_manager.get_formatted_history()
        assert "No calculation history" in formatted

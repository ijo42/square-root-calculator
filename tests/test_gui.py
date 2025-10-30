"""Tests for GUI components and main window."""

import pytest
from unittest.mock import MagicMock, patch
from square_root_calculator.core.calculator import CalculationResult
from square_root_calculator.core.history import HistoryManager
from square_root_calculator.ui.history_display import HistoryDisplayManager
from square_root_calculator.locales.translator import Translator


class TestHistoryDisplayManager:
    """Test HistoryDisplayManager class."""

    @pytest.fixture
    def mock_list_widget(self):
        """Create a mock QListWidget."""
        mock = MagicMock()
        mock.clear = MagicMock()
        mock.addItem = MagicMock()
        return mock

    @pytest.fixture
    def history_display(self, mock_list_widget):
        """Create HistoryDisplayManager instance."""
        history = HistoryManager(max_entries=10)
        translator = Translator("en")
        return HistoryDisplayManager(mock_list_widget, history, translator)

    def test_create_history_display(self, history_display):
        """Test creating history display manager."""
        assert history_display is not None
        assert history_display.history is not None
        assert history_display.translator is not None

    def test_add_to_history_with_result(self, history_display):
        """Test adding calculation result to history."""
        # Create a mock calculation result
        result = CalculationResult(
            input_value="4", roots=["2.0", "-2.0"], precision=10, is_complex=False
        )

        history_display.add_to_history(result)

        # Verify history was updated
        entries = history_display.history.get_entries()
        assert len(entries) == 1
        assert entries[0].input_value == "4"
        assert entries[0].result_text == "2.0"

    def test_add_to_history_no_roots(self, history_display):
        """Test adding result with no roots."""
        result = CalculationResult(
            input_value="invalid", roots=[], precision=10, is_complex=False
        )

        history_display.add_to_history(result)

        entries = history_display.history.get_entries()
        assert len(entries) == 1
        assert entries[0].result_text == "N/A"

    def test_update_display(self, history_display, mock_list_widget):
        """Test updating the display with history entries."""
        # Add some entries
        history_display.history.add_entry("2", "1.414...")
        history_display.history.add_entry("4", "2.0")

        history_display.update_display()

        # Verify clear was called
        mock_list_widget.clear.assert_called_once()

        # Verify items were added
        assert mock_list_widget.addItem.call_count == 2

    def test_update_display_truncates_long_results(
        self, history_display, mock_list_widget
    ):
        """Test that long results are truncated with ellipsis."""
        # Add entry with long result
        long_result = "1.41421356237309504880168872420969807856967187537694"
        history_display.history.add_entry("2", long_result)

        history_display.update_display()

        # Get the call arguments
        call_args = mock_list_widget.addItem.call_args_list
        assert len(call_args) == 1

        # Check that the item text contains "..." for truncation
        item = call_args[0][0][0]
        item_text = item.text()
        assert "..." in item_text
        assert len(long_result[:20]) < len(long_result)

    def test_update_display_no_truncation_short_results(
        self, history_display, mock_list_widget
    ):
        """Test that short results don't get unnecessary ellipsis."""
        # Add entry with short result
        short_result = "2.0"
        history_display.history.add_entry("4", short_result)

        history_display.update_display()

        # Get the call arguments
        call_args = mock_list_widget.addItem.call_args_list
        assert len(call_args) == 1

        # Check that the item text doesn't have trailing "..."
        item = call_args[0][0][0]
        item_text = item.text()
        # Short result shouldn't have ellipsis after it
        assert not item_text.endswith("2.0...")

    def test_clear_history(self, history_display, mock_list_widget):
        """Test clearing history."""
        history_display.history.add_entry("2", "1.414...")
        assert not history_display.history.is_empty()

        history_display.clear()

        assert history_display.history.is_empty()
        mock_list_widget.clear.assert_called()

    def test_get_selected_entry(self, history_display, mock_list_widget):
        """Test getting selected entry."""
        # Setup mock to return an item
        mock_item = MagicMock()
        mock_entry = MagicMock()
        mock_item.data.return_value = mock_entry
        mock_list_widget.currentItem.return_value = mock_item

        result = history_display.get_selected_entry()

        assert result == mock_entry
        mock_item.data.assert_called_once_with(1)

    def test_get_selected_entry_none(self, history_display, mock_list_widget):
        """Test getting selected entry when nothing selected."""
        mock_list_widget.currentItem.return_value = None

        result = history_display.get_selected_entry()

        assert result is None


class TestCalculationResultIntegration:
    """Test calculation result integration with history."""

    def test_calculation_result_to_history(self):
        """Test full flow from calculation to history."""
        from square_root_calculator.core.calculator import SquareRootCalculator

        calc = SquareRootCalculator(precision=10)
        result = calc.calculate(4)

        # Verify result structure
        assert result.input_value == "4"
        assert len(result.roots) == 2
        # result.roots contains tuples of (real, imag) Decimal values
        formatted_roots = result.get_formatted_roots()
        assert formatted_roots[0] == "2.0000000000"

        # Create history manager and add
        history = HistoryManager()
        history.add_entry(str(result.input_value), formatted_roots[0])

        # Verify it was added correctly
        entries = history.get_entries()
        assert len(entries) == 1
        assert entries[0].input_value == "4"
        assert entries[0].result_text == "2.0000000000"


class TestGUIErrorHandling:
    """Test error handling in GUI components."""

    def test_history_display_handles_empty_result(self):
        """Test that history display handles empty results gracefully."""
        mock_list = MagicMock()
        history = HistoryManager()
        translator = Translator("en")
        display = HistoryDisplayManager(mock_list, history, translator)

        # Create result with no roots
        result = CalculationResult(
            input_value="test", roots=[], precision=10, is_complex=False
        )

        # Should not raise exception
        display.add_to_history(result)

        entries = history.get_entries()
        assert len(entries) == 1
        assert entries[0].result_text == "N/A"

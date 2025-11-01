"""Widget helper functions for reducing code duplication.

Вспомогательные функции виджетов для уменьшения дублирования кода.
"""

from typing import Optional
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget
from PyQt6.QtCore import Qt


class WidgetHelpers:
    """Helper functions for common widget operations.

    Вспомогательные функции для общих операций с виджетами.
    """

    @staticmethod
    def create_label(
        text: str = "",
        font_size: int = 14,
        min_width: Optional[int] = None,
        bold: bool = False,
    ) -> QLabel:
        """Create a label with common styling.

        Создать метку с общим стилем.

        Args:
            text: Label text
            font_size: Font size in pixels
            min_width: Minimum width in pixels
            bold: Whether to make text bold

        Returns:
            Configured QLabel
        """
        label = QLabel(text)
        style_parts = [f"font-size: {font_size}px;"]
        if bold:
            style_parts.append("font-weight: bold;")
        label.setStyleSheet(" ".join(style_parts))

        if min_width:
            label.setMinimumWidth(min_width)

        return label

    @staticmethod
    def create_input_field(
        placeholder: str = "0",
        min_width: Optional[int] = None,
        max_width: Optional[int] = None,
        font_size: int = 14,
        align_right: bool = True,
    ) -> QLineEdit:
        """Create an input field with common styling.

        Создать поле ввода с общим стилем.

        Args:
            placeholder: Placeholder text
            min_width: Minimum width in pixels
            max_width: Maximum width in pixels
            font_size: Font size in pixels
            align_right: Whether to align text to the right

        Returns:
            Configured QLineEdit
        """
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setStyleSheet(f"font-size: {font_size}px;")

        if min_width:
            field.setMinimumWidth(min_width)
        if max_width:
            field.setMaximumWidth(max_width)
        if align_right:
            field.setAlignment(Qt.AlignmentFlag.AlignRight)

        return field

    @staticmethod
    def create_button(
        text: str = "",
        font_size: int = 16,
        padding: int = 10,
        callback: Optional[callable] = None,
    ) -> QPushButton:
        """Create a button with common styling.

        Создать кнопку с общим стилем.

        Args:
            text: Button text
            font_size: Font size in pixels
            padding: Padding in pixels
            callback: Click callback function

        Returns:
            Configured QPushButton
        """
        button = QPushButton(text)
        button.setStyleSheet(f"font-size: {font_size}px; padding: {padding}px;")

        if callback:
            button.clicked.connect(callback)

        return button

    @staticmethod
    def apply_monospace_style(
        widget: QWidget, font_size: int = 14, padding: int = 0
    ):
        """Apply monospace font styling to a widget.

        Применить моноширинный шрифт к виджету.

        Args:
            widget: Widget to style
            font_size: Font size in pixels
            padding: Padding in pixels
        """
        style_parts = [
            "font-family: 'Courier New', monospace;",
            f"font-size: {font_size}px;",
        ]
        if padding > 0:
            style_parts.append(f"padding: {padding}px;")

        widget.setStyleSheet(" ".join(style_parts))

    @staticmethod
    def set_widget_size(
        widget: QWidget,
        min_width: Optional[int] = None,
        max_width: Optional[int] = None,
        min_height: Optional[int] = None,
        max_height: Optional[int] = None,
    ):
        """Set widget size constraints.

        Установить ограничения размера виджета.

        Args:
            widget: Widget to configure
            min_width: Minimum width
            max_width: Maximum width
            min_height: Minimum height
            max_height: Maximum height
        """
        if min_width:
            widget.setMinimumWidth(min_width)
        if max_width:
            widget.setMaximumWidth(max_width)
        if min_height:
            widget.setMinimumHeight(min_height)
        if max_height:
            widget.setMaximumHeight(max_height)

    @staticmethod
    def block_signals_context(widget: QWidget):
        """Context manager to temporarily block widget signals.

        Контекстный менеджер для временной блокировки сигналов виджета.

        Args:
            widget: Widget to block signals for

        Returns:
            Context manager
        """

        class SignalBlocker:
            def __init__(self, w):
                self.widget = w

            def __enter__(self):
                self.widget.blockSignals(True)
                return self.widget

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.widget.blockSignals(False)

        return SignalBlocker(widget)


class StyleConstants:
    """Common style constants.

    Общие константы стилей.
    """

    FONT_SIZE_SMALL = 13
    FONT_SIZE_NORMAL = 14
    FONT_SIZE_LARGE = 16

    BUTTON_PADDING = 10
    TEXT_PADDING = 10

    MONOSPACE_FONT = "'Courier New', monospace"

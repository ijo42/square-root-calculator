"""Main GUI window for the Square Root Calculator.

Главное окно GUI для Калькулятора квадратного корня.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction, QDesktopServices

from ..core.calculator import (
    SquareRootCalculator,
    InvalidInputError,
    CalculatorError,
    PrecisionError,
    CalculationResult,
)
from ..core.history import HistoryManager
from ..core.update_checker import UpdateChecker
from ..core.settings import Settings
from ..core.constants import PRECISION_SLIDER_MAX
from ..locales.translator import Translator
from .. import __version__
from .update_thread import UpdateCheckThread
from .components import apply_theme_to_window, get_output_stylesheet
from .history_display import HistoryDisplayManager
from .menu_builder import MenuBuilder
from .result_formatter import ResultFormatter
from .input_validator import InputValidator
from .calculation_handler import CalculationHandler
from .ui_builder import UIBuilder
from .widget_helpers import WidgetHelpers


class MainWindow(QMainWindow):
    """Main application window.

    Главное окно приложения.
    """

    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self._manual_check = False

        # Initialize with settings
        lang = self.settings.get("language", "en")
        precision = self.settings.get("precision", 4)

        self.calculator = SquareRootCalculator(precision=precision)
        self.translator = Translator(lang)
        self.history = HistoryManager()
        self.update_checker = UpdateChecker(
            "ijo42", "square-root-calculator", __version__
        )

        # Initialize helper classes
        self.menu_builder = MenuBuilder(self)
        self.result_formatter = ResultFormatter(self.translator, self.settings)
        self.input_validator = InputValidator(self.translator)
        self.calculation_handler = CalculationHandler(
            self.calculator, self.translator, self.input_validator
        )
        self.ui_builder = UIBuilder(self)
        self.widget_helpers = WidgetHelpers()

        self.init_ui()

        # Initialize history display manager after UI is created
        self.history_display = HistoryDisplayManager(
            self.history_list, self.history, self.translator
        )

        # Apply theme after UI is created
        self.apply_theme(self.settings.get("theme", "light"))

        # Check for updates on startup (non-blocking)
        self.check_for_updates_async(manual=False)

    def init_ui(self):
        """Initialize the user interface using UIBuilder.

        Инициализировать пользовательский интерфейс с использованием UIBuilder.
        """
        self.ui_builder.setup_window()

        # Create menu bar
        self.create_menu_bar()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Top row: input tabs and precision control
        top_row_layout = self.ui_builder.create_top_row()
        layout.addLayout(top_row_layout)

        # Bottom: result display and history
        splitter = self.ui_builder.create_result_and_history_section()
        layout.addWidget(splitter)

        # Update all text
        self.update_ui_text()

    def toggle_exact_precision(self):
        """Toggle between slider and exact precision spinbox (mutually exclusive)."""
        show = self.show_exact_precision_action.isChecked()
        self.settings.set("show_exact_precision", show)
        self.ui_builder.toggle_precision_display(show)

    def create_menu_bar(self):
        """Create the menu bar using MenuBuilder.

        Создать строку меню с использованием MenuBuilder.
        """
        self.menu_builder.create_menu_bar()

    def update_ui_text(self):
        """Update all UI text based on current language."""
        self.setWindowTitle(self.translator.get("app_title"))

        # Update tab labels
        self.mode_tabs.setTabText(0, self.translator.get("mode_real"))
        self.mode_tabs.setTabText(1, self.translator.get("mode_complex"))

        # Update input labels
        self.input_label.setText(self.translator.get("input_label"))
        self.real_part_label.setText(self.translator.get("real_part_label"))
        self.imag_part_label.setText(self.translator.get("imag_part_label"))

        # Update precision labels
        self.precision_group.setTitle(self.translator.get("precision_control"))
        self.precision_label.setText(self.translator.get("precision_label"))
        self.spinbox_label.setText(self.translator.get("exact_value"))

        # Update buttons
        self.calculate_button.setText(self.translator.get("calculate_button"))
        self.clear_button.setText(self.translator.get("clear_button"))
        self.clear_history_button.setText(self.translator.get("clear_history_button"))

        # Update result and history groups
        self.result_group.setTitle(self.translator.get("result_label"))
        self.history_group.setTitle(self.translator.get("history_label"))

        # Update menu actions
        self.settings_menu.setTitle(self.translator.get("settings"))
        self.theme_menu.setTitle(self.translator.get("theme"))
        self.light_theme_action.setText(self.translator.get("theme_light"))
        self.dark_theme_action.setText(self.translator.get("theme_dark"))
        self.show_exact_precision_action.setText(
            self.translator.get("show_exact_precision")
        )
        self.show_negative_roots_action.setText(
            self.translator.get("show_negative_roots")
        )
        self.language_menu.setTitle(self.translator.get("language_menu"))
        self.help_menu.setTitle(self.translator.get("help"))
        self.user_manual_action.setText(self.translator.get("user_manual"))
        self.check_updates_action.setText(self.translator.get("check_updates"))
        self.about_action.setText(self.translator.get("about"))
        self.help_action.setText(self.translator.get("help"))

    def build_language_menu(self):
        """Build language menu with all available languages.

        Построить меню языков со всеми доступными языками.
        """
        # Clear existing actions
        self.language_menu.clear()
        self.language_actions.clear()

        # Get all available languages
        available_languages = self.translator.get_available_languages()
        current_language = self.settings.get("language", "en")

        # Create action for each language
        for lang_code, lang_name in available_languages:
            action = QAction(lang_name, self)
            action.setCheckable(True)
            action.setChecked(lang_code == current_language)
            # Use a lambda with default argument to capture lang_code
            action.triggered.connect(
                lambda checked, code=lang_code: self.change_language_from_menu(code)
            )
            self.language_menu.addAction(action)
            self.language_actions[lang_code] = action

        # Add separator and reload option
        self.language_menu.addSeparator()
        self.reload_translations_action = QAction(
            self.translator.get("reload_translations"), self
        )
        self.reload_translations_action.triggered.connect(self.reload_translations)
        self.language_menu.addAction(self.reload_translations_action)

    def change_language_from_menu(self, language_code):
        """Handle language change from menu."""
        self.translator.set_language(language_code)
        self.settings.set("language", language_code)

        # Update menu checkmarks
        for code, action in self.language_actions.items():
            action.setChecked(code == language_code)

        self.update_ui_text()

    def change_theme(self, theme):
        """Change application theme."""
        self.settings.set("theme", theme)
        self.light_theme_action.setChecked(theme == "light")
        self.dark_theme_action.setChecked(theme == "dark")
        self.apply_theme(theme)

    def apply_theme(self, theme):
        """Apply the specified theme."""
        self.app = QApplication.instance()
        apply_theme_to_window(self, theme)

        # Update output area stylesheet
        output_style = get_output_stylesheet(theme)
        self.result_display.setStyleSheet(output_style)

        # Update group box title colors based on theme
        title_color = "#ffffff" if theme == "dark" else "#0066cc"

        groupbox_style = f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 8px;
                color: {title_color};
            }}
        """

        self.precision_group.setStyleSheet(groupbox_style)
        self.result_group.setStyleSheet(groupbox_style)
        self.history_group.setStyleSheet(groupbox_style)

    def toggle_negative_roots(self):
        """Toggle showing negative roots."""
        show = self.show_negative_roots_action.isChecked()
        self.settings.set("show_negative_roots", show)
        # Will be used in display_result method

    def open_user_manual(self):
        """Open user manual in browser."""
        url = "https://github.com/ijo42/square-root-calculator/blob/master/README.md"
        QDesktopServices.openUrl(QUrl(url))

    def _sync_precision_widgets(self, value: int):
        """Synchronize all precision widgets to the same value.

        Синхронизировать все виджеты точности с одним значением.

        Args:
            value: Precision value to set
        """
        self.precision_value_label.setText(str(value))

        # Update slider if value is within its range
        if value <= PRECISION_SLIDER_MAX:
            with self.widget_helpers.block_signals_context(self.precision_slider):
                self.precision_slider.setValue(value)

        # Update spinbox
        with self.widget_helpers.block_signals_context(self.precision_spinbox):
            self.precision_spinbox.setValue(value)

    def precision_slider_changed(self, value):
        """Handle precision slider change."""
        self._sync_precision_widgets(value)
        try:
            self.calculator.set_precision(value)
            self.settings.set("precision", value)
        except Exception as e:
            self.show_error(str(e))

    def precision_spinbox_changed(self, value):
        """Handle precision spinbox change."""
        self._sync_precision_widgets(value)
        try:
            self.calculator.set_precision(value)
            self.settings.set("precision", value)
        except Exception as e:
            self.show_error(str(e))

    def calculate(self, from_history=False):
        """Perform calculation based on current mode using CalculationHandler.

        Выполнить вычисление на основе текущего режима с использованием CalculationHandler.

        Args:
            from_history: Whether this calculation is from history recall
        """
        try:
            # Check which tab is active
            if self.mode_tabs.currentIndex() == 0:
                # Real mode
                value = self.input_field.text().strip()
                result = self.calculation_handler.calculate_real(value)
            else:
                # Complex mode
                real_str = self.real_part_field.text().strip()
                imag_str = self.imag_part_field.text().strip()
                result = self.calculation_handler.calculate_complex(
                    real_str, imag_str
                )

            # Display unified result
            self.display_result(result)

            # Add to history only if not from history recall
            if not from_history:
                self.add_to_history(result)

        except (InvalidInputError, PrecisionError, CalculatorError, Exception) as e:
            error_msg = self.calculation_handler.format_error_message(e)
            self.show_error(error_msg)

    def display_result(self, result: CalculationResult):
        """Display calculation result in unified format using ResultFormatter.

        Отобразить результат вычисления в едином формате с использованием ResultFormatter.

        Args:
            result: Calculation result to display
        """
        self.result_display.clear()
        output = self.result_formatter.build_result_html(result)
        self.result_display.setHtml(output)

    def add_to_history(self, result: CalculationResult):
        """Add calculation to history."""
        self.history_display.add_to_history(result)

    def update_history_display(self):
        """Update history list widget."""
        self.history_display.update_display()

    def history_item_double_clicked(self, item):
        """Handle double-click on history item - recalculate with same parameters.

        Обработать двойной клик по элементу истории - пересчитать с теми же параметрами.

        Args:
            item: The list widget item that was double-clicked
        """
        entry = self.history_display.get_selected_entry()
        if not entry:
            return

        current_precision = self.calculator.precision

        # Apply history entry settings
        if entry.precision:
            self._apply_precision_from_history(entry.precision)

        self._set_input_from_history(entry)
        self.calculate(from_history=True)

        # Restore original precision if it was different
        if current_precision != entry.precision and entry.precision:
            self._apply_precision_from_history(current_precision)

    def _apply_precision_from_history(self, precision: int):
        """Apply precision value from history entry.

        Применить значение точности из записи истории.

        Args:
            precision: Precision value to apply
        """
        self.calculator.set_precision(precision)
        self._sync_precision_widgets(precision)

    def _set_input_from_history(self, entry):
        """Set input fields based on history entry.

        Установить поля ввода на основе записи истории.

        Args:
            entry: History entry to restore
        """
        if entry.is_complex:
            self.mode_tabs.setCurrentIndex(1)
            self.real_part_field.setText(entry.real_part or "0")
            self.imag_part_field.setText(entry.imag_part or "0")
        else:
            self.mode_tabs.setCurrentIndex(0)
            self.input_field.setText(entry.input_value)

    def clear_history(self):
        """Clear calculation history."""
        self.history_display.clear()

    def clear_fields(self):
        """Clear all input and output fields."""
        self.input_field.clear()
        self.real_part_field.clear()
        self.imag_part_field.clear()
        self.result_display.clear()

    def check_for_updates_async(self, manual=False):
        """Check for updates in background thread.

        Args:
            manual: Whether this is a manual check initiated by the user
        """
        self._manual_check = manual
        self.update_thread = UpdateCheckThread(self.update_checker)
        self.update_thread.update_checked.connect(self.on_update_checked)
        self.update_thread.start()

    def check_for_updates_manual(self):
        """Manually check for updates (user initiated)."""
        self.check_for_updates_async(manual=True)

    def on_update_checked(self, has_update: bool, version: str, error: str):
        """Handle update check result."""
        if error:
            # Only show error if manually checked
            if self._manual_check:
                QMessageBox.warning(
                    self,
                    self.translator.get("check_updates"),
                    self.translator.get("update_check_failed") + f"\n\n{error}",
                )
            self._manual_check = False
            return

        if has_update and version:
            # Check if user has skipped this version
            skipped_updates = self.settings.get("skipped_updates", [])
            if version in skipped_updates and not self._manual_check:
                # User previously skipped this version, don't show again
                self._manual_check = False
                return

            message = self.translator.get("update_message").format(version, __version__)

            # Create message box with custom buttons
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle(self.translator.get("update_available"))
            msgBox.setText(message)
            msgBox.setIcon(QMessageBox.Icon.Information)

            # Add Download and Skip buttons
            download_button = msgBox.addButton(
                self.translator.get("download_update"),
                QMessageBox.ButtonRole.AcceptRole,
            )
            skip_button = msgBox.addButton(
                self.translator.get("skip_update"), QMessageBox.ButtonRole.RejectRole
            )

            msgBox.exec()

            # If user clicked Download, open the download URL
            if msgBox.clickedButton() == download_button:
                download_url = self.translator.get("download_url")
                QDesktopServices.openUrl(QUrl(download_url))
            elif msgBox.clickedButton() == skip_button:
                # Save skipped version
                if version not in skipped_updates:
                    skipped_updates.append(version)
                    self.settings.set("skipped_updates", skipped_updates)
        elif self._manual_check:
            # Only show "no update" if manually checked
            QMessageBox.information(
                self,
                self.translator.get("check_updates"),
                self.translator.get("no_update"),
            )

        self._manual_check = False

    def reload_translations(self):
        """Reload custom translations from JSON files."""
        self.translator.reload_translations()
        self.build_language_menu()  # Rebuild menu to include any new languages
        self.update_ui_text()
        QMessageBox.information(
            self,
            self.translator.get("app_title"),
            self.translator.get("translations_reloaded"),
        )

    def show_error(self, message):
        """Display error message."""
        QMessageBox.critical(self, self.translator.get("error_title"), message)

    def show_about(self):
        """Show about dialog."""
        about_text = self.translator.get("about_text").format(__version__)
        QMessageBox.about(self, self.translator.get("about"), about_text)

    def show_help(self):
        """Show help dialog."""
        QMessageBox.information(
            self, self.translator.get("help"), self.translator.get("help_text")
        )


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

"""Main GUI window for the Square Root Calculator.

Главное окно GUI для Калькулятора квадратного корня.
"""

import sys
import webbrowser
from decimal import Decimal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTextEdit,
    QGroupBox, QRadioButton, QButtonGroup, QMessageBox, QMenuBar, QMenu,
    QSlider, QTabWidget, QListWidget, QSplitter
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QDesktopServices

from ..core.calculator import SquareRootCalculator, InvalidInputError, CalculatorError, CalculationResult
from ..core.history import HistoryManager
from ..core.update_checker import UpdateChecker
from ..core.settings import Settings
from ..locales.translator import Translator
from .. import __version__
from .update_thread import UpdateCheckThread
from .components import apply_theme_to_window, get_output_stylesheet
from .history_display import HistoryDisplayManager


class MainWindow(QMainWindow):
    """Main application window.
    
    Главное окно приложения.
    """
    
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        
        # Initialize with settings
        lang = self.settings.get('language', 'en')
        precision = self.settings.get('precision', 4)
        
        self.calculator = SquareRootCalculator(precision=precision)
        self.translator = Translator(lang)
        self.history = HistoryManager()
        self.update_checker = UpdateChecker('ijo42', 'square-root-calculator', __version__)
        
        self.init_ui()
        
        # Initialize history display manager after UI is created
        self.history_display = HistoryDisplayManager(
            self.history_list,
            self.history,
            self.translator
        )
        
        # Apply theme after UI is created
        self.apply_theme(self.settings.get('theme', 'light'))
        
        # Check for updates on startup (non-blocking)
        self.check_for_updates_async()
    
    def init_ui(self):
        """Initialize the user interface.
        
        Инициализировать пользовательский интерфейс.
        """
        self.setWindowTitle(self.translator.get('app_title'))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Mode selection using tabs (more convenient)
        self.mode_tabs = QTabWidget()
        layout.addWidget(self.mode_tabs)
        
        # Real numbers tab
        real_tab = QWidget()
        real_layout = QVBoxLayout()
        real_tab.setLayout(real_layout)
        
        real_input_layout = QHBoxLayout()
        self.input_label = QLabel()
        real_input_layout.addWidget(self.input_label)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('0')
        real_input_layout.addWidget(self.input_field)
        real_layout.addLayout(real_input_layout)
        real_layout.addStretch()
        
        self.mode_tabs.addTab(real_tab, '')  # Text will be set in update_ui_text
        
        # Complex numbers tab
        complex_tab = QWidget()
        complex_layout = QVBoxLayout()
        complex_tab.setLayout(complex_layout)
        
        real_row = QHBoxLayout()
        self.real_part_label = QLabel()
        real_row.addWidget(self.real_part_label)
        self.real_part_field = QLineEdit()
        self.real_part_field.setPlaceholderText('0')
        real_row.addWidget(self.real_part_field)
        complex_layout.addLayout(real_row)
        
        imag_row = QHBoxLayout()
        self.imag_part_label = QLabel()
        imag_row.addWidget(self.imag_part_label)
        self.imag_part_field = QLineEdit()
        self.imag_part_field.setPlaceholderText('0')
        imag_row.addWidget(self.imag_part_field)
        complex_layout.addLayout(imag_row)
        complex_layout.addStretch()
        
        self.mode_tabs.addTab(complex_tab, '')  # Text will be set in update_ui_text
        
        # Precision control with slider
        precision_group = QGroupBox()
        self.precision_group = precision_group
        precision_layout = QVBoxLayout()
        
        # Precision value display
        precision_value_layout = QHBoxLayout()
        self.precision_label = QLabel()
        precision_value_layout.addWidget(self.precision_label)
        initial_precision = self.settings.get('precision', 4)
        self.precision_value_label = QLabel(str(initial_precision))
        self.precision_value_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        precision_value_layout.addWidget(self.precision_value_label)
        precision_value_layout.addStretch()
        precision_layout.addLayout(precision_value_layout)
        
        # Slider for quick adjustment
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel('1'))
        self.precision_slider = QSlider(Qt.Orientation.Horizontal)
        self.precision_slider.setMinimum(1)
        self.precision_slider.setMaximum(200)
        self.precision_slider.setValue(initial_precision)
        self.precision_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.precision_slider.setTickInterval(20)
        self.precision_slider.valueChanged.connect(self.precision_slider_changed)
        slider_layout.addWidget(self.precision_slider)
        slider_layout.addWidget(QLabel('200'))
        precision_layout.addLayout(slider_layout)
        
        # SpinBox for precise input (hidden by default)
        self.spinbox_layout = QHBoxLayout()
        spinbox_label = QLabel()
        self.spinbox_label = spinbox_label
        self.spinbox_layout.addWidget(spinbox_label)
        self.precision_spinbox = QSpinBox()
        self.precision_spinbox.setMinimum(1)
        self.precision_spinbox.setMaximum(1000)
        self.precision_spinbox.setValue(initial_precision)
        self.precision_spinbox.valueChanged.connect(self.precision_spinbox_changed)
        self.spinbox_layout.addWidget(self.precision_spinbox)
        self.spinbox_layout.addStretch()
        precision_layout.addLayout(self.spinbox_layout)
        
        # Hide spinbox by default if setting is False
        if not self.settings.get('show_exact_precision', False):
            self.spinbox_label.hide()
            self.precision_spinbox.hide()
        
        precision_group.setLayout(precision_layout)
        layout.addWidget(precision_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton()
        self.calculate_button.setStyleSheet("font-size: 14px; padding: 8px;")
        self.calculate_button.clicked.connect(self.calculate)
        button_layout.addWidget(self.calculate_button)
        
        self.clear_button = QPushButton()
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # Splitter for result and history
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Result display with better formatting
        result_group = QGroupBox()
        self.result_group = result_group
        result_layout = QVBoxLayout()
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMinimumHeight(150)
        self.result_display.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background-color: #f5f5f5;
                padding: 10px;
            }
        """)
        result_layout.addWidget(self.result_display)
        
        result_group.setLayout(result_layout)
        splitter.addWidget(result_group)
        
        # History panel
        history_group = QGroupBox()
        self.history_group = history_group
        history_layout = QVBoxLayout()
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        self.history_list.itemClicked.connect(self.history_item_clicked)
        history_layout.addWidget(self.history_list)
        
        self.clear_history_button = QPushButton()
        self.clear_history_button.clicked.connect(self.clear_history)
        history_layout.addWidget(self.clear_history_button)
        
        history_group.setLayout(history_layout)
        splitter.addWidget(history_group)
        
        # Set initial splitter sizes (60% result, 40% history)
        splitter.setSizes([480, 320])
        
        # Update all text
        self.update_ui_text()
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # Settings menu
        self.settings_menu = menubar.addMenu('Settings')
        
        # Theme submenu
        self.theme_menu = QMenu('Theme', self)
        self.settings_menu.addMenu(self.theme_menu)
        
        self.light_theme_action = QAction('Light Theme', self)
        self.light_theme_action.setCheckable(True)
        self.light_theme_action.setChecked(self.settings.get('theme') == 'light')
        self.light_theme_action.triggered.connect(lambda: self.change_theme('light'))
        self.theme_menu.addAction(self.light_theme_action)
        
        self.dark_theme_action = QAction('Dark Theme', self)
        self.dark_theme_action.setCheckable(True)
        self.dark_theme_action.setChecked(self.settings.get('theme') == 'dark')
        self.dark_theme_action.triggered.connect(lambda: self.change_theme('dark'))
        self.theme_menu.addAction(self.dark_theme_action)
        
        self.settings_menu.addSeparator()
        
        # Show exact precision field toggle
        self.show_exact_precision_action = QAction('Show Exact Precision Field', self)
        self.show_exact_precision_action.setCheckable(True)
        self.show_exact_precision_action.setChecked(self.settings.get('show_exact_precision', False))
        self.show_exact_precision_action.triggered.connect(self.toggle_exact_precision)
        self.settings_menu.addAction(self.show_exact_precision_action)
        
        # Show negative roots toggle
        self.show_negative_roots_action = QAction('Show Negative Roots', self)
        self.show_negative_roots_action.setCheckable(True)
        self.show_negative_roots_action.setChecked(self.settings.get('show_negative_roots', False))
        self.show_negative_roots_action.triggered.connect(self.toggle_negative_roots)
        self.settings_menu.addAction(self.show_negative_roots_action)
        
        # Language menu
        self.language_menu = menubar.addMenu('Language')
        
        self.english_action = QAction('English', self)
        self.english_action.setCheckable(True)
        self.english_action.setChecked(self.settings.get('language') == 'en')
        self.english_action.triggered.connect(lambda: self.change_language_from_menu('en'))
        self.language_menu.addAction(self.english_action)
        
        self.russian_action = QAction('Русский', self)
        self.russian_action.setCheckable(True)
        self.russian_action.setChecked(self.settings.get('language') == 'ru')
        self.russian_action.triggered.connect(lambda: self.change_language_from_menu('ru'))
        self.language_menu.addAction(self.russian_action)
        
        # Help menu
        self.help_menu = menubar.addMenu('Help')
        
        self.user_manual_action = QAction('User Manual', self)
        self.user_manual_action.triggered.connect(self.open_user_manual)
        self.help_menu.addAction(self.user_manual_action)
        
        self.help_menu.addSeparator()
        
        self.check_updates_action = QAction('Check for Updates', self)
        self.check_updates_action.triggered.connect(self.check_for_updates_manual)
        self.help_menu.addAction(self.check_updates_action)
        
        self.help_menu.addSeparator()
        
        self.about_action = QAction('About', self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)
        
        self.help_action = QAction('Help', self)
        self.help_action.triggered.connect(self.show_help)
        self.help_menu.addAction(self.help_action)
    
    def update_ui_text(self):
        """Update all UI text based on current language."""
        self.setWindowTitle(self.translator.get('app_title'))
        
        # Update tab labels
        self.mode_tabs.setTabText(0, self.translator.get('mode_real'))
        self.mode_tabs.setTabText(1, self.translator.get('mode_complex'))
        
        # Update input labels
        self.input_label.setText(self.translator.get('input_label'))
        self.real_part_label.setText(self.translator.get('real_part_label'))
        self.imag_part_label.setText(self.translator.get('imag_part_label'))
        
        # Update precision labels
        self.precision_group.setTitle(self.translator.get('precision_control'))
        self.precision_label.setText(self.translator.get('precision_label'))
        self.spinbox_label.setText(self.translator.get('exact_value'))
        
        # Update buttons
        self.calculate_button.setText(self.translator.get('calculate_button'))
        self.clear_button.setText(self.translator.get('clear_button'))
        self.clear_history_button.setText(self.translator.get('clear_history_button'))
        
        # Update result and history groups
        self.result_group.setTitle(self.translator.get('result_label'))
        self.history_group.setTitle(self.translator.get('history_label'))
        
        # Update menu actions
        self.settings_menu.setTitle(self.translator.get('settings'))
        self.theme_menu.setTitle(self.translator.get('theme'))
        self.light_theme_action.setText(self.translator.get('theme_light'))
        self.dark_theme_action.setText(self.translator.get('theme_dark'))
        self.show_exact_precision_action.setText(self.translator.get('show_exact_precision'))
        self.show_negative_roots_action.setText(self.translator.get('show_negative_roots'))
        self.language_menu.setTitle(self.translator.get('language_menu'))
        self.help_menu.setTitle(self.translator.get('help'))
        self.user_manual_action.setText(self.translator.get('user_manual'))
        self.check_updates_action.setText(self.translator.get('check_updates'))
        self.about_action.setText(self.translator.get('about'))
        self.help_action.setText(self.translator.get('help'))
    
    def change_language_from_menu(self, language_code):
        """Handle language change from menu."""
        self.translator.set_language(language_code)
        self.settings.set('language', language_code)
        
        # Update menu checkmarks
        self.english_action.setChecked(language_code == 'en')
        self.russian_action.setChecked(language_code == 'ru')
        
        self.update_ui_text()
    
    def change_theme(self, theme):
        """Change application theme."""
        self.settings.set('theme', theme)
        self.light_theme_action.setChecked(theme == 'light')
        self.dark_theme_action.setChecked(theme == 'dark')
        self.apply_theme(theme)
    
    def apply_theme(self, theme):
        """Apply the specified theme."""
        self.app = QApplication.instance()
        apply_theme_to_window(self, theme)
        
        # Update output area stylesheet
        output_style = get_output_stylesheet(theme)
        self.output_text.setStyleSheet(output_style)
    
    def toggle_exact_precision(self):
        """Toggle visibility of exact precision spinbox."""
        show = self.show_exact_precision_action.isChecked()
        self.settings.set('show_exact_precision', show)
        
        if show:
            self.spinbox_label.show()
            self.precision_spinbox.show()
        else:
            self.spinbox_label.hide()
            self.precision_spinbox.hide()
    
    def toggle_negative_roots(self):
        """Toggle showing negative roots."""
        show = self.show_negative_roots_action.isChecked()
        self.settings.set('show_negative_roots', show)
        # Will be used in display_result method
    
    def open_user_manual(self):
        """Open user manual in browser."""
        url = "https://github.com/ijo42/square-root-calculator/blob/master/README.md"
        QDesktopServices.openUrl(QUrl(url))
    
    def precision_slider_changed(self, value):
        """Handle precision slider change."""
        self.precision_value_label.setText(str(value))
        self.precision_spinbox.blockSignals(True)
        self.precision_spinbox.setValue(value)
        self.precision_spinbox.blockSignals(False)
        try:
            self.calculator.set_precision(value)
            self.settings.set('precision', value)
        except Exception as e:
            self.show_error(str(e))
    
    def precision_spinbox_changed(self, value):
        """Handle precision spinbox change."""
        self.precision_value_label.setText(str(value))
        if value <= 200:
            self.precision_slider.blockSignals(True)
            self.precision_slider.setValue(value)
            self.precision_slider.blockSignals(False)
        try:
            self.calculator.set_precision(value)
            self.settings.set('precision', value)
        except Exception as e:
            self.show_error(str(e))
    
    def calculate(self):
        """Perform calculation based on current mode."""
        try:
            # Check which tab is active
            if self.mode_tabs.currentIndex() == 0:
                # Real mode
                value = self.input_field.text().strip()
                if not value:
                    raise InvalidInputError(self.translator.get('invalid_input'))
                result = self.calculator.calculate(value)
            else:
                # Complex mode
                real_str = self.real_part_field.text().strip() or '0'
                imag_str = self.imag_part_field.text().strip() or '0'
                result = self.calculator.calculate(None, real_str, imag_str)
            
            # Display unified result
            self.display_result(result)
            
            # Add to history
            self.add_to_history(result)
            
        except InvalidInputError as e:
            self.show_error(str(e))
        except CalculatorError as e:
            self.show_error(self.translator.get('calculation_error').format(str(e)))
        except Exception as e:
            self.show_error(self.translator.get('calculation_error').format(str(e)))
    
    def display_result(self, result: CalculationResult):
        """Display calculation result in unified format."""
        self.result_display.clear()
        
        # Build HTML output
        output = "<div style='font-family: Courier New; font-size: 12px;'>"
        
        # Input
        output += f"<p style='margin: 5px 0;'><b>{self.translator.get('input_label')}</b> {result.input_value}</p>"
        
        # Roots section
        output += f"<p style='margin: 10px 0 5px 0;'><b>{self.translator.get('roots_label')}</b></p>"
        
        formatted_roots = result.get_formatted_roots()
        show_negative = self.settings.get('show_negative_roots', False)
        
        if len(formatted_roots) >= 1:
            output += f"<p style='margin: 3px 0 3px 20px; color: #0066cc;'><b>{self.translator.get('root_positive')}</b> +√({result.input_value}) = {formatted_roots[0]}</p>"
            
            if show_negative and len(formatted_roots) >= 2:
                output += f"<p style='margin: 3px 0 3px 20px; color: #0066cc;'><b>{self.translator.get('root_negative')}</b> -√({result.input_value}) = {formatted_roots[1]}</p>"
        
        # Representations/Alternative forms
        representations = result.get_representations()
        if representations:
            if result.is_complex:
                output += f"<p style='margin: 10px 0 5px 0;'><b>{self.translator.get('alternative_forms')}</b></p>"
                
                if 'polar' in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('polar_form')}</b> {representations['polar']}</p>"
                
                if 'exponential' in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('exponential_form')}</b> {representations['exponential']}</p>"
            else:
                output += f"<p style='margin: 10px 0 5px 0;'><b>{self.translator.get('representations_label')}</b></p>"
                
                if 'decimal' in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('decimal_repr')}</b> {representations['decimal']}</p>"
                
                if 'scientific' in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('scientific_repr')}</b> {representations['scientific']}</p>"
                
                if 'fraction' in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('fraction_repr')}</b> {representations['fraction']}</p>"
        
        output += "</div>"
        
        self.result_display.setHtml(output)
    
    def add_to_history(self, result: CalculationResult):
        """Add calculation to history."""
        self.history_display.add_to_history(result)
    
    def update_history_display(self):
        """Update history list widget."""
        self.history_display.update_display()
    
    def history_item_clicked(self, item):
        """Handle click on history item - display result in result pane."""
        entry = self.history_display.get_selected_entry()
        
        if entry:
            # Display in result pane
            output = "<div style='font-family: Courier New; font-size: 12px;'>"
            output += f"<p style='margin: 5px 0;'><b>From History:</b></p>"
            output += f"<p style='margin: 5px 0;'><b>{self.translator.get('input_label')}</b> {entry.input_value}</p>"
            output += f"<p style='margin: 5px 0; color: #0066cc;'><b>Result:</b> {entry.result_value[:50]}...</p>"
            output += f"<p style='margin: 5px 0; font-size: 10px;'>Calculated: {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>"
            output += "</div>"
            
            self.result_display.setHtml(output)
    
    def clear_history(self):
        """Clear calculation history."""
        self.history_display.clear()
    
    def clear_fields(self):
        """Clear all input and output fields."""
        self.input_field.clear()
        self.real_part_field.clear()
        self.imag_part_field.clear()
        self.result_display.clear()
    
    def check_for_updates_async(self):
        """Check for updates in background thread."""
        self.update_thread = UpdateCheckThread(self.update_checker)
        self.update_thread.update_checked.connect(self.on_update_checked)
        self.update_thread.start()
    
    def check_for_updates_manual(self):
        """Manually check for updates (user initiated)."""
        self.check_for_updates_async()
    
    def on_update_checked(self, has_update: bool, version: str, error: str):
        """Handle update check result."""
        if error:
            # Only show error if manually checked
            return
        
        if has_update and version:
            message = self.translator.get('update_message').format(version, __version__)
            QMessageBox.information(
                self,
                self.translator.get('update_available'),
                message
            )
        elif hasattr(self, '_manual_check'):
            # Only show "no update" if manually checked
            QMessageBox.information(
                self,
                self.translator.get('check_updates'),
                self.translator.get('no_update')
            )
    
    def show_error(self, message):
        """Display error message."""
        QMessageBox.critical(
            self,
            self.translator.get('error_title'),
            message
        )
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            self.translator.get('about'),
            self.translator.get('about_text')
        )
    
    def show_help(self):
        """Show help dialog."""
        QMessageBox.information(
            self,
            self.translator.get('help'),
            self.translator.get('help_text')
        )


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

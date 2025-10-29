"""Main GUI window for the Square Root Calculator."""

import sys
from decimal import Decimal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTextEdit,
    QGroupBox, QRadioButton, QButtonGroup, QMessageBox, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from ..core.calculator import SquareRootCalculator, InvalidInputError, CalculatorError
from ..locales.translator import Translator


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.calculator = SquareRootCalculator()
        self.translator = Translator('en')
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(self.translator.get('app_title'))
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel()
        self.lang_label = lang_label
        lang_layout.addWidget(lang_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem('English', 'en')
        self.language_combo.addItem('Русский', 'ru')
        self.language_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)
        
        # Mode selection group
        mode_group = QGroupBox()
        self.mode_group = mode_group
        mode_layout = QVBoxLayout()
        
        self.mode_button_group = QButtonGroup()
        self.real_mode_radio = QRadioButton()
        self.complex_mode_radio = QRadioButton()
        
        self.real_mode_radio.setChecked(True)
        self.mode_button_group.addButton(self.real_mode_radio, 0)
        self.mode_button_group.addButton(self.complex_mode_radio, 1)
        
        mode_layout.addWidget(self.real_mode_radio)
        mode_layout.addWidget(self.complex_mode_radio)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        self.mode_button_group.buttonClicked.connect(self.mode_changed)
        
        # Input section for real numbers
        self.real_input_group = QGroupBox()
        real_input_layout = QVBoxLayout()
        
        real_input_row = QHBoxLayout()
        self.input_label = QLabel()
        real_input_row.addWidget(self.input_label)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('0')
        real_input_row.addWidget(self.input_field)
        real_input_layout.addLayout(real_input_row)
        
        self.real_input_group.setLayout(real_input_layout)
        layout.addWidget(self.real_input_group)
        
        # Input section for complex numbers
        self.complex_input_group = QGroupBox()
        complex_input_layout = QVBoxLayout()
        
        real_row = QHBoxLayout()
        self.real_part_label = QLabel()
        real_row.addWidget(self.real_part_label)
        self.real_part_field = QLineEdit()
        self.real_part_field.setPlaceholderText('0')
        real_row.addWidget(self.real_part_field)
        complex_input_layout.addLayout(real_row)
        
        imag_row = QHBoxLayout()
        self.imag_part_label = QLabel()
        imag_row.addWidget(self.imag_part_label)
        self.imag_part_field = QLineEdit()
        self.imag_part_field.setPlaceholderText('0')
        imag_row.addWidget(self.imag_part_field)
        complex_input_layout.addLayout(imag_row)
        
        self.complex_input_group.setLayout(complex_input_layout)
        self.complex_input_group.hide()
        layout.addWidget(self.complex_input_group)
        
        # Precision control
        precision_layout = QHBoxLayout()
        self.precision_label = QLabel()
        precision_layout.addWidget(self.precision_label)
        
        self.precision_spinbox = QSpinBox()
        self.precision_spinbox.setMinimum(1)
        self.precision_spinbox.setMaximum(1000)
        self.precision_spinbox.setValue(50)
        self.precision_spinbox.valueChanged.connect(self.precision_changed)
        precision_layout.addWidget(self.precision_spinbox)
        precision_layout.addStretch()
        layout.addLayout(precision_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton()
        self.calculate_button.clicked.connect(self.calculate)
        button_layout.addWidget(self.calculate_button)
        
        self.clear_button = QPushButton()
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # Result display
        result_group = QGroupBox()
        self.result_group = result_group
        result_layout = QVBoxLayout()
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMaximumHeight(150)
        result_layout.addWidget(self.result_display)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        # Update all text
        self.update_ui_text()
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # Help menu
        self.help_menu = menubar.addMenu('Help')
        
        self.about_action = QAction('About', self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)
        
        self.help_action = QAction('Help', self)
        self.help_action.triggered.connect(self.show_help)
        self.help_menu.addAction(self.help_action)
    
    def update_ui_text(self):
        """Update all UI text based on current language."""
        self.setWindowTitle(self.translator.get('app_title'))
        self.lang_label.setText(self.translator.get('language'))
        self.mode_group.setTitle(self.translator.get('mode_label'))
        self.real_mode_radio.setText(self.translator.get('mode_real'))
        self.complex_mode_radio.setText(self.translator.get('mode_complex'))
        self.input_label.setText(self.translator.get('input_label'))
        self.real_part_label.setText(self.translator.get('real_part_label'))
        self.imag_part_label.setText(self.translator.get('imag_part_label'))
        self.precision_label.setText(self.translator.get('precision_label'))
        self.calculate_button.setText(self.translator.get('calculate_button'))
        self.clear_button.setText(self.translator.get('clear_button'))
        self.result_group.setTitle(self.translator.get('result_label'))
        self.about_action.setText(self.translator.get('about'))
        self.help_action.setText(self.translator.get('help'))
    
    def change_language(self, index):
        """Handle language change."""
        language_code = self.language_combo.itemData(index)
        self.translator.set_language(language_code)
        self.update_ui_text()
    
    def mode_changed(self):
        """Handle mode change between real and complex."""
        if self.real_mode_radio.isChecked():
            self.real_input_group.show()
            self.complex_input_group.hide()
        else:
            self.real_input_group.hide()
            self.complex_input_group.show()
    
    def precision_changed(self, value):
        """Handle precision change."""
        try:
            self.calculator.set_precision(value)
        except Exception as e:
            self.show_error(str(e))
    
    def calculate(self):
        """Perform calculation based on current mode."""
        try:
            if self.real_mode_radio.isChecked():
                self.calculate_real()
            else:
                self.calculate_complex()
        except InvalidInputError as e:
            self.show_error(str(e))
        except CalculatorError as e:
            self.show_error(self.translator.get('calculation_error').format(str(e)))
        except Exception as e:
            self.show_error(self.translator.get('calculation_error').format(str(e)))
    
    def calculate_real(self):
        """Calculate square root of real number."""
        value = self.input_field.text().strip()
        if not value:
            raise InvalidInputError(self.translator.get('invalid_input'))
        
        result = self.calculator.sqrt_real(value)
        formatted = self.calculator.format_result(result)
        
        self.result_display.clear()
        self.result_display.append(f"√({value}) = {formatted}")
    
    def calculate_complex(self):
        """Calculate square root of complex number."""
        real_str = self.real_part_field.text().strip() or '0'
        imag_str = self.imag_part_field.text().strip() or '0'
        
        real_part, imag_part = self.calculator.sqrt_complex(real_str, imag_str)
        
        real_formatted = self.calculator.format_result(real_part)
        imag_formatted = self.calculator.format_result(imag_part)
        
        self.result_display.clear()
        
        # Format complex number nicely
        if imag_str == '0':
            input_str = real_str
        else:
            imag_display = imag_str if imag_str.startswith('-') else f"+{imag_str}"
            input_str = f"{real_str}{imag_display}i"
        
        # Format result
        if imag_part < 0:
            result_str = f"{real_formatted}{imag_formatted}i"
        else:
            result_str = f"{real_formatted}+{imag_formatted}i"
        
        self.result_display.append(f"√({input_str}) = {result_str}")
    
    def clear_fields(self):
        """Clear all input and output fields."""
        self.input_field.clear()
        self.real_part_field.clear()
        self.imag_part_field.clear()
        self.result_display.clear()
    
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

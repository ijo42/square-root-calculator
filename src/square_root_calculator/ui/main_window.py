"""Main GUI window for the Square Root Calculator.

Главное окно GUI для Калькулятора квадратного корня.
"""

import re
import sys
import webbrowser
from decimal import Decimal
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QSpinBox,
    QTextEdit,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QMenuBar,
    QMenu,
    QSlider,
    QTabWidget,
    QListWidget,
    QSplitter,
)
from PyQt6.QtCore import Qt, QUrl
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
from ..core.constants import (
    LABEL_MIN_WIDTH,
    INPUT_MIN_WIDTH,
    PRECISION_GROUP_MIN_WIDTH,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    PRECISION_SLIDER_MIN,
    PRECISION_SLIDER_MAX,
    PRECISION_SPINBOX_MIN,
    PRECISION_SPINBOX_MAX,
    PRECISION_SLIDER_TICK_INTERVAL,
    DEFAULT_PRECISION,
    SPLITTER_RESULT_SIZE,
    SPLITTER_HISTORY_SIZE,
)
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
        """Initialize the user interface.

        Инициализировать пользовательский интерфейс.
        """
        self.setWindowTitle(self.translator.get("app_title"))
        self.setMinimumWidth(WINDOW_MIN_WIDTH)
        self.setMinimumHeight(WINDOW_MIN_HEIGHT)

        # Create menu bar
        self.create_menu_bar()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Top row: input tabs and precision control
        top_row_layout = self._create_top_row()
        layout.addLayout(top_row_layout)

        # Bottom: result display and history
        splitter = self._create_result_and_history_section()
        layout.addWidget(splitter)

        # Update all text
        self.update_ui_text()

    def _create_top_row(self) -> QHBoxLayout:
        """Create top row with input tabs and precision control.

        Создать верхний ряд с вкладками ввода и управлением точностью.

        Returns:
            Horizontal layout with mode tabs and precision control
        """
        top_row_layout = QHBoxLayout()

        # Left side: Mode tabs with input fields
        input_container = self._create_input_tabs()
        top_row_layout.addWidget(input_container, stretch=3)

        # Right side: Precision control
        precision_group = self._create_precision_control()
        top_row_layout.addWidget(precision_group, stretch=2)

        return top_row_layout

    def _create_input_tabs(self) -> QWidget:
        """Create input tabs container with real and complex mode tabs.

        Создать контейнер вкладок ввода с вкладками реального и комплексного режимов.

        Returns:
            Widget containing mode tabs
        """
        # Mode selection using tabs
        self.mode_tabs = QTabWidget()

        # Container for tabs and buttons
        input_container = QWidget()
        input_container_layout = QVBoxLayout()
        input_container_layout.setContentsMargins(0, 0, 0, 0)
        input_container.setLayout(input_container_layout)
        input_container_layout.addWidget(self.mode_tabs)

        # Create tabs
        self._create_real_numbers_tab()
        self._create_complex_numbers_tab()

        # Buttons
        button_layout = self._create_buttons()
        input_container_layout.addLayout(button_layout)

        return input_container

    def _create_real_numbers_tab(self):
        """Create real numbers input tab.

        Создать вкладку ввода действительных чисел.
        """
        real_tab = QWidget()
        real_layout = QVBoxLayout()
        real_tab.setLayout(real_layout)

        real_input_layout = QHBoxLayout()
        self.input_label = QLabel()
        self.input_label.setMinimumWidth(LABEL_MIN_WIDTH)
        self.input_label.setStyleSheet("font-size: 14px;")
        real_input_layout.addWidget(self.input_label)
        real_input_layout.addStretch()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("0")
        self.input_field.setMinimumWidth(INPUT_MIN_WIDTH)
        self.input_field.setMaximumWidth(INPUT_MIN_WIDTH)
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.input_field.setStyleSheet("font-size: 14px;")
        real_input_layout.addWidget(self.input_field)
        
        real_layout.addLayout(real_input_layout)
        real_layout.addStretch()

        self.mode_tabs.addTab(real_tab, "")  # Text will be set in update_ui_text

    def _create_complex_numbers_tab(self):
        """Create complex numbers input tab.

        Создать вкладку ввода комплексных чисел.
        """
        complex_tab = QWidget()
        complex_layout = QVBoxLayout()
        complex_tab.setLayout(complex_layout)

        # Real part
        real_row = QHBoxLayout()
        self.real_part_label = QLabel()
        self.real_part_label.setMinimumWidth(LABEL_MIN_WIDTH)
        self.real_part_label.setStyleSheet("font-size: 14px;")
        real_row.addWidget(self.real_part_label)
        real_row.addStretch()
        
        self.real_part_field = QLineEdit()
        self.real_part_field.setPlaceholderText("0")
        self.real_part_field.setMinimumWidth(INPUT_MIN_WIDTH)
        self.real_part_field.setMaximumWidth(INPUT_MIN_WIDTH)
        self.real_part_field.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.real_part_field.setStyleSheet("font-size: 14px;")
        real_row.addWidget(self.real_part_field)
        complex_layout.addLayout(real_row)

        # Imaginary part
        imag_row = QHBoxLayout()
        self.imag_part_label = QLabel()
        self.imag_part_label.setMinimumWidth(LABEL_MIN_WIDTH)
        self.imag_part_label.setStyleSheet("font-size: 14px;")
        imag_row.addWidget(self.imag_part_label)
        imag_row.addStretch()
        
        self.imag_part_field = QLineEdit()
        self.imag_part_field.setPlaceholderText("0")
        self.imag_part_field.setMinimumWidth(INPUT_MIN_WIDTH)
        self.imag_part_field.setMaximumWidth(INPUT_MIN_WIDTH)
        self.imag_part_field.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.imag_part_field.setStyleSheet("font-size: 14px;")
        imag_row.addWidget(self.imag_part_field)
        complex_layout.addLayout(imag_row)
        complex_layout.addStretch()

        self.mode_tabs.addTab(complex_tab, "")  # Text will be set in update_ui_text

    def _create_buttons(self) -> QHBoxLayout:
        """Create calculate and clear buttons.

        Создать кнопки вычисления и очистки.

        Returns:
            Horizontal layout with buttons
        """
        button_layout = QHBoxLayout()
        
        self.calculate_button = QPushButton()
        self.calculate_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.calculate_button.clicked.connect(self.calculate)
        button_layout.addWidget(self.calculate_button)

        self.clear_button = QPushButton()
        self.clear_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)

        return button_layout

    def _create_precision_control(self) -> QGroupBox:
        """Create precision control group with slider and spinbox.

        Создать группу управления точностью со слайдером и спинбоксом.

        Returns:
            QGroupBox containing precision controls
        """
        precision_group = QGroupBox()
        self.precision_group = precision_group
        precision_group.setMinimumWidth(PRECISION_GROUP_MIN_WIDTH)
        precision_layout = QVBoxLayout()

        initial_precision = self.settings.get("precision", DEFAULT_PRECISION)

        # Precision value display
        precision_value_layout = QHBoxLayout()
        self.precision_label = QLabel()
        self.precision_label.setStyleSheet("font-size: 14px;")
        precision_value_layout.addWidget(self.precision_label)
        self.precision_value_label = QLabel(str(initial_precision))
        self.precision_value_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        precision_value_layout.addWidget(self.precision_value_label)
        precision_value_layout.addStretch()
        self.precision_value_layout = precision_value_layout
        precision_layout.addLayout(precision_value_layout)

        # Slider for quick adjustment
        self.slider_layout = QHBoxLayout()
        self.slider_min_label = QLabel(str(PRECISION_SLIDER_MIN))
        self.slider_layout.addWidget(self.slider_min_label)
        self.precision_slider = QSlider(Qt.Orientation.Horizontal)
        self.precision_slider.setMinimum(PRECISION_SLIDER_MIN)
        self.precision_slider.setMaximum(PRECISION_SLIDER_MAX)
        self.precision_slider.setValue(initial_precision)
        self.precision_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.precision_slider.setTickInterval(PRECISION_SLIDER_TICK_INTERVAL)
        self.precision_slider.valueChanged.connect(self.precision_slider_changed)
        self.slider_layout.addWidget(self.precision_slider)
        self.slider_max_label = QLabel(str(PRECISION_SLIDER_MAX))
        self.slider_max_label.setStyleSheet("font-size: 13px;")
        self.slider_layout.addWidget(self.slider_max_label)
        precision_layout.addLayout(self.slider_layout)

        # SpinBox for precise input
        self.spinbox_layout = QHBoxLayout()
        spinbox_label = QLabel()
        spinbox_label.setStyleSheet("font-size: 14px;")
        self.spinbox_label = spinbox_label
        self.spinbox_layout.addWidget(spinbox_label)
        self.precision_spinbox = QSpinBox()
        self.precision_spinbox.setMinimum(PRECISION_SPINBOX_MIN)
        self.precision_spinbox.setMaximum(PRECISION_SPINBOX_MAX)
        self.precision_spinbox.setValue(initial_precision)
        self.precision_spinbox.setStyleSheet("font-size: 14px;")
        self.precision_spinbox.valueChanged.connect(self.precision_spinbox_changed)
        self.spinbox_layout.addWidget(self.precision_spinbox)
        self.spinbox_layout.addStretch()
        precision_layout.addLayout(self.spinbox_layout)

        # Show either slider or spinbox (mutually exclusive)
        show_exact = self.settings.get("show_exact_precision", False)
        self._toggle_precision_display(show_exact)

        precision_group.setLayout(precision_layout)
        return precision_group

    def _toggle_precision_display(self, show_exact: bool):
        """Toggle between slider and exact precision spinbox display.

        Переключить отображение между слайдером и точным спинбоксом.

        Args:
            show_exact: True to show spinbox, False to show slider
        """
        if show_exact:
            # Show spinbox, hide slider and precision label/value
            self.spinbox_label.show()
            self.precision_spinbox.show()
            self.precision_label.hide()
            self.precision_value_label.hide()
            self.slider_min_label.hide()
            self.precision_slider.hide()
            self.slider_max_label.hide()
        else:
            # Show slider and precision label/value, hide spinbox
            self.spinbox_label.hide()
            self.precision_spinbox.hide()
            self.precision_label.show()
            self.precision_value_label.show()
            self.slider_min_label.show()
            self.precision_slider.show()
            self.slider_max_label.show()

    def _create_result_and_history_section(self) -> QSplitter:
        """Create result display and history panel.

        Создать панель отображения результатов и истории.

        Returns:
            QSplitter containing result and history sections
        """
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Result display
        result_group = QGroupBox()
        self.result_group = result_group
        result_layout = QVBoxLayout()

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMinimumHeight(150)
        self.result_display.setStyleSheet(
            """
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                padding: 10px;
            }
        """
        )
        result_layout.addWidget(self.result_display)
        result_group.setLayout(result_layout)
        splitter.addWidget(result_group)

        # History panel
        history_group = QGroupBox()
        self.history_group = history_group
        history_layout = QVBoxLayout()

        self.history_list = QListWidget()
        self.history_list.setStyleSheet(
            """
            QListWidget {
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
        """
        )
        self.history_list.itemDoubleClicked.connect(self.history_item_double_clicked)
        history_layout.addWidget(self.history_list)

        self.clear_history_button = QPushButton()
        self.clear_history_button.clicked.connect(self.clear_history)
        history_layout.addWidget(self.clear_history_button)

        history_group.setLayout(history_layout)
        splitter.addWidget(history_group)

        # Set initial splitter sizes
        splitter.setSizes([SPLITTER_RESULT_SIZE, SPLITTER_HISTORY_SIZE])

        return splitter

    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()

        # Settings menu
        self.settings_menu = menubar.addMenu("Settings")

        # Theme submenu
        self.theme_menu = QMenu("Theme", self)
        self.settings_menu.addMenu(self.theme_menu)

        self.light_theme_action = QAction("Light Theme", self)
        self.light_theme_action.setCheckable(True)
        self.light_theme_action.setChecked(self.settings.get("theme") == "light")
        self.light_theme_action.triggered.connect(lambda: self.change_theme("light"))
        self.theme_menu.addAction(self.light_theme_action)

        self.dark_theme_action = QAction("Dark Theme", self)
        self.dark_theme_action.setCheckable(True)
        self.dark_theme_action.setChecked(self.settings.get("theme") == "dark")
        self.dark_theme_action.triggered.connect(lambda: self.change_theme("dark"))
        self.theme_menu.addAction(self.dark_theme_action)

        self.settings_menu.addSeparator()

        # Show exact precision field toggle
        self.show_exact_precision_action = QAction("Show Exact Precision Field", self)
        self.show_exact_precision_action.setCheckable(True)
        self.show_exact_precision_action.setChecked(
            self.settings.get("show_exact_precision", False)
        )
        self.show_exact_precision_action.triggered.connect(self.toggle_exact_precision)
        self.settings_menu.addAction(self.show_exact_precision_action)

        # Show negative roots toggle
        self.show_negative_roots_action = QAction("Show Negative Roots", self)
        self.show_negative_roots_action.setCheckable(True)
        self.show_negative_roots_action.setChecked(
            self.settings.get("show_negative_roots", False)
        )
        self.show_negative_roots_action.triggered.connect(self.toggle_negative_roots)
        self.settings_menu.addAction(self.show_negative_roots_action)

        # Language menu
        self.language_menu = menubar.addMenu("Language")
        self.language_actions = {}
        self.build_language_menu()

        # Help menu
        self.help_menu = menubar.addMenu("Help")

        self.user_manual_action = QAction("User Manual", self)
        self.user_manual_action.triggered.connect(self.open_user_manual)
        self.help_menu.addAction(self.user_manual_action)

        self.help_menu.addSeparator()

        self.check_updates_action = QAction("Check for Updates", self)
        self.check_updates_action.triggered.connect(self.check_for_updates_manual)
        self.help_menu.addAction(self.check_updates_action)

        self.help_menu.addSeparator()

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)

        self.help_action = QAction("Help", self)
        self.help_action.triggered.connect(self.show_help)
        self.help_menu.addAction(self.help_action)

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

    def toggle_exact_precision(self):
        """Toggle between slider and exact precision spinbox (mutually exclusive)."""
        show = self.show_exact_precision_action.isChecked()
        self.settings.set("show_exact_precision", show)
        self._toggle_precision_display(show)

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
            self.precision_slider.blockSignals(True)
            self.precision_slider.setValue(value)
            self.precision_slider.blockSignals(False)
        
        # Update spinbox
        self.precision_spinbox.blockSignals(True)
        self.precision_spinbox.setValue(value)
        self.precision_spinbox.blockSignals(False)

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

    def normalize_number_input(self, text: str) -> str:
        """Normalize number input by replacing comma with dot and validating.

        Нормализовать числовой ввод, заменяя запятую на точку и проверяя.

        Args:
            text: Input text to normalize

        Returns:
            Normalized number string

        Raises:
            InvalidInputError: If input contains invalid characters
        """
        if not text:
            return text

        # Check for invalid characters before normalization
        # Allow: digits, comma OR dot (but not both in validation), minus, plus, 'i' character, and whitespace
        if not re.match(r"^[0-9.,\-+i\s]+$", text):
            raise InvalidInputError(
                self.translator.get("invalid_input")
                + ": "
                + self.translator.get("text_instead_of_numbers")
            )

        # Replace comma with dot for decimal separator
        normalized = text.replace(",", ".")

        # Additional validation: check for multiple decimal points in a single number
        # For complex numbers, handle real and imaginary parts separately
        if "i" in normalized:
            # Remove 'i' and split by + or - (keeping the sign)
            temp = normalized.replace("i", "")
            # Split but keep delimiters
            parts = re.split(r"(\+|\-)", temp)
            # Reconstruct parts and check each number component
            current = ""
            for i, part in enumerate(parts):
                if part in ["+", "-"]:
                    if current and current.count(".") > 1:
                        raise InvalidInputError(
                            self.translator.get("invalid_input")
                            + ": Multiple decimal separators"
                        )
                    current = part if i == 0 else ""
                else:
                    current += part
                    if i == len(parts) - 1 and current and current.count(".") > 1:
                        raise InvalidInputError(
                            self.translator.get("invalid_input")
                            + ": Multiple decimal separators"
                        )
        else:
            # Simple number - just check for multiple dots
            if normalized.strip().count(".") > 1:
                raise InvalidInputError(
                    self.translator.get("invalid_input")
                    + ": Multiple decimal separators"
                )

        return normalized

    def calculate(self, from_history=False):
        """Perform calculation based on current mode.

        Args:
            from_history: Whether this calculation is from history recall (don't add to history again)
        """
        try:
            # Check which tab is active
            if self.mode_tabs.currentIndex() == 0:
                # Real mode
                value = self.input_field.text().strip()
                if not value:
                    raise InvalidInputError(self.translator.get("invalid_input"))
                # Normalize input (handle comma as decimal separator)
                value = self.normalize_number_input(value)
                result = self.calculator.calculate(value)
            else:
                # Complex mode
                real_str = self.real_part_field.text().strip() or "0"
                imag_str = self.imag_part_field.text().strip() or "0"
                # Normalize inputs
                real_str = self.normalize_number_input(real_str)
                imag_str = self.normalize_number_input(imag_str)
                result = self.calculator.calculate(None, real_str, imag_str)

            # Display unified result
            self.display_result(result)

            # Add to history only if not from history recall
            if not from_history:
                self.add_to_history(result)

        except InvalidInputError as e:
            self.show_error(str(e))
        except PrecisionError as e:
            # Handle precision errors with proper translation
            if e.is_generic:
                error_msg = self.translator.get("precision_error_generic").format(
                    e.current_precision, e.required_precision
                )
            else:
                error_msg = self.translator.get("precision_too_low").format(
                    e.required_precision
                )
            self.show_error(error_msg)
        except CalculatorError as e:
            self.show_error(self.translator.get("calculation_error").format(str(e)))
        except Exception as e:
            self.show_error(self.translator.get("calculation_error").format(str(e)))

    def display_result(self, result: CalculationResult):
        """Display calculation result in unified format."""
        self.result_display.clear()

        # Build HTML output
        output = "<div style='font-family: Courier New; font-size: 13px;'>"

        # Input
        output += f"<p style='margin: 5px 0;'><b>{self.translator.get('input_label')}</b> {result.input_value}</p>"

        # Roots section
        output += f"<p style='margin: 10px 0 5px 0;'><b>{self.translator.get('roots_label')}</b></p>"

        formatted_roots = result.get_formatted_roots()
        show_negative = self.settings.get("show_negative_roots", False)

        if len(formatted_roots) >= 1:
            output += f"<p style='margin: 3px 0 3px 20px; color: #0066cc;'><b>{self.translator.get('root_positive')}</b> +√({result.input_value}) = {formatted_roots[0]}</p>"

            if show_negative and len(formatted_roots) >= 2:
                output += f"<p style='margin: 3px 0 3px 20px; color: #0066cc;'><b>{self.translator.get('root_negative')}</b> -√({result.input_value}) = {formatted_roots[1]}</p>"

        # Representations/Alternative forms
        representations = result.get_representations()
        if representations:
            if result.is_complex:
                output += f"<p style='margin: 10px 0 5px 0;'><b>{self.translator.get('alternative_forms')}</b></p>"

                if "polar" in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('polar_form')}</b> {representations['polar']}</p>"

                if "exponential" in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('exponential_form')}</b> {representations['exponential']}</p>"
            else:
                output += f"<p style='margin: 10px 0 5px 0;'><b>{self.translator.get('representations_label')}</b></p>"

                if "decimal" in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('decimal_repr')}</b> {representations['decimal']}</p>"

                if "scientific" in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('scientific_repr')}</b> {representations['scientific']}</p>"

                if "fraction" in representations:
                    output += f"<p style='margin: 3px 0 3px 20px;'><b>{self.translator.get('fraction_repr')}</b> {representations['fraction']}</p>"

        output += "</div>"

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
        """
        entry = self.history_display.get_selected_entry()

        if entry:
            # Save current precision
            current_precision = self.calculator.precision

            # Set precision from history entry
            if entry.precision:
                self.calculator.set_precision(entry.precision)
                self.precision_value_label.setText(str(entry.precision))
                if entry.precision <= 200:
                    self.precision_slider.blockSignals(True)
                    self.precision_slider.setValue(entry.precision)
                    self.precision_slider.blockSignals(False)
                self.precision_spinbox.blockSignals(True)
                self.precision_spinbox.setValue(entry.precision)
                self.precision_spinbox.blockSignals(False)

            # Set mode and input fields from history entry
            if entry.is_complex:
                # Switch to complex mode
                self.mode_tabs.setCurrentIndex(1)
                # Set real and imaginary parts
                self.real_part_field.setText(entry.real_part or "0")
                self.imag_part_field.setText(entry.imag_part or "0")
            else:
                # Switch to real mode
                self.mode_tabs.setCurrentIndex(0)
                # Set input value
                self.input_field.setText(entry.input_value)

            # Perform calculation (from_history=True to not add to history again)
            self.calculate(from_history=True)

            # Restore precision if it was different
            if current_precision != entry.precision and entry.precision:
                self.calculator.set_precision(current_precision)
                self.precision_value_label.setText(str(current_precision))
                if current_precision <= 200:
                    self.precision_slider.blockSignals(True)
                    self.precision_slider.setValue(current_precision)
                    self.precision_slider.blockSignals(False)
                self.precision_spinbox.blockSignals(True)
                self.precision_spinbox.setValue(current_precision)
                self.precision_spinbox.blockSignals(False)

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

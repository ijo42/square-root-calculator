"""UI builder for creating main window widgets and layouts.

Построитель пользовательского интерфейса для создания виджетов и макетов главного окна.
"""

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QTextEdit,
    QGroupBox,
    QSlider,
    QTabWidget,
    QListWidget,
    QSplitter,
    QWidget,
)
from PyQt6.QtCore import Qt

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
from .widget_helpers import WidgetHelpers, StyleConstants


class UIBuilder:
    """Builds UI components for the main window.

    Строит компоненты пользовательского интерфейса для главного окна.
    """

    def __init__(self, main_window):
        """Initialize UI builder.

        Args:
            main_window: Reference to the main window instance
        """
        self.window = main_window
        self.helpers = WidgetHelpers()

    def setup_window(self):
        """Setup main window properties.

        Настроить свойства главного окна.
        """
        self.window.setWindowTitle(self.window.translator.get("app_title"))
        self.helpers.set_widget_size(
            self.window, min_width=WINDOW_MIN_WIDTH, min_height=WINDOW_MIN_HEIGHT
        )

    def create_top_row(self) -> QHBoxLayout:
        """Create top row with input tabs and precision control.

        Создать верхний ряд с вкладками ввода и управлением точностью.

        Returns:
            Horizontal layout with mode tabs and precision control
        """
        top_row_layout = QHBoxLayout()

        # Left side: Mode tabs with input fields
        input_container = self.create_input_tabs()
        top_row_layout.addWidget(input_container, stretch=3)

        # Right side: Precision control
        precision_group = self.create_precision_control()
        top_row_layout.addWidget(precision_group, stretch=2)

        return top_row_layout

    def create_input_tabs(self) -> QWidget:
        """Create input tabs container with real and complex mode tabs.

        Создать контейнер вкладок ввода с вкладками реального и комплексного режимов.

        Returns:
            Widget containing mode tabs
        """
        # Mode selection using tabs
        self.window.mode_tabs = QTabWidget()

        # Container for tabs and buttons
        input_container = QWidget()
        input_container_layout = QVBoxLayout()
        input_container_layout.setContentsMargins(0, 0, 0, 0)
        input_container.setLayout(input_container_layout)
        input_container_layout.addWidget(self.window.mode_tabs)

        # Create tabs
        self.create_real_numbers_tab()
        self.create_complex_numbers_tab()

        # Buttons
        button_layout = self.create_buttons()
        input_container_layout.addLayout(button_layout)

        return input_container

    def create_real_numbers_tab(self):
        """Create real numbers input tab.

        Создать вкладку ввода действительных чисел.
        """
        real_tab = QWidget()
        real_layout = QVBoxLayout()
        real_tab.setLayout(real_layout)

        real_input_layout = QHBoxLayout()

        # Label
        self.window.input_label = self.helpers.create_label(
            min_width=LABEL_MIN_WIDTH, font_size=StyleConstants.FONT_SIZE_NORMAL
        )
        real_input_layout.addWidget(self.window.input_label)
        real_input_layout.addStretch()

        # Input field
        self.window.input_field = self.helpers.create_input_field(
            min_width=INPUT_MIN_WIDTH,
            max_width=INPUT_MIN_WIDTH,
            font_size=StyleConstants.FONT_SIZE_NORMAL,
        )
        real_input_layout.addWidget(self.window.input_field)

        real_layout.addLayout(real_input_layout)
        real_layout.addStretch()

        self.window.mode_tabs.addTab(real_tab, "")

    def create_complex_numbers_tab(self):
        """Create complex numbers input tab.

        Создать вкладку ввода комплексных чисел.
        """
        complex_tab = QWidget()
        complex_layout = QVBoxLayout()
        complex_tab.setLayout(complex_layout)

        # Real part
        real_row = self._create_complex_input_row()
        self.window.real_part_label = real_row["label"]
        self.window.real_part_field = real_row["field"]
        complex_layout.addLayout(real_row["layout"])

        # Imaginary part
        imag_row = self._create_complex_input_row()
        self.window.imag_part_label = imag_row["label"]
        self.window.imag_part_field = imag_row["field"]
        complex_layout.addLayout(imag_row["layout"])

        complex_layout.addStretch()

        self.window.mode_tabs.addTab(complex_tab, "")

    def _create_complex_input_row(self) -> dict:
        """Create a row for complex number input (label + field).

        Создать строку для ввода комплексного числа.

        Returns:
            Dictionary with 'layout', 'label', and 'field' keys
        """
        row_layout = QHBoxLayout()

        label = self.helpers.create_label(
            min_width=LABEL_MIN_WIDTH, font_size=StyleConstants.FONT_SIZE_NORMAL
        )
        row_layout.addWidget(label)
        row_layout.addStretch()

        field = self.helpers.create_input_field(
            min_width=INPUT_MIN_WIDTH,
            max_width=INPUT_MIN_WIDTH,
            font_size=StyleConstants.FONT_SIZE_NORMAL,
        )
        row_layout.addWidget(field)

        return {"layout": row_layout, "label": label, "field": field}

    def create_buttons(self) -> QHBoxLayout:
        """Create calculate and clear buttons.

        Создать кнопки вычисления и очистки.

        Returns:
            Horizontal layout with buttons
        """
        button_layout = QHBoxLayout()

        self.window.calculate_button = self.helpers.create_button(
            font_size=StyleConstants.FONT_SIZE_LARGE,
            padding=StyleConstants.BUTTON_PADDING,
            callback=self.window.calculate,
        )
        button_layout.addWidget(self.window.calculate_button)

        self.window.clear_button = self.helpers.create_button(
            font_size=StyleConstants.FONT_SIZE_LARGE,
            padding=StyleConstants.BUTTON_PADDING,
            callback=self.window.clear_fields,
        )
        button_layout.addWidget(self.window.clear_button)

        return button_layout

    def create_precision_control(self) -> QGroupBox:
        """Create precision control group with slider and spinbox.

        Создать группу управления точностью со слайдером и спинбоксом.

        Returns:
            QGroupBox containing precision controls
        """
        precision_group = QGroupBox()
        self.window.precision_group = precision_group
        precision_group.setMinimumWidth(PRECISION_GROUP_MIN_WIDTH)
        precision_layout = QVBoxLayout()

        initial_precision = self.window.settings.get("precision", DEFAULT_PRECISION)

        # Precision value display
        self._create_precision_display(precision_layout, initial_precision)

        # Slider for quick adjustment
        self._create_precision_slider(precision_layout, initial_precision)

        # SpinBox for precise input
        self._create_precision_spinbox(precision_layout, initial_precision)

        # Show either slider or spinbox (mutually exclusive)
        show_exact = self.window.settings.get("show_exact_precision", False)
        self.toggle_precision_display(show_exact)

        precision_group.setLayout(precision_layout)
        return precision_group

    def _create_precision_display(self, parent_layout, initial_precision):
        """Create precision value display.

        Создать отображение значения точности.
        """
        precision_value_layout = QHBoxLayout()

        self.window.precision_label = self.helpers.create_label(
            font_size=StyleConstants.FONT_SIZE_NORMAL
        )
        precision_value_layout.addWidget(self.window.precision_label)

        self.window.precision_value_label = self.helpers.create_label(
            text=str(initial_precision),
            font_size=StyleConstants.FONT_SIZE_LARGE,
            bold=True,
        )
        precision_value_layout.addWidget(self.window.precision_value_label)
        precision_value_layout.addStretch()

        self.window.precision_value_layout = precision_value_layout
        parent_layout.addLayout(precision_value_layout)

    def _create_precision_slider(self, parent_layout, initial_precision):
        """Create precision slider with labels.

        Создать слайдер точности с метками.
        """
        self.window.slider_layout = QHBoxLayout()

        self.window.slider_min_label = self.helpers.create_label(
            text=str(PRECISION_SLIDER_MIN), font_size=StyleConstants.FONT_SIZE_SMALL
        )
        self.window.slider_layout.addWidget(self.window.slider_min_label)

        self.window.precision_slider = QSlider(Qt.Orientation.Horizontal)
        self.window.precision_slider.setMinimum(PRECISION_SLIDER_MIN)
        self.window.precision_slider.setMaximum(PRECISION_SLIDER_MAX)
        self.window.precision_slider.setValue(initial_precision)
        self.window.precision_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.window.precision_slider.setTickInterval(PRECISION_SLIDER_TICK_INTERVAL)
        self.window.precision_slider.valueChanged.connect(
            self.window.precision_slider_changed
        )
        self.window.slider_layout.addWidget(self.window.precision_slider)

        self.window.slider_max_label = self.helpers.create_label(
            text=str(PRECISION_SLIDER_MAX), font_size=StyleConstants.FONT_SIZE_SMALL
        )
        self.window.slider_layout.addWidget(self.window.slider_max_label)

        parent_layout.addLayout(self.window.slider_layout)

    def _create_precision_spinbox(self, parent_layout, initial_precision):
        """Create precision spinbox with label.

        Создать спинбокс точности с меткой.
        """
        self.window.spinbox_layout = QHBoxLayout()

        self.window.spinbox_label = self.helpers.create_label(
            font_size=StyleConstants.FONT_SIZE_NORMAL
        )
        self.window.spinbox_layout.addWidget(self.window.spinbox_label)

        self.window.precision_spinbox = QSpinBox()
        self.window.precision_spinbox.setMinimum(PRECISION_SPINBOX_MIN)
        self.window.precision_spinbox.setMaximum(PRECISION_SPINBOX_MAX)
        self.window.precision_spinbox.setValue(initial_precision)
        self.window.precision_spinbox.setStyleSheet(
            f"font-size: {StyleConstants.FONT_SIZE_NORMAL}px;"
        )
        self.window.precision_spinbox.valueChanged.connect(
            self.window.precision_spinbox_changed
        )
        self.window.spinbox_layout.addWidget(self.window.precision_spinbox)
        self.window.spinbox_layout.addStretch()

        parent_layout.addLayout(self.window.spinbox_layout)

    def toggle_precision_display(self, show_exact: bool):
        """Toggle between slider and exact precision spinbox display.

        Переключить отображение между слайдером и точным спинбоксом.

        Args:
            show_exact: True to show spinbox, False to show slider
        """
        # Define widget groups for show/hide
        slider_widgets = [
            self.window.precision_label,
            self.window.precision_value_label,
            self.window.slider_min_label,
            self.window.precision_slider,
            self.window.slider_max_label,
        ]
        spinbox_widgets = [self.window.spinbox_label, self.window.precision_spinbox]

        if show_exact:
            for widget in spinbox_widgets:
                widget.show()
            for widget in slider_widgets:
                widget.hide()
        else:
            for widget in slider_widgets:
                widget.show()
            for widget in spinbox_widgets:
                widget.hide()

    def create_result_and_history_section(self) -> QSplitter:
        """Create result display and history panel.

        Создать панель отображения результатов и истории.

        Returns:
            QSplitter containing result and history sections
        """
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Result display
        result_group = QGroupBox()
        self.window.result_group = result_group
        result_layout = QVBoxLayout()

        self.window.result_display = QTextEdit()
        self.window.result_display.setReadOnly(True)
        self.helpers.set_widget_size(self.window.result_display, min_height=150)
        self.helpers.apply_monospace_style(
            self.window.result_display,
            font_size=StyleConstants.FONT_SIZE_NORMAL,
            padding=StyleConstants.TEXT_PADDING,
        )
        result_layout.addWidget(self.window.result_display)
        result_group.setLayout(result_layout)
        splitter.addWidget(result_group)

        # History panel
        history_group = QGroupBox()
        self.window.history_group = history_group
        history_layout = QVBoxLayout()

        self.window.history_list = QListWidget()
        self.helpers.apply_monospace_style(
            self.window.history_list, font_size=StyleConstants.FONT_SIZE_NORMAL
        )
        self.window.history_list.itemDoubleClicked.connect(
            self.window.history_item_double_clicked
        )
        history_layout.addWidget(self.window.history_list)

        self.window.clear_history_button = self.helpers.create_button(
            callback=self.window.clear_history
        )
        history_layout.addWidget(self.window.clear_history_button)

        history_group.setLayout(history_layout)
        splitter.addWidget(history_group)

        # Set initial splitter sizes
        splitter.setSizes([SPLITTER_RESULT_SIZE, SPLITTER_HISTORY_SIZE])

        return splitter

"""Menu builder for the main window.

Построитель меню для главного окна.
"""

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu


class MenuBuilder:
    """Handles menu bar creation and management.

    Обрабатывает создание и управление строкой меню.
    """

    def __init__(self, main_window):
        """Initialize menu builder.

        Args:
            main_window: Reference to the main window instance
        """
        self.window = main_window

    def create_menu_bar(self):
        """Create the complete menu bar.

        Создать полную строку меню.
        """
        menubar = self.window.menuBar()

        self._create_settings_menu(menubar)
        self._create_language_menu(menubar)
        self._create_help_menu(menubar)

    def _create_settings_menu(self, menubar):
        """Create settings menu with theme and display options.

        Создать меню настроек с темами и параметрами отображения.

        Args:
            menubar: Main menu bar to add menu to
        """
        self.window.settings_menu = menubar.addMenu("Settings")

        self._create_theme_submenu()
        self.window.settings_menu.addSeparator()
        self._create_display_options()

    def _create_theme_submenu(self):
        """Create theme selection submenu.

        Создать подменю выбора темы.
        """
        self.window.theme_menu = QMenu("Theme", self.window)
        self.window.settings_menu.addMenu(self.window.theme_menu)

        self.window.light_theme_action = QAction("Light Theme", self.window)
        self.window.light_theme_action.setCheckable(True)
        current_theme = self.window.settings.get("theme")
        self.window.light_theme_action.setChecked(current_theme == "light")
        self.window.light_theme_action.triggered.connect(
            lambda: self.window.change_theme("light")
        )
        self.window.theme_menu.addAction(self.window.light_theme_action)

        self.window.dark_theme_action = QAction("Dark Theme", self.window)
        self.window.dark_theme_action.setCheckable(True)
        self.window.dark_theme_action.setChecked(current_theme == "dark")
        self.window.dark_theme_action.triggered.connect(
            lambda: self.window.change_theme("dark")
        )
        self.window.theme_menu.addAction(self.window.dark_theme_action)

    def _create_display_options(self):
        """Create display options in settings menu.

        Создать параметры отображения в меню настроек.
        """
        # Show exact precision field toggle
        self.window.show_exact_precision_action = QAction(
            "Show Exact Precision Field", self.window
        )
        self.window.show_exact_precision_action.setCheckable(True)
        self.window.show_exact_precision_action.setChecked(
            self.window.settings.get("show_exact_precision", False)
        )
        self.window.show_exact_precision_action.triggered.connect(
            self.window.toggle_exact_precision
        )
        self.window.settings_menu.addAction(
            self.window.show_exact_precision_action
        )

        # Show negative roots toggle
        self.window.show_negative_roots_action = QAction(
            "Show Negative Roots", self.window
        )
        self.window.show_negative_roots_action.setCheckable(True)
        self.window.show_negative_roots_action.setChecked(
            self.window.settings.get("show_negative_roots", False)
        )
        self.window.show_negative_roots_action.triggered.connect(
            self.window.toggle_negative_roots
        )
        self.window.settings_menu.addAction(
            self.window.show_negative_roots_action
        )

    def _create_language_menu(self, menubar):
        """Create language selection menu.

        Создать меню выбора языка.

        Args:
            menubar: Main menu bar to add menu to
        """
        self.window.language_menu = menubar.addMenu("Language")
        self.window.language_actions = {}
        self.window.build_language_menu()

    def _create_help_menu(self, menubar):
        """Create help menu with manual, updates, and about options.

        Создать меню справки с руководством, обновлениями и информацией.

        Args:
            menubar: Main menu bar to add menu to
        """
        self.window.help_menu = menubar.addMenu("Help")

        self.window.user_manual_action = QAction("User Manual", self.window)
        self.window.user_manual_action.triggered.connect(
            self.window.open_user_manual
        )
        self.window.help_menu.addAction(self.window.user_manual_action)

        self.window.help_menu.addSeparator()

        self.window.check_updates_action = QAction(
            "Check for Updates", self.window
        )
        self.window.check_updates_action.triggered.connect(
            self.window.check_for_updates_manual
        )
        self.window.help_menu.addAction(self.window.check_updates_action)

        self.window.help_menu.addSeparator()

        self.window.about_action = QAction("About", self.window)
        self.window.about_action.triggered.connect(self.window.show_about)
        self.window.help_menu.addAction(self.window.about_action)

        self.window.help_action = QAction("Help", self.window)
        self.window.help_action.triggered.connect(self.window.show_help)
        self.window.help_menu.addAction(self.window.help_action)

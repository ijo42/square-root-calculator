"""UI components and styling helpers for the Square Root Calculator.

Компоненты пользовательского интерфейса и помощники стилей для Калькулятора квадратного корня.
"""

try:
    from qt_material import apply_stylesheet

    HAS_QT_MATERIAL = True
except ImportError:
    HAS_QT_MATERIAL = False


def apply_theme_to_window(window, theme: str):
    """Apply theme to the main window.

    Применить тему к главному окну.

    Args:
        window: Main window instance
        theme: Theme name ('light' or 'dark')
    """
    if HAS_QT_MATERIAL:
        if theme == "dark":
            apply_stylesheet(window.app, theme="dark_teal.xml")
        else:
            apply_stylesheet(window.app, theme="light_blue.xml")
    else:
        # Fallback stylesheet if qt-material is not available
        if theme == "dark":
            window.setStyleSheet(
                """
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QLineEdit, QTextEdit, QSpinBox {
                    background-color: #3c3c3c;
                    color: #ffffff;
                    border: 1px solid #555555;
                }
                QPushButton {
                    background-color: #0d7377;
                    color: #ffffff;
                    border: none;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #14a1a8;
                }
                QGroupBox {
                    border: 1px solid #555555;
                    margin-top: 10px;
                    font-weight: bold;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 5px;
                }
            """
            )
        else:
            window.setStyleSheet(
                """
                QLineEdit, QTextEdit, QSpinBox {
                    border: 1px solid #cccccc;
                    padding: 4px;
                }
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: none;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #357abd;
                }
            """
            )


def get_output_stylesheet(theme: str) -> str:
    """Get stylesheet for output text area based on theme.

    Получить стиль для области вывода текста на основе темы.

    Args:
        theme: Theme name ('light' or 'dark')

    Returns:
        Stylesheet string for the output area
    """
    if theme == "dark":
        return """
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444444;
                font-family: 'Courier New', monospace;
                font-size: 11pt;
            }
        """
    else:
        return """
            QTextEdit {
                background-color: #f8f8f8;
                border: 1px solid #cccccc;
                font-family: 'Courier New', monospace;
                font-size: 11pt;
            }
        """

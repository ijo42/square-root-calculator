"""Background thread for checking application updates.

Фоновый поток для проверки обновлений приложения.
"""

from PyQt6.QtCore import QThread, pyqtSignal


class UpdateCheckThread(QThread):
    """Thread for checking updates without blocking UI.
    
    Поток для проверки обновлений без блокировки пользовательского интерфейса.
    """
    
    update_checked = pyqtSignal(bool, str, str)  # has_update, version, error
    
    def __init__(self, checker):
        """Initialize update check thread.
        
        Args:
            checker: UpdateChecker instance to use for checking updates
        """
        super().__init__()
        self.checker = checker
    
    def run(self):
        """Run update check in background.
        
        Запустить проверку обновлений в фоновом режиме.
        """
        has_update, version, error = self.checker.check_for_updates()
        self.update_checked.emit(has_update, version or "", error or "")

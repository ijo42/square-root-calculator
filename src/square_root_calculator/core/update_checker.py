"""Update checker for checking new versions from GitHub.

Проверка обновлений для проверки новых версий из GitHub.
"""

import urllib.request
import urllib.error
import json
from typing import Optional, Tuple


class UpdateChecker:
    """Check for application updates from GitHub.
    
    Проверка обновлений приложения из GitHub.
    """
    
    def __init__(self, repo_owner: str, repo_name: str, current_version: str):
        """Initialize update checker.
        
        Инициализировать проверку обновлений.
        
        Args:
            repo_owner: GitHub repository owner
                       Владелец репозитория GitHub
            repo_name: GitHub repository name
                      Название репозитория GitHub
            current_version: Current application version
                           Текущая версия приложения
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.pyproject_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/master/pyproject.toml"
    
    def check_for_updates(self, timeout: int = 5) -> Tuple[bool, Optional[str], Optional[str]]:
        """Check if a new version is available.
        
        Проверить, доступна ли новая версия.
        
        Args:
            timeout: Request timeout in seconds
                    Таймаут запроса в секундах
            
        Returns:
            Tuple of (update_available, latest_version, error_message)
            Кортеж (доступно_обновление, последняя_версия, сообщение_об_ошибке)
        """
        try:
            # Fetch pyproject.toml from master branch
            req = urllib.request.Request(
                self.pyproject_url,
                headers={'User-Agent': 'Square-Root-Calculator'}
            )
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read().decode('utf-8')
                
                # Parse version from pyproject.toml
                latest_version = self._parse_version_from_toml(content)
                
                if latest_version is None:
                    return False, None, "Could not parse version from pyproject.toml"
                
                # Compare versions
                update_available = self._is_newer_version(latest_version, self.current_version)
                
                return update_available, latest_version, None
                
        except urllib.error.URLError as e:
            return False, None, f"Network error: {str(e)}"
        except Exception as e:
            return False, None, f"Error checking updates: {str(e)}"
    
    def _parse_version_from_toml(self, content: str) -> Optional[str]:
        """Parse version from pyproject.toml content.
        
        Извлечь версию из содержимого pyproject.toml.
        
        Args:
            content: Content of pyproject.toml
                    Содержимое pyproject.toml
        
        Returns:
            Version string or None
            Строка версии или None
        """
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('version'):
                # Extract version from line like: version = "0.1.0"
                parts = line.split('=')
                if len(parts) == 2:
                    version = parts[1].strip().strip('"').strip("'")
                    return version
        return None
    
    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Compare version strings.
        
        Сравнить строки версий.
        
        Args:
            latest: Latest version string
                   Строка последней версии
            current: Current version string
                    Строка текущей версии
            
        Returns:
            True if latest is newer than current
            True, если последняя версия новее текущей
        """
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Pad to same length
            while len(latest_parts) < len(current_parts):
                latest_parts.append(0)
            while len(current_parts) < len(latest_parts):
                current_parts.append(0)
            
            # Compare each part
            for l, c in zip(latest_parts, current_parts):
                if l > c:
                    return True
                elif l < c:
                    return False
            
            return False  # Versions are equal
            
        except (ValueError, AttributeError):
            # If parsing fails, assume no update
            return False

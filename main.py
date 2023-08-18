from config import api_id, api_hash
import telegram_session as tgses
import window_tools as win


class Teleparser:
    """Приложение для парсинга telegram с графическим интерфейсом.
    Атрибуты:
        1. Главное окно с поддержкой сценариев.
        2. Ядро telegram-сессии"""

    def __init__(self) -> None:
        """Создает главное окно, задает ему параметры и подвязывает к telegram сессии"""
        self.app = tgses.GUIClient(api_hash=api_hash, api_id=api_id)
        self.gui = win.MainInterface()




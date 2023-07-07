from config import api_id, api_hash
import telegram_session as tgses
import window_tools as win


class Teleparser:
    """Приложение для парсинга telegram с графическим интерфейсом.
    Атрибуты:
        1. Главное окно с поддержкой сценариев.
        2. Ядро telegram-сессии"""

    def __init__(self, win_name: str='teleparser',
                       win_icon: str='teleparser',
                       win_size: str='teleparser') -> None:
        """Создает главное окно, задает ему параметры и подвязывает к telegram сессии"""
        pass


tgses.check(api_id, api_hash)
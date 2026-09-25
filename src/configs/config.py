import logging
from decouple import config


class Settings:
    log_format = '%(levelname)s:     %(message)s'
    log_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }


    def __init__(self):
        # Устанавливаем логгер
        log_level = config('LOG_LEVEL', default='info', cast=str)
        logging.basicConfig(level=self.log_levels.get(log_level), 
                            format=self.log_format)
        self.logger = logging.getLogger(__name__)

        # Получаем API ключ
        self.VK_API_KEY = config('VK_API_KEY', cast=str)

        # Получаем домен группы
        self.VK_GROUP_DOMAIN = config('VK_GROUP_DOMAIN')

settings = Settings()
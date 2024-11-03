import json
import logging
import logging.config


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level: int, logger_name=''):
        super().__init__(logger_name)
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = True
    logger.handlers = []
    return logger


with open('secrets.json', encoding='utf-8') as file:
    secrets = json.load(file)

    RIOT_API_KEY: str = secrets['RIOT_API_KEY']

POSTGRES_USER = 'riot'
POSTGRES_PASSWORD = '1515'
POSTGRES_HOST = 'localhost'
POSTGRES_DB = 'lol'

NOT_FOUNDED_WARNING = 100
NOT_FOUNDED_ERROR = 250
NOT_FOUNDED_EXIT = 500

LOGCONFIG_DICT = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        }
    },
    'handlers': {
        'out': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filters': [MaxLevelFilter(logging.INFO)],
            'stream': 'ext://sys.stdout',
        },
        'err': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'default',
            'stream': 'ext://sys.stderr',
        }
    },
    'loggers': {
        'gunicorn.access': {
            'level': 'WARNING',
            'propagate': True
        },
        'gunicorn.error': {
            'level': 'NOTSET',
            'propagate': True
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['out', 'err']
    },
    'disable_existing_loggers': False
}

logging.config.dictConfig(LOGCONFIG_DICT)

import json
import logging
import logging.config
import os

# configs

CONFIG = os.environ

POSTGRES_USER = CONFIG['POSTGRES_USER']
POSTGRES_DB = CONFIG['POSTGRES_DB']

NOT_FOUNDED_WARNING = 100
NOT_FOUNDED_ERROR = 250
NOT_FOUNDED_EXIT = 500

# secrets

API_KEY_PATH = '/run/secrets/secrets.json'
API_KEY_PATH_DEBUG = '../../secrets.json'
POSTGRES_PASSWORD_PATH = '/run/secrets/postgres_password'
POSTGRES_PASSWORD_PATH_DEBUG = '/../../postgres_password'

try:
    with open(API_KEY_PATH, encoding='utf-8') as file:
        RIOT_API_KEY = json.load(file)['RIOT_API_KEY_PROD']
    with open(POSTGRES_PASSWORD_PATH, encoding='utf-8') as file:
        POSTGRES_PASSWORD = file.read()

    POSTGRES_HOST = CONFIG['POSTGRES_HOST']

except FileNotFoundError:
    with open(API_KEY_PATH_DEBUG, encoding='utf-8') as file:
        RIOT_API_KEY = json.load(file)['RIOT_API_KEY_DEV']
    with open(POSTGRES_PASSWORD_PATH_DEBUG, encoding='utf-8') as file:
        POSTGRES_PASSWORD = file.read()

    POSTGRES_HOST = 'localhost'


# logging

class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level: int, logger_name=''):
        super().__init__(logger_name)
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


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


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = True
    logger.handlers = []
    return logger

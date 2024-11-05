import json
import logging
import logging.config
import os

import requests

# configs

NAME = 'Collector'

NOT_FOUNDED_WARNING = 100
NOT_FOUNDED_ERROR = 250
NOT_FOUNDED_EXIT = 500

API_KEY_PATH = '/run/secrets/secrets.json'
API_KEY_PATH_DEBUG = '../../secrets.json'
POSTGRES_PASSWORD_PATH = '/run/secrets/postgres_password'
POSTGRES_PASSWORD_PATH_DEBUG = '/../../postgres_password'

try:
    with open(API_KEY_PATH, encoding='utf-8') as file:
        SECRETS = json.load(file)

    with open(POSTGRES_PASSWORD_PATH, encoding='utf-8') as file:
        POSTGRES_PASSWORD = file.read()

    RIOT_API_KEY = SECRETS['RIOT_API_KEY_PROD']

    TG_BOT_TOKEN = SECRETS['TG_BOT_TOKEN']
    TG_ALL_ERROR_CHAT = SECRETS['TG_ALL_ERROR_CHAT']

    CONFIG = os.environ
    MODE = CONFIG['MODE']

    POSTGRES_USER = CONFIG['POSTGRES_USER']
    POSTGRES_HOST = CONFIG['POSTGRES_HOST']
    POSTGRES_DB = CONFIG['POSTGRES_DB']

except FileNotFoundError:
    with open(API_KEY_PATH_DEBUG, encoding='utf-8') as file:
        SECRETS = json.load(file)

    with open(POSTGRES_PASSWORD_PATH_DEBUG, encoding='utf-8') as file:
        POSTGRES_PASSWORD = file.read()

    RIOT_API_KEY = SECRETS['RIOT_API_KEY_DEV']

    MODE = 'DEV'

    POSTGRES_USER = 'riot'
    POSTGRES_HOST = 'localhost'
    POSTGRES_DB = 'lol'


# logging

class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level: int, logger_name=''):
        super().__init__(logger_name)
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


class TGHandler(logging.Handler):
    def __init__(self):
        super().__init__()

        self.url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/'
        self.chat_id = TG_ALL_ERROR_CHAT

    def emit(self, record):
        error = self.format(record)

        # noinspection PyBroadException
        try:
            length = 3000

            if len(error) > length:
                text = f'{error[:length // 2]}...\n{'.\n' * 3}...{error[-length // 2:]}'
            else:
                text = error

            response = requests.post(
                url=f'{self.url}sendMessage',
                data={
                    'chat_id': self.chat_id,
                    'text': f'{NAME}\n```log\n{text}\n```',
                    'parse_mode': 'MarkdownV2'
                }
            )

            if response.status_code != 200:
                raise Exception

            response = requests.post(
                url=f'{self.url}sendDocument',
                data={
                    'chat_id': self.chat_id,
                    'reply_parameters': json.dumps({'message_id': response.json()['result']['message_id']})
                },
                files={
                    'document': ('error.txt', error)
                }
            )

            if response.status_code != 200:
                raise Exception

        except Exception:
            self.handleError(record)


if MODE == 'PROD':
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
            },
            'tg': {
                '()': TGHandler,
                'level': 'ERROR',
                'formatter': 'default'
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
            'handlers': ['out', 'err', 'tg']
        },
        'disable_existing_loggers': False
    }

elif MODE == 'DEV':
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

else:
    raise ValueError('MODE must be PROD or DEV')

logging.config.dictConfig(LOGCONFIG_DICT)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = True
    logger.handlers = []
    return logger

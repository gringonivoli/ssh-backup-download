import logging
import os
import requests
from config import LOGGER_NAME, LOGS_PATH, DEBUG


def send_telegram_msg(message=''):
    """Envía un mensaje al chat de telegram que se indica
    en la variable de entorno TELEGRAM_CHAT_ID con el bot
    con token especificado en la var de entorno TELEGRAM_BOT_TOKEN.

    Parameters
    ----------
    message : str, optional
        Mensaje a enviar por telegram, by default ''
    """
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    telegram_api = os.getenv('TELEGRAM_API')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f'{telegram_api}/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    requests.post(url)


def set_logging(log_name):
    """Setea el logger, para usarlo se debe llamar a
    logging.getLogger(LOGGER_NAME)

    Parameters
    ----------
    log_name : str
        nombre del file en donde se va a escribir el log
    """
    logger = logging.getLogger(LOGGER_NAME)
    general_level = logging.DEBUG if DEBUG else logging.INFO
    logger.setLevel(general_level)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'{LOGS_PATH}{log_name}')
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    msg_format = '%(asctime)s [%(filename)s]-[%(levelname)s]: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    console_format = logging.Formatter(msg_format, datefmt=date_format)
    file_format = logging.Formatter(msg_format, datefmt=date_format)
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

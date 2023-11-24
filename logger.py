import logging

from logging_config import config


def get_logger():
    root = logging.getLogger()
    root.setLevel(config['level'])

    handler = logging.StreamHandler(config['stream_handler'])
    handler.setLevel(config['level'])
    formatter = logging.Formatter(config['format'])
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


logger = get_logger()

logger.info('Bot logger is init')


def set_log_level(level: str = 'INFO'):
    global logger
    if level.lower() == 'info':
        config['level'] = logging.INFO
    elif level.lower() == 'debug':
        config['level'] = logging.DEBUG
    else:
        pass
    logger = get_logger()
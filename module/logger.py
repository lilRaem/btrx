import logging
import logging.handlers


def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s:%(lineno)s =>\n[ %(message)s ]'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(filename="logs/main.log",backupCount=1,encoding='utf-8')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug("***Logger INITIALIZED***")
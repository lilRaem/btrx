import logging
import logging.handlers


def init_logger(name:str,file:str):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s | %(levelname)s | %(name)s:%(lineno)s =>\n[ %(message)s ]\n'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(filename=f"logs/{file}.log",backupCount=2,encoding='utf-8')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    # logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug("[***] | Logger INITIALIZED | [***]")
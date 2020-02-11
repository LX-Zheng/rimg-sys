import logging
from logging.handlers import TimedRotatingFileHandler

from app import app

if __name__ == '__main__':
    app.debug = True
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    # when=D 按天切分，interval=1，每天都切分，backupCount=15，保留15天日志
    handler = TimedRotatingFileHandler(
        "flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)
    app.run()
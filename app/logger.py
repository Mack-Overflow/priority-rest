import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)  # Log only error messages or higher

    # Create file handler which logs even debug messages
    fh = RotatingFileHandler('errors.log', maxBytes=10000, backupCount=5)
    fh.setLevel(logging.ERROR)
    fh.addFilter(ContextualFilter())

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)

    return logger


def request_formatter():
    return request.url if request else "No request"

# Add custom request details in log records
class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        log_record.request = request_formatter()
        return True

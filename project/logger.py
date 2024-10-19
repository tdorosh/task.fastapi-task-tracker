import logging


def setup_logger():
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)
    _logger.addHandler(logging.StreamHandler())
    return _logger


logger = setup_logger()

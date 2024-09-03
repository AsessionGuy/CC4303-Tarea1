"""
Logger module that provides a shared logger instance for the project.
"""
import logging

logging.basicConfig(level=logging.INFO)

class Logger:
    """
    Logger class that provides a shared logger instance for the project.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

logger = Logger()
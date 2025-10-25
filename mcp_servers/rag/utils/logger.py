import logging
import sys
from rich.logging import RichHandler

def get_logger(name: str = "LoopMind"):
    """Create and configure a logger with rich output."""
    # Configure root logger to use stderr
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        handler = RichHandler(rich_tracebacks=True, markup=True)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)

    # Create named logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

log = get_logger("")
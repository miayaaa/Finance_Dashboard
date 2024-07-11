import logging
from datetime import datetime
import os


def setup_logging():
    """Set up logging to a file."""
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = os.path.join(log_dir, datetime.now().strftime("log_%Y%m%d.txt"))

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )



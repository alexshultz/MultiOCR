import logging
from enum import Enum, auto

class LogType(Enum):
    NORMAL = auto()
    DISPLAY = auto()
    ALL = auto()

def setup_logging(log_type: LogType):
    if log_type == LogType.NORMAL or log_type == LogType.ALL:
        logging.basicConfig(filename='normal.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    
    if log_type == LogType.DISPLAY or log_type == LogType.ALL:
        display_logger = logging.getLogger('display')
        display_logger.setLevel(logging.INFO)
        fh = logging.FileHandler('display.log')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        display_logger.addHandler(fh)

def log_message(message: str, log_type: LogType):
    if log_type == LogType.NORMAL or log_type == LogType.ALL:
        logging.info(message)
    
    if log_type == LogType.DISPLAY or log_type == LogType.ALL:
        display_logger = logging.getLogger('display')
        display_logger.info(message)

# Usage example:
setup_logging(LogType.ALL)
log_message("Processing file_1.txt", LogType.NORMAL)
log_message("File_1.txt processed successfully", LogType.DISPLAY)
log_message("Moving to next file", LogType.ALL)

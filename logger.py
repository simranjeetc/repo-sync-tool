import logging
import os

# Get the log directory from environment variable or use default
LOG_DIR = os.getenv("LOG_DIR", "/app/logs")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all types of log messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'app.log')),
        logging.StreamHandler()
    ]
)

# Custom logger
logger = logging.getLogger("RepoSyncTool")

def log_debug(message):
    logger.debug(message)

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message)

def log_critical(message):
    logger.critical(message)

def log_exception(message):
    logger.exception(message)  # This automatically includes the traceback

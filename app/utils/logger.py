from loguru import logger
import sys

# Remove all existing handlers
logger.remove()

# Configure logger
logger.add(sys.stdout, level="INFO", format="{time} - {name} - {level} - {message}")

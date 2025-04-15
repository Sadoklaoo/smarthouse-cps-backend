# app/core/logging_config.py
import logging

# Create logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)  # You can adjust the log level to DEBUG or ERROR as needed

# Create console handler
console_handler = logging.StreamHandler()

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

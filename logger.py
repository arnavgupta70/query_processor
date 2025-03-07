"""
logger.py

Provides simple logging for capturing errors 
and important events. This helps with debugging 
the flow in more complex scenarios.
"""

import datetime

class AppLogger:
    def __init__(self, log_file="application.log"):
        """
        Initialize the AppLogger with a default log file name.
        """
        self.log_file = log_file

    def log_error(self, error_type: str, message: str):
        """
        Logs an error event to the specified log file.

        Args:
            error_type (str): descriptor of the error category (e.g., "PromptSelectorError").
            message (str): The detailed error message or stack trace.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] ERROR: {error_type} - {message}\n"
        self._write_to_log(log_entry)


    def log_info(self, info_type: str, message: str):
        """
        Logs an informational event to the log file.

        Args:
            info_type (str): descriptor of the info category (e.g., "SystemStart").
            message (str): The detailed information message.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] INFO: {info_type} - {message}\n"
        self._write_to_log(log_entry)

    def _write_to_log(self, log_entry: str):
        """
        Helper method to write a log entry to the file.
        """
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

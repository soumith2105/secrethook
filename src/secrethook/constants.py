"""
Shared constants for colors and whitelist markers used across the project.
"""


# Terminal color codes
class Colors:
    """
    ANSI escape codes for terminal color formatting.
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    GRAY = "\033[90m"


LINE_WHITELIST = "# secret-ok"
"""Inline comment to whitelist a specific line from scanning."""

FILE_WHITELIST = "# secret-file-ok"
"""Comment to whitelist an entire file (first few lines)."""

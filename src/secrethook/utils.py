"""
Utility functions for file-type detection and entropy scoring.
"""

from math import log2
import mimetypes


def shannon_entropy(data: str) -> float:
    """
    Compute Shannon entropy to measure randomness of a string.

    Args:
        data (str): The string to analyze.

    Returns:
        float: Entropy score (higher → more random).
    """

    if not data:
        return 0.0
    freq = {char: data.count(char) for char in set(data)}
    entropy = -sum((f / len(data)) * log2(f / len(data)) for f in freq.values())
    return entropy


def is_text_file(file_path: str) -> bool:
    """
    Determine whether a file is likely to be text-based using MIME type.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if file is text, False otherwise.
    """

    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("text")

"""
Handles loading and parsing of `.secrethookrc` configuration files.

Supports:
- Default fallback config
- Custom regex patterns and preview masks
- Glob-style ignore paths
"""

import json
import os
import re

DEFAULT_CONFIG = {
    "disabled_patterns": [],
    "custom_patterns": {},
    "ignore_paths": [],
    "entropy_threshold": 3.5,
}

CONFIG_FILENAMES = ["secrethook.config.json", ".secrethookrc"]


def load_config() -> dict:
    """
    Load and merge user configuration from `.secrethookrc`.

    Returns:
        dict: Final config dictionary including:
              - compiled_custom_patterns (regex objects)
              - custom_preview_formats (mask templates)
              - ignore_paths
              - disabled_patterns
              - entropy_threshold
    """

    config_data = DEFAULT_CONFIG.copy()
    config_path = next((f for f in CONFIG_FILENAMES if os.path.exists(f)), None)

    if not config_path:
        return config_data

    try:
        with open(config_path, "r") as f:
            user_config = json.load(f)
            config_data.update(user_config)
    except Exception as e:
        print(f"⚠️ Failed to load config: {e}")
        return config_data

    compiled_patterns = {}
    preview_map = {}

    for name, val in config_data.get("custom_patterns", {}).items():
        if isinstance(val, dict):
            if "pattern" in val:
                try:
                    compiled_patterns[name] = re.compile(val["pattern"])
                except re.error as e:
                    print(f"⚠️ Invalid regex for '{name}': {e}")
            if "masked" in val:
                preview_map[name] = val["masked"]
        elif isinstance(val, str):
            try:
                compiled_patterns[name] = re.compile(val)
            except re.error as e:
                print(f"⚠️ Invalid regex for '{name}': {e}")

    config_data["compiled_custom_patterns"] = compiled_patterns
    config_data["custom_preview_formats"] = preview_map

    return config_data

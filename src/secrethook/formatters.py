"""
Helpers to format detected secrets into masked previews.
"""

from secrethook.patterns import PATTERNS


def apply_template_mask(template: str, value: str) -> str:
    """
    Replace placeholder tags like {last4}, {length}, etc. in a mask template.

    Args:
        template (str): Template string with placeholders.
        value (str): The detected secret value.

    Returns:
        str: Masked value string for safe display.
    """

    return (
        template.replace("{last4}", value[-4:] if len(value) >= 4 else "XXXX")
        .replace("{last9}", value[-9:] if len(value) >= 9 else "XXXXXXXXX")
        .replace("{first4}", value[:4])
        .replace("{first3}", value[:3])
        .replace("{length}", str(len(value)))
    )


def format_secret_preview(name: str, value: str, config: dict) -> str:
    """
    Generate a masked preview for a matched secret using built-in or custom templates.

    Args:
        name (str): Name of the secret type.
        value (str): The matched secret string.
        config (dict): Loaded config (used to lookup preview format).

    Returns:
        str: Human-readable masked preview.
    """

    custom_masked = config.get("custom_preview_formats", {}).get(name)
    if custom_masked:
        return apply_template_mask(custom_masked, value)

    pattern_meta = PATTERNS.get(name)
    if isinstance(pattern_meta, dict) and "masked" in pattern_meta:
        return apply_template_mask(pattern_meta["masked"], value)

    return f"[{name} •••••••••••••••]"

from secrethook.config_loader import load_config


def test_default_config_fields():
    config = load_config()
    assert "entropy_threshold" in config
    assert isinstance(config["compiled_custom_patterns"], dict)

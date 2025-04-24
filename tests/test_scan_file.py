import tempfile
from secrethook.core import scan_file
from secrethook.config_loader import load_config


def test_scan_detects_secret():
    content = 'api_key = "AKIAABCDEFGHIJKLMNOP"\n'
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        results = scan_file(tmp.name, load_config())

    assert any("AKIA" in r[2] for r in results)

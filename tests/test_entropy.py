from secrethook.utils import shannon_entropy


def test_entropy_low_vs_high():
    low_entropy = shannon_entropy("password123")
    high_entropy = shannon_entropy("ghp_abcdefghijklmnopqrstuvwxyz1234567890")

    assert low_entropy < 4
    assert high_entropy > 4

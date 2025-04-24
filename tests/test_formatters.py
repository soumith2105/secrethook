from secrethook.formatters import apply_template_mask


def test_apply_template_mask():
    result = apply_template_mask("****{last4}", "abcd1234")
    assert result == "****1234"

    result = apply_template_mask("{first3}••••{last4}", "abcdefg")
    assert result == "abc••••defg"

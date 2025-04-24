"""
Command-line interface entrypoint for SecretHook.
Used as `python -m secrethook.cli` or configured via pre-commit hook.
"""

from secrethook.core import main as core_main


def main():
    core_main()


if __name__ == "__main__":
    main()

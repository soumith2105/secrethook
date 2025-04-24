"""
Core scanner logic for SecretHook.

Handles:
- File collection
- Secret scanning using regex + entropy
- Ignore logic and whitelisting
- Summary reporting
"""

import os
import fnmatch
import subprocess
import sys

from secrethook.patterns import PATTERNS
from secrethook.utils import is_text_file, shannon_entropy
from secrethook.formatters import format_secret_preview
from secrethook.config_loader import load_config
from secrethook.constants import Colors, FILE_WHITELIST, LINE_WHITELIST


def get_staged_files() -> list[str]:
    """
    Get all staged files tracked by Git.

    Returns:
        list[str]: List of file paths.
    """

    result = subprocess.run(
        ["git", "ls-files", "--cached"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        print(f"{Colors.FAIL}❌ Could not list git-tracked files.{Colors.ENDC}")
        sys.exit(1)
    return result.stdout.strip().split("\n")


def should_skip_file(file_path: str, config: dict) -> str | None:
    """
    Determine if a file should be skipped (via glob pattern or file-level whitelist).

    Args:
        file_path (str): The file to check.
        config (dict): Loaded config with ignore_paths.

    Returns:
        str | None: Reason for skip (glob pattern or whitelist comment), or None.
    """

    normalized_file = os.path.normpath(file_path)
    for pattern in config.get("ignore_paths", []):
        if fnmatch.fnmatch(normalized_file, pattern):
            return f"ignore: {pattern}"
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(5):
                line = f.readline()
                if not line:
                    break
                if FILE_WHITELIST in line:
                    return FILE_WHITELIST
    except Exception as e:
        print(
            f"{Colors.WARNING}⚠️ Whitelist check failed for {file_path}: {e}{Colors.ENDC}"
        )
    return None


def scan_file(file_path: str, config: dict) -> list[tuple[int, str, str]]:
    """
    Scan a file line by line for secrets using patterns and entropy.

    Args:
        file_path (str): The path to the file.
        config (dict): Loaded config.

    Returns:
        list[tuple[int, str, str]]: List of (line_number, secret_type, matched_value).
    """

    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                for name, meta in PATTERNS.items():
                    if name in config.get("disabled_patterns", []):
                        continue
                    match = meta["pattern"].search(line)
                    if (
                        match
                        and shannon_entropy(match.group()) > config["entropy_threshold"]
                        and LINE_WHITELIST not in line
                    ):
                        findings.append((line_num, name, match.group()))

                for name, pattern in config["compiled_custom_patterns"].items():
                    if name in config.get("disabled_patterns", []):
                        continue
                    match = pattern.search(line)
                    if (
                        match
                        and shannon_entropy(match.group()) > config["entropy_threshold"]
                        and LINE_WHITELIST not in line
                    ):
                        findings.append((line_num, name, match.group()))
    except Exception as e:
        print(f"{Colors.WARNING}⚠️ Could not scan {file_path}: {e}{Colors.ENDC}")
    return findings


def main() -> None:
    """
    CLI entrypoint for scanning staged files.

    Loads configuration, identifies files to scan, detects secrets, and prints results.
    Blocks commit if secrets are found.
    """

    if os.environ.get("SECRETHOOK_RUN_ONCE") == "true":
        return
    os.environ["SECRETHOOK_RUN_ONCE"] = "true"

    config = load_config()
    secrets_found = {}
    staged_files = get_staged_files()

    print(
        f"{Colors.OKCYAN}🔍 Scanning staged files for secrets...{Colors.ENDC}", end="\r"
    )

    for file in staged_files:
        if not file or not os.path.isfile(file) or not is_text_file(file):
            continue

        skip_reason = should_skip_file(file, config)
        if skip_reason:
            print(f"{Colors.GRAY}🛡️  Skipped ({skip_reason}): {file}{Colors.ENDC}")
            continue

        print(f"{Colors.GRAY}Scanning {file}...{Colors.ENDC}", end="\r")
        results = scan_file(file, config)
        if results:
            secrets_found[file] = results

    print(" " * 80, end="\r")  # clear line
    total_files = len(staged_files)
    flagged_files = len(secrets_found)
    total_findings = sum(len(v) for v in secrets_found.values())

    if secrets_found:
        print(f"{Colors.FAIL}\n🚨 Potential secrets detected!{Colors.ENDC}")
        for file, issues in secrets_found.items():
            print(f"\n{Colors.UNDERLINE}{Colors.BOLD}📄 {file}{Colors.ENDC}")
            for line, type_, value in issues:
                print(
                    f"{Colors.WARNING}  🔒 Line {line} [{type_}]: {Colors.GRAY}🔑 {format_secret_preview(type_, value, config)}{Colors.ENDC}"
                )

        print(f"\n{Colors.BOLD}{Colors.OKCYAN}📊 Scan Summary{Colors.ENDC}")
        print(f"{Colors.OKBLUE}  🔍 Files scanned: {total_files}{Colors.ENDC}")
        print(f"{Colors.WARNING}  ❌ Files flagged: {flagged_files}{Colors.ENDC}")
        print(f"{Colors.FAIL}  🚫 Secrets detected: {total_findings}{Colors.ENDC}")

        print(
            f"\n{Colors.FAIL}❌ Commit blocked. Clean or whitelist secrets before committing.{Colors.ENDC}"
        )
        print(
            f"{Colors.OKBLUE}💡 Tip: Use '{LINE_WHITELIST}' or '{FILE_WHITELIST}' to bypass for dev/test.{Colors.ENDC}"
        )
        sys.exit(1)
    else:
        print(f"{Colors.OKGREEN}✅ No secrets found. You're good to go!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}📊 Files scanned: {total_files}{Colors.ENDC}")

# 🔐 SecretHook — Real-Time Code Secrets Detector for Git

Prevent sensitive credentials like API keys, passwords, JWTs, tokens, and URIs from accidentally leaking into your codebase — before they ever reach version control.

- Works as a **pre-commit hook** or as a **CI/CD scan step**  
- Fully customizable with regex + masking + whitelisting  
- Developer-friendly with meaningful masked previews


## 🚀 Features

-  **Pre-commit hook**: Scans only Git-tracked staged files
-  **Regex + Entropy detection**: Catches real secrets, avoids false positives
-  **Pattern masking**: Fake-looking preview shows only partial token for safety
-  **Custom patterns**: Define your own keys/tokens with flexible formats
-  **Config file support** (`.secrethookrc`): Control everything from one place
-  **Smart whitelisting**:
     - `# secret-ok` for line-level ignore
     - `# secret-file-ok` to skip entire files
-  **Ignore Git-ignored files**: Only scans Git-tracked files
-  **Terminal summary**: Clean CLI with colors and hints
-  **Disable specific patterns** via config


## 🧠 How Entropy Helps Catch Real Secrets

SecretHook uses Shannon entropy to measure how random a matched value is — this helps filter out fake, low-risk, or test keys that still match regex patterns.

Why it matters:
- 🔐 Real secrets (API keys, JWTs, passwords) are random and high-entropy
- 🧪 Dummy/test values or predictable strings are low-entropy
- ✅ This reduces false positives and improves precision

Examples:

| String                         | Entropy Score | Detection |
| ------------------------------ | ------------- | --------- |
| password123                    | ~2.85         | ❌ Ignored |
| ghp_aA1bB2cC3dD4eE5fF6gG7      | ~4.8          | ✅ Flagged |
| helloworldhelloworld           | ~1.5          | ❌ Ignored |
| eyJhbGciOiJIUzI1NiIsInR5cCI6Ik | ~4.7          | ✅ Flagged |

You can customize the threshold in .secrethookrc:

```json
{
  "entropy_threshold": 3.2
}
```

Set it to `0` to disable entropy filtering entirely.

## 📦 Installation

Make sure you have Python and [pre-commit](https://pre-commit.com/) installed:

```bash
pip install pre-commit
pre-commit install
```

Add this to your .pre-commit-config.yaml:

```yaml
- repo: https://github.com/soumith2105/secrethook
  rev: v0.1.0
  hooks:
    - id: secrethook
```

Then activate it:

```bash
pre-commit install
```


## ⚙️ Configuration (.secrethookrc)

Create a .secrethookrc or secrethook.config.json at the project root:

```json
{
  "custom_patterns": {
    "Fake Credit Card": {
      "pattern": "\\b4[0-9]{12}(?:[0-9]{3})?\\b",
      "masked": "[•••• •••• •••• {last4}]"
    }
  },
  "disabled_patterns": ["Private Key Start"],
  "ignore_paths": ["tests/mock_data.py", "examples/"],
  "entropy_threshold": 3.2
}
```


## 🧩 Supported Built-in Patterns

| Name             | Example Detected                           |
| ---------------- | ------------------------------------------ |
| AWS Access Key   | `AKIA1234567890EXAMPLE`                    |
| JWT              | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`  |
| MongoDB URI      | `mongodb+srv://user:pass@host/`            |
| OAuth Token      | `ya29.a0AfH6S...`                          |
| Slack Token      | `xoxb-123456789012-123456789012-abc123`    |
| GitHub Token     | `ghp_abcdefghijklmnopqrstuvwxyz1234567890` |
| Password in Code | `password = "12345"`                       |
| _...many more_   | _See `patterns.py` for the full list_      |



## 🛡 Whitelisting Options
- `#secret-ok` → Ignores this line
- `#secret-file-ok` → Ignores this whole file
- `ignore_paths` in config → Skip scanning files/folders

⸻

## 📊 Example Output

```bash
📄 sample_project/config.py
  🔒 Line 1 [JWT]: 🔑 [JWT-like-token eyJ......signature]

📊 Scan Summary
  🔍 Files scanned:       3
  ❌ Files flagged:       1
  🚫 Secrets detected:    1

❌ Commit blocked. Clean or whitelist secrets before committing.
💡 Tip: Use '#secret-ok' for lines or '#secret-file-ok' at top of file to ignore test secrets.
```



## 💡 Tips
- ✅ Add secrets to .gitignore (e.g. .env, .secrets)
- ✅ Customize each pattern’s masked preview with {last4}, {first3}, {length}
- 🧪 Run manually: pre-commit run --all-files
- 🔧 Use disabled_patterns to turn off detections you don’t need


## 📚 Roadmap (Optional Enhancements)
- ⏳ GitHub Actions integration (CI scanning)
- 🌐 Support glob path matching for ignore_paths
- 🔍 Reporting to file (--report CLI)
- 🧼 Auto-redaction/clean-up suggestions


## ❤️ Contributing

Open a PR or file an issue if you’d like to:
- Add more patterns
- Improve masking logic
- Suggest integrations (e.g., VSCode, GitHub)

\
\
Let me know if you'd like this:

- Turned into a Markdown file in your repo directly
- Auto-generated with CLI help via `--help`
- Rendered as a GitHub page with setup gifs/screenshots! 📸
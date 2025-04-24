import re

# Centralized secret detection patterns and their default masked previews
PATTERNS = {
    "AWS Access Key": {
        "pattern": re.compile(r"AKIA[0-9A-Z]{16}"),
        "masked": "[AKIA••••••••••••••••••••••••{last4}]",
    },
    "AWS Secret Key": {
        "pattern": re.compile(
            r"(?i)aws(.{0,20})?(secret|access)?(.{0,20})?['\"][0-9a-zA-Z/+]{40}['\"]"
        ),
        "masked": "[aws-secret •••••••••••••••••••••••••{last4}]",
    },
    "Generic API Key": {
        "pattern": re.compile(
            r"(?i)(api_key|apikey|token|access_token|auth_token)['\"]?\s*[:=]\s*['\"][0-9a-zA-Z\-_]{16,45}['\"]?"
        ),
        "masked": "[api-key •••••••••••••••••••••••••{last4}]",
    },
    "Google API Key": {
        "pattern": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
        "masked": "[google-api-key AIz••••••••••••••••••••••••{last4}]",
    },
    "Slack Token": {
        "pattern": re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,48}"),
        "masked": "[slack-token xox•••••••••••••••{last4}]",
    },
    "GitHub Token": {
        "pattern": re.compile(r"gh[pousr]_[0-9a-zA-Z]{36,255}"),
        "masked": "[github-token gh••••••••••••••••••••••{last4}]",
    },
    "Heroku API Key": {
        "pattern": re.compile(r"(?i)heroku(.{0,20})?['\"][0-9a-f]{32}['\"]"),
        "masked": "[heroku-key he••••••••••••••••••••••••{last4}]",
    },
    "JWT": {
        "pattern": re.compile(r"eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+"),
        "masked": "[JWT-like-token {first3}......{last9}]",
    },
    "OAuth Token": {
        "pattern": re.compile(r"ya29\.[0-9A-Za-z\-_]+"),
        "masked": "[oauth-token ya••••••••••••••••{last4}]",
    },
    "Private Key Start": {
        "pattern": re.compile(r"-----BEGIN (RSA|EC|DSA|PGP|OPENSSH) PRIVATE KEY-----"),
        "masked": "[private-key-block ... END]",
    },
    "MongoDB URI": {
        "pattern": re.compile(r"mongodb(\+srv)?:\/\/[^:@\s]+:[^:@\s]+@[^@\s\/]+"),
        "masked": "[mongodb://***@cluster]",
    },
    "PostgreSQL URI": {
        "pattern": re.compile(r"postgres:\/\/[^:@\s]+:[^:@\s]+@[^@\s\/]+"),
        "masked": "[postgres://***@host]",
    },
    "MySQL URI": {
        "pattern": re.compile(r"mysql:\/\/[^:@\s]+:[^:@\s]+@[^@\s\/]+"),
        "masked": "[mysql://***@host]",
    },
    "Stripe Secret Key": {
        "pattern": re.compile(r"sk_live_[0-9a-zA-Z]{24}"),
        "masked": "[stripe-key sk_live_••••••••••••••{last4}]",
    },
    "SendGrid API Key": {
        "pattern": re.compile(r"SG\.[a-zA-Z0-9_\-]{22,48}\.[a-zA-Z0-9_\-]{22,48}"),
        "masked": "[sendgrid-key SG••••••••••••••••{last4}]",
    },
    "Twilio API Key": {
        "pattern": re.compile(r"SK[0-9a-fA-F]{32}"),
        "masked": "[twilio-key SK••••••••••••••••••••••{last4}]",
    },
    "Password in Code": {
        "pattern": re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*[\"'].*?[\"']"),
        "masked": "[password ••••••••••••••• ({length} chars)]",
    },
    "SSH Password": {
        "pattern": re.compile(
            r"(?i)(sshpass|ssh_password|ssh_pass)\s*[:=]\s*[\"'].*?[\"']"
        ),
        "masked": "[ssh-password ••••••••••••••• ({length} chars)]",
    },
    "Basic Auth in URL": {
        "pattern": re.compile(r"https?:\/\/[^\/\s:@]+:[^\/\s:@]+@[^\/\s]+"),
        "masked": "[http://***:***@host]",
    },
    "Authorization Header": {
        "pattern": re.compile(
            r"(?i)(authorization|auth)\s*[:=]\s*[\'\"]?(bearer|basic)?\s?[a-z0-9\-._~\+\/]+=*[\'\"]?"
        ),
        "masked": "[auth-header •••••••••••••••••••••]",
    },
}

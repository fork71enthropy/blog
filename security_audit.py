#!/usr/bin/env python3
"""
django_security_audit.py
------------------------
Audits the security configuration of a Django project by analysing
settings files and common misconfigurations.

Usage:
    python django_security_audit.py /path/to/your/django/project

Or, from inside the project directory:
    python django_security_audit.py .
"""

import ast
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ── Colours ──────────────────────────────────────────────────────────────────

RESET  = "\033[0m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

def red(s):    return f"{RED}{s}{RESET}"
def yellow(s): return f"{YELLOW}{s}{RESET}"
def green(s):  return f"{GREEN}{s}{RESET}"
def cyan(s):   return f"{CYAN}{s}{RESET}"
def bold(s):   return f"{BOLD}{s}{RESET}"
def dim(s):    return f"{DIM}{s}{RESET}"


# ── Finding model ─────────────────────────────────────────────────────────────

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "OK": 4, "INFO": 5}

@dataclass
class Finding:
    severity: str          # CRITICAL | HIGH | MEDIUM | LOW | OK | INFO
    category: str
    message: str
    detail: str = ""
    fix: str = ""

    def severity_label(self):
        colours = {
            "CRITICAL": RED + BOLD,
            "HIGH":     RED,
            "MEDIUM":   YELLOW,
            "LOW":      YELLOW,
            "OK":       GREEN,
            "INFO":     CYAN,
        }
        c = colours.get(self.severity, "")
        return f"{c}[{self.severity:^8}]{RESET}"

    def __lt__(self, other):
        return SEVERITY_ORDER[self.severity] < SEVERITY_ORDER[other.severity]


# ── Settings extractor ────────────────────────────────────────────────────────

class SettingsReader:
    """
    Best-effort static reader for Django settings files.
    Does NOT execute the file – uses AST parsing + regex fallback.
    """

    def __init__(self, path: Path):
        self.path = path
        self.raw = path.read_text(errors="replace")
        self._values: dict = {}
        self._parse()

    def _parse(self):
        try:
            tree = ast.parse(self.raw)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            try:
                                self._values[target.id] = ast.literal_eval(node.value)
                            except Exception:
                                # Keep raw source snippet for regex checks
                                self._values[target.id] = ast.get_source_segment(
                                    self.raw, node.value
                                )
        except SyntaxError:
            pass  # fall back to regex only

    def get(self, key, default=None):
        return self._values.get(key, default)

    def __contains__(self, key):
        return key in self._values

    def raw_contains(self, pattern: str) -> bool:
        return bool(re.search(pattern, self.raw))

    def raw_find(self, pattern: str) -> Optional[re.Match]:
        return re.search(pattern, self.raw)


# ── Checks ────────────────────────────────────────────────────────────────────

def check_secret_key(s: SettingsReader) -> list[Finding]:
    findings = []
    sk = s.get("SECRET_KEY", "")
    sk_str = str(sk) if sk else ""

    if not sk_str:
        findings.append(Finding(
            "CRITICAL", "SECRET_KEY",
            "SECRET_KEY not found in settings",
            "Your Django application cannot run securely without a secret key.",
            "Generate one with: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\"",
        ))
    elif re.search(r"(django-insecure|changeme|secret|password|12345)", sk_str, re.I):
        findings.append(Finding(
            "CRITICAL", "SECRET_KEY",
            "SECRET_KEY looks like a placeholder or insecure default",
            f"Value: {sk_str[:40]}…",
            "Replace with a strong random key and store it in an environment variable, never in version control.",
        ))
    elif len(sk_str) < 40:
        findings.append(Finding(
            "HIGH", "SECRET_KEY",
            "SECRET_KEY is unusually short (< 40 chars)",
            f"Length: {len(sk_str)} characters",
            "Use a key of at least 50 random characters.",
        ))
    else:
        findings.append(Finding("OK", "SECRET_KEY", "SECRET_KEY looks acceptable"))

    # Check if hardcoded (not pulled from env)
    if sk_str and not s.raw_contains(r"(os\.environ|os\.getenv|get_secret|config\()"):
        findings.append(Finding(
            "HIGH", "SECRET_KEY",
            "SECRET_KEY appears to be hardcoded – not loaded from environment",
            "",
            "Use os.environ['SECRET_KEY'] or python-decouple / django-environ.",
        ))
    return findings


def check_debug(s: SettingsReader) -> list[Finding]:
    debug = s.get("DEBUG")
    if debug is True:
        return [Finding(
            "CRITICAL", "DEBUG",
            "DEBUG = True – NEVER use in production",
            "This exposes stack traces, SQL queries, and environment variables to end users.",
            "Set DEBUG = False in production and control via env variable: DEBUG = os.getenv('DEBUG', 'False') == 'True'",
        )]
    elif debug is False:
        return [Finding("OK", "DEBUG", "DEBUG = False ✓")]
    else:
        return [Finding(
            "MEDIUM", "DEBUG",
            "DEBUG value is dynamic or unknown – verify it evaluates to False in production",
            f"Found: {debug}",
        )]


def check_allowed_hosts(s: SettingsReader) -> list[Finding]:
    ah = s.get("ALLOWED_HOSTS", [])
    if isinstance(ah, list):
        if not ah:
            return [Finding(
                "HIGH", "ALLOWED_HOSTS",
                "ALLOWED_HOSTS is empty",
                "Requests will be rejected in production when DEBUG=False.",
                "Set ALLOWED_HOSTS to your domain(s): ['example.com', 'www.example.com']",
            )]
        if "*" in ah:
            return [Finding(
                "HIGH", "ALLOWED_HOSTS",
                "ALLOWED_HOSTS contains '*' – accepts any hostname",
                "This exposes your app to Host header attacks.",
                "Replace '*' with your actual domain names.",
            )]
        return [Finding("OK", "ALLOWED_HOSTS", f"ALLOWED_HOSTS set to {ah}")]
    return [Finding("INFO", "ALLOWED_HOSTS", f"ALLOWED_HOSTS is dynamic: {ah}")]


def check_database(s: SettingsReader) -> list[Finding]:
    findings = []
    db = s.get("DATABASES", {})

    # SQLite in production
    db_str = str(db)
    if "sqlite" in db_str.lower():
        findings.append(Finding(
            "MEDIUM", "DATABASE",
            "SQLite detected – not recommended for production",
            "SQLite has no access control, limited concurrency, and is often committed to version control.",
            "Use PostgreSQL or MySQL for production workloads.",
        ))

    # Hardcoded credentials
    if re.search(r"'PASSWORD'\s*:\s*'[^']{2,}'", db_str):
        findings.append(Finding(
            "HIGH", "DATABASE",
            "Database PASSWORD appears to be hardcoded in settings",
            "",
            "Load credentials from environment variables.",
        ))

    # db.sqlite3 tracked by git
    sqlite_path = Path(s.path.parent) / "db.sqlite3"
    gitignore = s.path.parent / ".gitignore"
    root_gitignore = s.path.parent.parent / ".gitignore"
    ignored = False
    for gi in [gitignore, root_gitignore]:
        if gi.exists() and "db.sqlite3" in gi.read_text():
            ignored = True
    if sqlite_path.exists() and not ignored:
        findings.append(Finding(
            "HIGH", "DATABASE",
            "db.sqlite3 exists and is NOT listed in .gitignore",
            "If committed to git, your entire database (users, sessions, data) is exposed.",
            "Add 'db.sqlite3' to .gitignore immediately and remove it from git history if already committed.",
        ))

    if not findings:
        findings.append(Finding("OK", "DATABASE", "No obvious database misconfigurations found"))
    return findings


def check_https_settings(s: SettingsReader) -> list[Finding]:
    findings = []
    checks = [
        ("SECURE_SSL_REDIRECT",           True,  "HIGH",   "HTTPS redirect disabled",
         "Set SECURE_SSL_REDIRECT = True in production to force HTTPS."),
        ("SECURE_HSTS_SECONDS",           None,  "MEDIUM", "HSTS not configured",
         "Set SECURE_HSTS_SECONDS = 31536000 (1 year) to enforce HTTPS via browsers."),
        ("SECURE_HSTS_INCLUDE_SUBDOMAINS", True, "LOW",    "HSTS does not cover subdomains",
         "Set SECURE_HSTS_INCLUDE_SUBDOMAINS = True."),
        ("SECURE_HSTS_PRELOAD",           True,  "LOW",    "HSTS preload not enabled",
         "Set SECURE_HSTS_PRELOAD = True once HSTS is properly configured."),
        ("SECURE_CONTENT_TYPE_NOSNIFF",   True,  "MEDIUM", "X-Content-Type-Options header missing",
         "Set SECURE_CONTENT_TYPE_NOSNIFF = True."),
        ("SECURE_BROWSER_XSS_FILTER",     True,  "LOW",    "X-XSS-Protection header not set",
         "Set SECURE_BROWSER_XSS_FILTER = True."),
    ]
    for key, expected, sev, msg, fix in checks:
        val = s.get(key)
        if expected is True and val is not True:
            findings.append(Finding(sev, "HTTPS/HEADERS", f"{key}: {msg}", f"Current: {val}", fix))
        elif expected is None and (val is None or val == 0):
            findings.append(Finding(sev, "HTTPS/HEADERS", f"{key}: {msg}", f"Current: {val}", fix))
        else:
            findings.append(Finding("OK", "HTTPS/HEADERS", f"{key} = {val} ✓"))
    return findings


def check_cookies(s: SettingsReader) -> list[Finding]:
    findings = []
    cookie_checks = [
        ("SESSION_COOKIE_SECURE",   True, "HIGH",   "Session cookie sent over HTTP",
         "Set SESSION_COOKIE_SECURE = True so the session cookie is only sent over HTTPS."),
        ("SESSION_COOKIE_HTTPONLY", True, "HIGH",   "Session cookie accessible via JavaScript",
         "Set SESSION_COOKIE_HTTPONLY = True to prevent XSS from stealing sessions."),
        ("CSRF_COOKIE_SECURE",      True, "HIGH",   "CSRF cookie sent over HTTP",
         "Set CSRF_COOKIE_SECURE = True."),
        ("CSRF_COOKIE_HTTPONLY",    True, "MEDIUM", "CSRF cookie accessible via JavaScript",
         "Set CSRF_COOKIE_HTTPONLY = True."),
    ]
    for key, expected, sev, msg, fix in cookie_checks:
        val = s.get(key)
        if val is not True:
            findings.append(Finding(sev, "COOKIES", f"{key}: {msg}", f"Current: {val}", fix))
        else:
            findings.append(Finding("OK", "COOKIES", f"{key} = True ✓"))

    # Session age
    age = s.get("SESSION_COOKIE_AGE")
    if age is not None and isinstance(age, int) and age > 86400 * 30:
        findings.append(Finding(
            "LOW", "COOKIES",
            f"SESSION_COOKIE_AGE is very long ({age // 86400} days)",
            "",
            "Consider shortening session lifetime to reduce exposure from stolen cookies.",
        ))
    return findings


def check_csrf(s: SettingsReader) -> list[Finding]:
    findings = []
    middleware = s.get("MIDDLEWARE", [])
    if isinstance(middleware, list):
        if not any("CsrfViewMiddleware" in m for m in middleware):
            findings.append(Finding(
                "CRITICAL", "CSRF",
                "CsrfViewMiddleware is NOT in MIDDLEWARE",
                "Your application has no CSRF protection.",
                "Add 'django.middleware.csrf.CsrfViewMiddleware' to MIDDLEWARE.",
            ))
        else:
            findings.append(Finding("OK", "CSRF", "CsrfViewMiddleware present ✓"))
    else:
        findings.append(Finding("INFO", "CSRF", "MIDDLEWARE is dynamic – verify CsrfViewMiddleware is included"))
    return findings


def check_installed_apps(s: SettingsReader) -> list[Finding]:
    findings = []
    apps = s.get("INSTALLED_APPS", [])
    if not isinstance(apps, list):
        return [Finding("INFO", "INSTALLED_APPS", "INSTALLED_APPS is dynamic – skipping app checks")]

    dangerous = {
        "debug_toolbar": ("MEDIUM", "django-debug-toolbar is installed",
                          "Ensure it is gated behind DEBUG=True and never active in production."),
        "django_extensions": ("LOW", "django-extensions is installed",
                              "Some commands (shell_plus, etc.) can be dangerous if accessible in production."),
    }
    for app in apps:
        for pattern, (sev, msg, fix) in dangerous.items():
            if pattern in app:
                findings.append(Finding(sev, "INSTALLED_APPS", msg, f"App: {app}", fix))

    if not findings:
        findings.append(Finding("OK", "INSTALLED_APPS", "No obviously dangerous apps detected"))
    return findings


def check_email(s: SettingsReader) -> list[Finding]:
    backend = s.get("EMAIL_BACKEND", "")
    if "console" in str(backend).lower():
        return [Finding(
            "MEDIUM", "EMAIL",
            "EMAIL_BACKEND is set to ConsoleEmailBackend",
            "Emails will only be printed to stdout – not delivered in production.",
            "Set a real SMTP backend for production.",
        )]
    if "dummy" in str(backend).lower():
        return [Finding(
            "HIGH", "EMAIL",
            "EMAIL_BACKEND is set to DummyEmailBackend – emails are silently discarded",
            "",
            "Configure a real email backend for production.",
        )]
    return []


def check_password_validators(s: SettingsReader) -> list[Finding]:
    validators = s.get("AUTH_PASSWORD_VALIDATORS", [])
    if not validators:
        return [Finding(
            "HIGH", "PASSWORDS",
            "AUTH_PASSWORD_VALIDATORS is empty – no password strength enforcement",
            "",
            "Configure at least UserAttributeSimilarityValidator, MinimumLengthValidator, and CommonPasswordValidator.",
        )]
    if isinstance(validators, list) and len(validators) < 3:
        return [Finding(
            "MEDIUM", "PASSWORDS",
            f"Only {len(validators)} password validator(s) configured",
            "",
            "Django ships with 4 validators – consider enabling all of them.",
        )]
    return [Finding("OK", "PASSWORDS", f"{len(validators)} password validator(s) configured ✓")]


def check_logging(s: SettingsReader) -> list[Finding]:
    logging_cfg = s.get("LOGGING")
    if not logging_cfg:
        return [Finding(
            "LOW", "LOGGING",
            "No LOGGING configuration found",
            "Security events (failed logins, permission denials) won't be captured.",
            "Configure Django's logging to capture django.security and django.request at WARNING level.",
        )]
    return [Finding("OK", "LOGGING", "LOGGING configuration present ✓")]


def check_x_frame_options(s: SettingsReader) -> list[Finding]:
    xfo = s.get("X_FRAME_OPTIONS", "SAMEORIGIN")
    middleware = s.get("MIDDLEWARE", [])
    has_middleware = isinstance(middleware, list) and any("XFrameOptionsMiddleware" in m for m in middleware)
    if not has_middleware:
        return [Finding(
            "MEDIUM", "CLICKJACKING",
            "XFrameOptionsMiddleware is NOT in MIDDLEWARE",
            "Your pages may be embeddable in iframes (clickjacking risk).",
            "Add 'django.middleware.clickjacking.XFrameOptionsMiddleware' to MIDDLEWARE.",
        )]
    if str(xfo).upper() == "ALLOWALL":
        return [Finding(
            "HIGH", "CLICKJACKING",
            "X_FRAME_OPTIONS = ALLOWALL – all framing permitted",
            "",
            "Use DENY or SAMEORIGIN.",
        )]
    return [Finding("OK", "CLICKJACKING", f"X_FRAME_OPTIONS = {xfo} with middleware ✓")]


def check_static_media(s: SettingsReader) -> list[Finding]:
    findings = []
    media_root = s.get("MEDIA_ROOT", "")
    if not media_root:
        findings.append(Finding(
            "LOW", "STATIC/MEDIA",
            "MEDIA_ROOT is not set",
            "",
            "Configure MEDIA_ROOT to a directory outside the project for uploaded files.",
        ))
    # Check for file upload validation
    if not s.raw_contains(r"(FileExtensionValidator|validate_file_extension|ALLOWED_IMAGE_TYPES)"):
        findings.append(Finding(
            "LOW", "STATIC/MEDIA",
            "No file upload validation detected in settings",
            "",
            "Validate uploaded file types with FileExtensionValidator and consider virus scanning.",
        ))
    return findings


def check_env_file(project_root: Path) -> list[Finding]:
    findings = []
    env_file = project_root / ".env"
    gitignore_paths = list(project_root.rglob(".gitignore"))

    env_in_gitignore = False
    for gi in gitignore_paths:
        content = gi.read_text(errors="replace")
        if re.search(r"^\.env$|^\.env\b", content, re.MULTILINE):
            env_in_gitignore = True
            break

    if env_file.exists():
        if not env_in_gitignore:
            findings.append(Finding(
                "CRITICAL", ".ENV FILE",
                ".env file found but NOT listed in .gitignore",
                f"Path: {env_file}",
                "Add '.env' to .gitignore immediately. If already committed, rotate all secrets.",
            ))
        else:
            findings.append(Finding("OK", ".ENV FILE", ".env is present and listed in .gitignore ✓"))
    return findings


def check_requirements(project_root: Path) -> list[Finding]:
    """Check for known vulnerable / outdated patterns in requirements."""
    findings = []
    req_files = list(project_root.rglob("requirements*.txt")) + list(project_root.rglob("Pipfile"))
    if not req_files:
        findings.append(Finding(
            "INFO", "DEPENDENCIES",
            "No requirements.txt / Pipfile found – cannot audit dependencies",
            "",
            "Run 'pip-audit' or 'safety check' regularly to detect vulnerable packages.",
        ))
        return findings

    for rf in req_files:
        content = rf.read_text(errors="replace")
        # Unpinned dependencies
        unpinned = [l.strip() for l in content.splitlines()
                    if l.strip() and not l.startswith("#")
                    and not re.search(r"[=<>!~]", l)]
        if unpinned:
            findings.append(Finding(
                "LOW", "DEPENDENCIES",
                f"{rf.name}: {len(unpinned)} unpinned package(s)",
                ", ".join(unpinned[:5]) + ("…" if len(unpinned) > 5 else ""),
                "Pin all dependencies to exact versions for reproducible and auditable builds.",
            ))

    findings.append(Finding(
        "INFO", "DEPENDENCIES",
        "Run 'pip-audit' or 'safety check' for CVE scanning",
        "Static analysis cannot detect known CVEs.",
        "pip install pip-audit && pip-audit",
    ))
    return findings


# ── Git history check ─────────────────────────────────────────────────────────

def check_git_secrets(project_root: Path) -> list[Finding]:
    """Warn if sensitive patterns might be in git history."""
    git_dir = project_root / ".git"
    if not git_dir.exists():
        return [Finding("INFO", "GIT", "Not a git repository – skipping history checks")]

    findings = [Finding(
        "INFO", "GIT",
        "Run 'git log -p | grep -E \"SECRET_KEY|PASSWORD|AWS_\"' to check for committed secrets",
        "",
        "Use 'git-secrets' or 'trufflehog' for automated history scanning.",
    )]
    return findings


# ── Settings file finder ──────────────────────────────────────────────────────

def find_settings_files(root: Path) -> list[Path]:
    candidates = list(root.rglob("settings.py")) + list(root.rglob("settings_prod.py")) \
               + list(root.rglob("settings/base.py")) + list(root.rglob("settings/production.py"))
    # Exclude virtualenvs
    return [p for p in candidates if not any(
        part in p.parts for part in ("venv", ".venv", "env", "site-packages", "node_modules")
    )]


# ── Report ────────────────────────────────────────────────────────────────────

def print_report(all_findings: list[Finding], settings_files: list[Path]):
    counts = {k: 0 for k in SEVERITY_ORDER}
    for f in all_findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    print()
    print(bold("=" * 66))
    print(bold("  🔒  Django Security Audit Report"))
    print(bold("=" * 66))

    if settings_files:
        print(dim(f"\n  Settings analysed:"))
        for sf in settings_files:
            print(dim(f"    • {sf}"))

    print()
    for finding in sorted(all_findings):
        if finding.severity == "OK":
            continue  # Printed in summary section
        icon = {"CRITICAL": "💀", "HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "ℹ️ "}.get(finding.severity, "  ")
        print(f"  {icon}  {finding.severity_label()}  {bold(finding.category)}")
        print(f"       {finding.message}")
        if finding.detail:
            print(dim(f"       Detail : {finding.detail}"))
        if finding.fix:
            print(green(f"       Fix    : {finding.fix}"))
        print()

    # OK items (collapsed)
    ok_items = [f for f in all_findings if f.severity == "OK"]
    if ok_items:
        print(green(f"  ✅  {len(ok_items)} check(s) passed:"))
        for f in ok_items:
            print(green(f"       • [{f.category}] {f.message}"))
        print()

    # Summary
    print(bold("─" * 66))
    print(bold("  Summary"))
    print(bold("─" * 66))
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        n = counts.get(sev, 0)
        if n:
            label = {
                "CRITICAL": red(f"  {n:3}  CRITICAL"),
                "HIGH":     red(f"  {n:3}  HIGH"),
                "MEDIUM":   yellow(f"  {n:3}  MEDIUM"),
                "LOW":      yellow(f"  {n:3}  LOW"),
                "INFO":     cyan(f"  {n:3}  INFO"),
            }[sev]
            print(label)
    print(green(f"  {counts.get('OK', 0):3}  OK / passed"))
    print(bold("=" * 66))
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def audit(project_root: Path):
    print(cyan(f"\n  Scanning: {project_root.resolve()}\n"))

    settings_files = find_settings_files(project_root)
    all_findings: list[Finding] = []

    if not settings_files:
        print(yellow("  ⚠  No settings.py found. Pass the project root as argument."))
        sys.exit(1)

    for sf in settings_files:
        s = SettingsReader(sf)
        all_findings += check_secret_key(s)
        all_findings += check_debug(s)
        all_findings += check_allowed_hosts(s)
        all_findings += check_database(s)
        all_findings += check_https_settings(s)
        all_findings += check_cookies(s)
        all_findings += check_csrf(s)
        all_findings += check_installed_apps(s)
        all_findings += check_email(s)
        all_findings += check_password_validators(s)
        all_findings += check_logging(s)
        all_findings += check_x_frame_options(s)
        all_findings += check_static_media(s)

    all_findings += check_env_file(project_root)
    all_findings += check_requirements(project_root)
    all_findings += check_git_secrets(project_root)

    print_report(all_findings, settings_files)

    critical = sum(1 for f in all_findings if f.severity == "CRITICAL")
    high     = sum(1 for f in all_findings if f.severity == "HIGH")
    sys.exit(1 if (critical + high) > 0 else 0)


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    if not root.exists():
        print(red(f"  Path not found: {root}"))
        sys.exit(1)
    audit(root)

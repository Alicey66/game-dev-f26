"""Name the exact setup problem and the command or link that fixes it.

Findings name the project, location or model involved, never a key's value.
"""

from dataclasses import dataclass
from datetime import date
import re

CREDITS_PAGE = "https://courseworks2.columbia.edu/courses/258228/pages/google-cloud-credits"
DEFAULT_MODEL = "gemini-3.5-flash-lite"
CAPABLE_MODEL = "gemini-3.8-flash"
VERTEX_MODELS = "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions"
# Gemini retirement dates from VERTEX_MODELS, checked 2026-10-17; matched as COURSE_MODEL prefixes.
RETIREMENTS = (
    ("gemini-1.", date(2025, 9, 24)),
    ("gemini-2.0-", date(2026, 6, 1)),
    ("gemini-2.5-", date(2026, 10, 20)),
    ("gemini-3.6-flash", date(2026, 11, 19)),
    ("gemini-3.7-flash", date(2027, 1, 28)),
)
WARN_DAYS = 60
REQUIRED = {
    "vertex": ("GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION", "COURSE_MODEL"),
    "anthropic": ("ANTHROPIC_API_KEY", "COURSE_MODEL"),
    "openai": ("OPENAI_API_KEY", "COURSE_MODEL"),
}
KEYS = {
    "ANTHROPIC_API_KEY": ("Anthropic", "sk-ant-", "https://platform.claude.com/settings/keys"),
    "OPENAI_API_KEY": ("OpenAI", "sk-", "https://platform.openai.com/api-keys"),
}
EXAMPLES = {"GOOGLE_CLOUD_PROJECT": "your-project-id", "GOOGLE_CLOUD_LOCATION": "global"}
MODEL_LISTS = {
    "vertex": VERTEX_MODELS,
    "anthropic": "https://platform.claude.com/docs/en/about-claude/models/overview",
    "openai": "https://platform.openai.com/docs/models",
}
FAMILIES = {"vertex": ("Gemini", re.compile(r"gemini")), "anthropic": ("Claude", re.compile(r"claude")),
            "openai": ("OpenAI", re.compile(r"gpt|o\d|chatgpt|codex"))}
USE_FAMILY = {"vertex": f"Use a Gemini model: export COURSE_MODEL='{DEFAULT_MODEL}'",
              "anthropic": f"Use a Claude model from {MODEL_LISTS['anthropic']}",
              "openai": f"Use an OpenAI model from {MODEL_LISTS['openai']}"}
CALL_FAMILY = {"vertex": "and the course Google credit.", "anthropic": "and an Anthropic API key.",
               "openai": "and an OpenAI API key."}
PLACEHOLDER = re.compile(r"your[_-]|replace[_-]with|placeholder|[<>\[\]]", re.I)
PROJECT_ID = re.compile(r"[a-z][a-z0-9-]{4,28}[a-z0-9]")
LOCATION = re.compile(r"global|us|eu|[a-z]+-[a-z]+\d+")
SECRETS = re.compile(
    r"sk-[A-Za-z0-9_*-]{4,}"  # OpenAI and Anthropic keys
    r"|AIza[0-9A-Za-z_-]{10,}"  # Google API keys
    r"|ya29\.[\w.-]+"  # Google access tokens
    r"|1//[\w.-]+"  # Google refresh tokens
    r"|Bearer\s+\S+"  # authorization headers
    r"|\"?private_key\"?\s*[:=].*",  # service-account key material, to the end of the line
    re.I,
)
SECRET_NAMES = re.compile(r"KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL", re.I)
SCREENSHOT = ("Message your instructor and TAs with a screenshot of this output.",)


@dataclass(frozen=True)
class Finding:
    level: str  # FAIL stops the live call; WARN does not.
    problem: str
    fix: tuple[str, ...] = ()


def render(label: str, finding: Finding) -> str:
    lines = [f"{finding.level} {label}: {finding.problem}"]
    lines += [("  Fix: " if i == 0 else "       ") + line for i, line in enumerate(finding.fix)]
    return "\n".join(lines)


def check_settings(provider: str, env, today: date | None = None) -> list[Finding]:
    """Problems visible in the settings alone, found before any billable call."""
    today = today or date.today()
    findings = []
    for name in REQUIRED.get(provider, ()):
        value = env.get(name, "").strip()
        if name in KEYS:
            findings += _check_key(name, value)
        elif not value:
            findings.append(Finding("FAIL", f"{name} is not set.", (_export(name, provider), _step(8, provider))))
        elif PLACEHOLDER.search(value):
            findings.append(Finding("FAIL", f"{name} is still a placeholder ('{value}').",
                                    (_export(name, provider), _step(8, provider))))
        elif name == "GOOGLE_CLOUD_PROJECT" and not PROJECT_ID.fullmatch(value):
            findings.append(Finding("FAIL", f"GOOGLE_CLOUD_PROJECT '{value}' is not a project ID; it may be "
                                    "the project's name.", (
                "List your projects and copy the PROJECT_ID column: gcloud projects list",
                "export GOOGLE_CLOUD_PROJECT='your-project-id'")))
        elif name == "GOOGLE_CLOUD_LOCATION" and not LOCATION.fullmatch(value):
            findings.append(Finding("FAIL", f"GOOGLE_CLOUD_LOCATION '{value}' is not a Vertex AI location.",
                                    ("export GOOGLE_CLOUD_LOCATION='global'",)))
        elif name == "COURSE_MODEL":
            findings += _check_model(value, provider, today)
    return findings


def _check_key(name: str, value: str) -> list[Finding]:
    company, prefix, _ = KEYS[name]
    load = _load_key(name)
    if not value:
        return [Finding("FAIL", f"{name} is not set.", (load,))]
    if PLACEHOLDER.search(value):
        return [Finding("FAIL", f"{name} still holds a placeholder.", (load,))]
    if not value.startswith(prefix):
        return [Finding("WARN", f"{name} does not look like an {company} API key; those start with {prefix}.",
                        (load,))]
    return []


def _load_key(name: str) -> str:
    return (f"Create a key at {KEYS[name][2]}, then load it into this shell as the README describes; "
            "keep it out of files Git tracks.")


def _check_model(model: str, provider: str, today: date) -> list[Finding]:
    for owner, (family, pattern) in FAMILIES.items():
        if owner != provider and pattern.match(model.lower()):
            return [Finding("FAIL", f"COURSE_MODEL {model} is a {family} model, and --provider {provider} "
                            f"calls {FAMILIES[provider][0]} models.", (
                USE_FAMILY[provider], f"or call {family} models with --provider {owner} {CALL_FAMILY[owner]}"))]
    for prefix, retired in RETIREMENTS:
        if model.startswith(prefix):
            fix = (f"export COURSE_MODEL='{DEFAULT_MODEL}'", f"Current models: {VERTEX_MODELS}")
            if today >= retired:
                return [Finding("FAIL", f"COURSE_MODEL {model} was retired on {retired}; calls to it fail.", fix)]
            if (retired - today).days <= WARN_DAYS:
                return [Finding("WARN", f"COURSE_MODEL {model} retires on {retired}; calls to it will fail "
                                "after that.", fix)]
    return []


def _export(name: str, provider: str) -> str:
    example = DEFAULT_MODEL if name == "COURSE_MODEL" and provider == "vertex" else EXAMPLES.get(name, "model-id")
    return f"export {name}='{example}'"


def _step(number: int, provider: str) -> str:
    if provider != "vertex":
        return f"Model IDs: {MODEL_LISTS.get(provider, VERTEX_MODELS)}"
    return f"Credits page, step {number}: {CREDITS_PAGE}"


def diagnose(error: BaseException, provider: str, env) -> Finding:
    """The problem behind a failed live call, with its fix."""
    for read in (_google, _openai, _anthropic, _connection, _narration):
        finding = read(error, provider, env)
        if finding:
            return finding
    return Finding("FAIL", f"{type(error).__name__}: {_scrub(str(error), env)[:300]}", SCREENSHOT)


def _google(error, provider, env):
    from google.auth.exceptions import DefaultCredentialsError, RefreshError
    from google.genai.errors import APIError

    login = "Sign in: gcloud auth application-default login (credits page, step 7)"
    if isinstance(error, DefaultCredentialsError):
        if env.get("GOOGLE_APPLICATION_CREDENTIALS"):
            return Finding("FAIL", "GOOGLE_APPLICATION_CREDENTIALS points to a sign-in file Google cannot use.",
                           ("Run: unset GOOGLE_APPLICATION_CREDENTIALS", login, f"Credits page: {CREDITS_PAGE}"))
        return Finding("FAIL", "this computer has no Google sign-in for Vertex AI.",
                       (login, "Then run this check again.", f"Credits page: {CREDITS_PAGE}"))
    if isinstance(error, RefreshError):
        return Finding("FAIL", "your Google sign-in has expired or was revoked.", (login, "Then run this check again."))
    if not isinstance(error, APIError):
        return None
    project = env.get("GOOGLE_CLOUD_PROJECT", "")
    location = env.get("GOOGLE_CLOUD_LOCATION", "")
    model = env.get("COURSE_MODEL", "")
    body = error.details if isinstance(error.details, dict) else {}
    info = body.get("error") if isinstance(body.get("error"), dict) else {}
    reason, meta = next(((d.get("reason"), d.get("metadata") or {}) for d in info.get("details", [])
                         if str(d.get("@type", "")).endswith("ErrorInfo")), (None, {}))
    again = "Then wait a few minutes and run this check again."
    if reason == "BILLING_DISABLED":
        url = meta.get("consoleUrl") or f"https://console.cloud.google.com/billing/linkedaccount?project={project}"
        return Finding("FAIL", f"billing is off for project {project}.", (
            "Link the project to your course billing account (credits page, step 4):", url, again))
    if reason == "SERVICE_DISABLED":
        url = meta.get("activationUrl") or (
            f"https://console.cloud.google.com/apis/library/aiplatform.googleapis.com?project={project}")
        return Finding("FAIL", f"the Vertex AI API (the console now calls it Agent Platform API) is off for "
                       f"project {project}.", ("Turn it on (credits page, step 5):", url, again))
    if reason == "CONSUMER_INVALID":
        return Finding("FAIL", f"project {project} does not exist, or your Google account cannot use it.", (
            "List the projects your account can use: gcloud projects list",
            "Set GOOGLE_CLOUD_PROJECT to your course project's PROJECT_ID (credits page, step 4).",
            "Check which account is signed in: gcloud auth list"))
    if reason == "IAM_PERMISSION_DENIED":
        return Finding("FAIL", f"your Google account lacks permission to call Vertex AI in project {project}.", (
            "Use your own course project (credits page, step 4), or ask the project's owner for the "
            "Vertex AI User role.",))
    if reason == "USER_PROJECT_DENIED":
        return Finding("FAIL", "your Google sign-in bills API usage to a project you cannot use.", (
            f"Run: gcloud auth application-default set-quota-project {project}",))
    if error.code == 404 and not info:
        return Finding("FAIL", f"GOOGLE_CLOUD_LOCATION '{location}' is not a Vertex AI location.", (
            "export GOOGLE_CLOUD_LOCATION='global'",))
    if error.code == 404:
        return Finding("FAIL", f"model {model} is not available to project {project} in location {location}.", (
            f"export COURSE_MODEL='{DEFAULT_MODEL}'", "export GOOGLE_CLOUD_LOCATION='global'",
            f"Current models: {VERTEX_MODELS}"))
    if error.code == 429:
        return Finding("FAIL", "Google is limiting requests from this project for the moment (429).", (
            "Wait a minute, then run this check again.",
            "GOOGLE_CLOUD_LOCATION='global' spreads requests across regions."))
    if error.code == 401:
        return Finding("FAIL", "Google rejected your sign-in.", (login,))
    if error.code >= 500:
        return Finding("FAIL", f"Google's service had a temporary problem ({error.code}).", (
            "Wait a few minutes, then run this check again.",))
    return Finding("FAIL", f"Google refused the request ({error.code}): {_scrub(error.message or '', env)[:300]}",
                   SCREENSHOT)


def _openai(error, provider, env):
    import openai

    if not isinstance(error, openai.OpenAIError):
        return None
    model = env.get("COURSE_MODEL", "")
    if isinstance(error, openai.AuthenticationError):
        return Finding("FAIL", "OpenAI rejected the key in OPENAI_API_KEY.", (_load_key("OPENAI_API_KEY"),))
    if isinstance(error, openai.RateLimitError) and getattr(error, "code", None) == "insufficient_quota":
        return Finding("FAIL", "this OpenAI account has no API credit.", (
            "OpenAI bills API use separately from ChatGPT Plus. Add API credit at",
            "https://platform.openai.com/settings/organization/billing",
            f"or use the course Google credit with --provider vertex: {CREDITS_PAGE}"))
    if isinstance(error, openai.RateLimitError):
        return Finding("FAIL", "OpenAI is limiting requests from this account for the moment (429).", (
            "Wait a minute, then run this check again.",))
    if isinstance(error, openai.NotFoundError):
        return Finding("FAIL", f"OpenAI cannot find model {model} for this account.", (
            f"Choose a model ID from {MODEL_LISTS['openai']}", "export COURSE_MODEL='model-id'"))
    if isinstance(error, openai.InternalServerError):
        return Finding("FAIL", f"OpenAI's service had a temporary problem ({error.status_code}).", (
            "Wait a few minutes, then run this check again.",))
    if isinstance(error, openai.APIStatusError):
        return Finding("FAIL", f"OpenAI refused the request ({error.status_code}): {_scrub(error.message, env)[:300]}",
                       SCREENSHOT)
    if isinstance(error, openai.APIConnectionError):
        return _unreachable("OpenAI")
    return None


def _anthropic(error, provider, env):
    import anthropic

    if not isinstance(error, anthropic.AnthropicError):
        return None
    model = env.get("COURSE_MODEL", "")
    if isinstance(error, anthropic.AuthenticationError):
        return Finding("FAIL", "Anthropic rejected the key in ANTHROPIC_API_KEY.",
                       (_load_key("ANTHROPIC_API_KEY"),))
    if isinstance(error, anthropic.APIStatusError):
        said = f"{error.message} {error.body}".lower()
        if error.status_code == 402 or "credit balance" in said:
            return Finding("FAIL", "this Anthropic account has no API credit.", (
                "Add credit at https://platform.claude.com/settings/billing",
                f"or use the course Google credit with --provider vertex: {CREDITS_PAGE}"))
        if isinstance(error, anthropic.NotFoundError):
            return Finding("FAIL", f"Anthropic cannot find model {model} for this account.", (
                f"Choose a model ID from {MODEL_LISTS['anthropic']}", "export COURSE_MODEL='model-id'"))
        if error.status_code == 429 or error.status_code >= 500:
            return Finding("FAIL", f"Anthropic is busy or limiting requests for the moment ({error.status_code}).", (
                "Wait a minute, then run this check again.",))
        return Finding("FAIL", f"Anthropic refused the request ({error.status_code}): {_scrub(error.message, env)[:300]}",
                       SCREENSHOT)
    if isinstance(error, anthropic.APIConnectionError):
        return _unreachable("Anthropic")
    return None


def _connection(error, provider, env):
    import httpx

    if isinstance(error, httpx.TransportError):
        return _unreachable({"vertex": "Google Vertex AI"}.get(provider, provider))
    return None


def _unreachable(service: str) -> Finding:
    return Finding("FAIL", f"this computer could not reach {service}.", (
        "Check your internet connection, then run this check again.",
        "Some networks block cloud APIs; if this one does, try another network."))


def _narration(error, provider, env):
    from .narrator import NarrationError

    if not isinstance(error, NarrationError):
        return None
    if str(error).startswith("Configure"):
        return Finding("FAIL", str(error), (_step(8, provider),))
    stronger = f"a more capable model, such as {CAPABLE_MODEL}" if provider == "vertex" else "a more capable model"
    return Finding("FAIL", f"the model answered, but its reply failed the narrator's checks: {error}", (
        "Run the check again; model replies vary.",
        f"If it keeps failing, compare {stronger} on the same question."))


def _scrub(text: str, env) -> str:
    """Hide key-shaped text and the exact value of every key-like setting before printing."""
    for name, value in env.items():
        if SECRET_NAMES.search(name) and len(value) >= 6:
            text = text.replace(value, "[key hidden]")
    return SECRETS.sub("[key hidden]", text)

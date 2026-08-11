# Security Policy

## No secrets in the repository

- Never commit API keys, tokens, credentials, or `.env` files. There are
  currently no secrets anywhere in this project — keep it that way; any
  future integration (e.g. an LLM call for the `triplets` stub) must read
  keys from an environment variable, never hardcode or commit one.
- If a secret is ever committed, treat it as compromised immediately:
  rotate/revoke it at the provider. Removing it from git history after the
  fact does not undo exposure — assume it was scraped.
- Run a secret scanner (e.g. `gitleaks` or `detect-secrets`) before pushing,
  and ideally in CI, so this is caught automatically rather than by review.
- Dependencies: keep the runtime dependency list at zero unless a change
  genuinely needs one, run `pip-audit` in CI to catch known CVEs, and use
  Dependabot with a cooldown period on version updates so a freshly
  published (possibly compromised) release isn't pulled in immediately.

## User text is sensitive by default

The whole point of this tool is to process text the user may not want
shared. That text — **both the input and the slopified output, at every
stage** — must be treated as private data:

- **Never transmit input or output text to any external service** (LLM
  API, analytics, telemetry, crash reporting) **without explicit, informed,
  per-use consent obtained beforehand.** Not a one-time setting buried in a
  config file — ask before the first send, every session, unless the user
  has explicitly asked for a persistent opt-in.
- This applies to features that don't exist yet, not just what's here
  today. The `triplets` transform is stubbed out precisely because a
  quality implementation would need real paraphrasing (likely an LLM
  call) — if that gets built, it must prompt for consent before any text
  leaves the machine, and the CLI/README must say plainly that that mode
  sends text off-device. Default behavior must stay fully local.
- No default telemetry or analytics that includes text content, file
  names, or file paths.
- If a web frontend is ever built and text is processed server-side, that
  is a network transmission and needs the same explicit consent — don't
  let "it's just our own server" quietly skip this.

## The transform log is itself sensitive

`slopify --log run.json` writes the **full original text plus every
intermediate transform state**, in plaintext, to disk. That's necessary for
exact-inverse `deslopify`, but it means a log file is functionally a second
copy of the user's text sitting on disk.

- `--log` must stay opt-in (it already is) — never write a log by default.
- Never auto-upload, sync, or attach log files to bug reports/telemetry.
- Don't commit sample log files to the repo; `.gitignore` excludes common
  log patterns, but double check before `git add` on anything you generate
  while testing.

## Input handling

- Don't `eval`/`exec`/`pickle.loads` any user-supplied content, ever.
- If a web frontend is added: enforce a request size limit (a large paste
  or upload is an easy DoS vector), validate any uploaded file's type
  before reading it, and never build file paths from user input without
  validation (path traversal).

## Reporting a vulnerability

Open an issue, or email hobson.james@gmail.com if it shouldn't be public
before a fix ships.

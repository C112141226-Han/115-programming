# AGENTS.md

## State
- 專案語言為 Python，以 conda 管理套件，環境名稱為 `iem_python`。
- Repo is newly initialized: only `.gitignore` (Python template) is committed. No source, README, manifest, or toolchain config exists yet.
- Do not assume a framework or test runner. Check what was added before running commands.

## 語言
- 所有的回應都使用繁體中文。

## Working agreements
- Prefer `read` / `edit` tools for file ops over `shell` equivalents; reserve `shell` for actual execution.
- Commands run on Windows via PowerShell. Quote paths with spaces.
- Verify every change by executing it when feasible; do not claim unverified behavior.
- Only create files that are necessary; prefer editing existing files.
- Keep this file updated as the stack lands: record exact setup, run, lint, typecheck, and test commands plus any required ordering.

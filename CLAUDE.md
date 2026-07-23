# Project Guide for AI Assistants

This document guides AI assistants on how to navigate and work with this project.

## Project Overview

**What this project does:** Read `README.rst` for project description and purpose.

**Project type:** Python package

## Domain Background

`chatbot_deeplink` collects the "deep link" URL schemes that various AI chatbot web apps/clients use to open a new conversation with a pre-filled prompt, and exposes each one as a Python function that does one-click percent-encoding for the caller.

- **Mechanism:** almost all of these are `https://<host>/...?q=<percent-encoded-utf8-prompt>` style URLs. The prompt is UTF-8 bytes, then percent-encoded (`%XX`) -- never Base64. Behavior differs per provider: some auto-submit the prompt as a sent message (e.g. ChatGPT `?q=`), some only pre-fill the input box and require the user to press Enter (e.g. Claude Web `/new?q=`), and native app/CLI schemes (e.g. `claude-cli://open?q=`) may impose a max query length and require user confirmation before submitting. None of this is an officially documented, versioned API -- treat every provider's mechanism as observed web behavior that can change without notice.
- **Design pattern:** each supported provider is modeled as a `dataclass` implementing a Command-pattern interface (build prompt -> encode -> produce URL), so adding a new provider means adding a new dataclass, not touching a central dispatch function.
- **Target providers** (best-effort, not all guaranteed to be supported): Claude, ChatGPT, Gemini, Grok, Doubao, DeepSeek, Zai, Kimi, MiniMax.
- **Reference docs:** `.claude/skills/pypi-chatbot_deeplink/ref/about.md` has the general deep link mechanism writeup; per-provider mechanism notes live in `ref/<provider>.md` -- only written once the mechanism has actually been confirmed, so an absent file means that provider's deep link behavior is not yet documented.

## Core Configuration Files

### Tool & Dependency Management
- `mise.toml` - Task runner and tool version management (Python 3.12, uv, claude)
- `pyproject.toml` - Python dependencies and package metadata
- `.venv/` - Virtual environment directory (created by uv)

Use `mise ls python --current` to see the exact Python version in use.

### CI/CD & Testing
- `.github/workflows/main.yml` - GitHub Actions CI workflow
- `codecov.yml` + `.coveragerc` - Code coverage reporting (codecov.io)
- `.readthedocs.yml` - Documentation hosting (readthedocs.org)

### Documentation
- `docs/source/` - Sphinx documentation source files
- `docs/source/conf.py` - Sphinx configuration

## Development Workflow

### Task Management
List all available tasks:
```bash
mise tasks ls
```

Run a specific task:
```bash
mise run ${task_name}
```

**Key tasks:**
- `inst` - Install all dependencies using uv (fast package manager)
- `cov` - Run unit tests with coverage report
- `build-doc` - Build Sphinx documentation

For complete task reference, run `mise run list-tasks` to generate `.claude/mise-tasks.md`.

### Testing Philosophy
This project uses **pytest** with a special pattern that allows running individual test files as standalone scripts.

**Example:** See `tests/test_api.py` - the `if __name__ == "__main__":` block demonstrates this pattern. It runs pytest as a subprocess with coverage tracking for the specific module, enabling quick isolated testing during development.

## Working with This Project

**Approach:**
1. Don't load entire files unnecessarily - read specific files only when needed
2. Use task commands (`mise run`) instead of direct tool invocation
3. Follow the testing pattern when creating new test files
4. Reference configuration files for specific settings rather than assuming defaults

**Tools in use:**
- **mise-en-place** - Development tool management
- **uv** - Fast Python package management
- **pytest** - Unit testing framework
- **sphinx** - Documentation generation

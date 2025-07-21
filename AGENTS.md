# ReasonBot Codex Agent Instructions

## Project Overview

ReasonBot is a Python-based AI bot that listens for @mentions on Twitter (X), analyzes the context and tone of the tweet it's tagged on, and replies with calm, strategic, cause-effect-based logic designed to dismantle bad faith arguments and misinformation.

This is **not** a spammy auto-reply bot. It is a summoned, logic-driven rhetorical assistant that aims to encourage high-fidelity thinking through powerful, controlled responses.

## Tech Stack

- Python 3.10+
- Tweepy (Twitter API wrapper)
- OpenAI or local LLMs for language analysis
- SQLite or Postgres for lightweight caching
- GitHub for version control
- Optional: Replit, Railway, or AWS for hosting

## File & Folder Structure

- `bot.py` — Core logic: monitors mentions, fetches tweets, posts replies
- `analyzer.py` — LLM prompt/response layer: sentiment detection, ideology tagging, etc.
- `replier.py` — Response builder: templates + logic for generating replies
- `utils.py` — Caching, rate-limiting, metadata tools
- `tests/` — All unit and integration tests
- `docs/` — Human-friendly documentation and explanations for vibe-coders (very important!)

## &#x20;Documentation & Comments

- All logic-heavy functions **must** include docstrings.
- Include **inline comments** wherever logic may be confusing or non-obvious.
- Provide **worked examples** and code explanations in the `/docs` folder to help developers (especially those who are not Python gods) understand what each part of the system is doing.

> This repo is being built by a very clever human, not a programming deity. Codex should **never assume expert-level knowledge** unless clearly stated. Comment generously. Document early. Empathize always.

## Development & Testing

- Dependencies:

  ```bash
  pip install -r requirements.txt
  ```

- Running tests:

  ```bash
  pytest tests/
  ```

- Formatting and linting:

  ```bash
  black .
  flake8 .
  ```

All PRs should pass tests, be flake8 and black compliant, and not break existing features.

## Behavior

- Bot responds **only** when @ReasonBot is explicitly mentioned.
- It pulls the tagged tweet and (optionally) a few of the original poster's recent tweets for context.
- Analyzes tone and patterns using LLMs or local sentiment logic.
- Chooses an appropriate response level (e.g. soft rebuttal, cause-effect loop, strategic scolding).
- Replies publicly and stores the interaction in a local cache to avoid duplicate replies.

## PR & Contribution Guidelines

All Pull Requests should:

- Be titled with a clear prefix: `[Feature]`, `[Fix]`, `[Refactor]`, `[Docs]`
- Include a short summary + what was tested and how
- Be well-documented in the code and `/docs/`
- Include new tests where applicable

## Future Modules (Roadmap)

- `scheduler.py` — optional cron/queue-based version for higher control
- `persona_switch.py` — lets user choose tone (ReasonBot vs Rhetoricus)
- `dashboard/` — visual logs of interactions, reply stats, etc.

---

> ReasonBot is more than a script. It's a rhetorical instrument. Codex is here to help keep its edge sharp and accessible to all who build with it.


# ReasonBot

**ReasonBot** is a rhetorical AI Twitter bot built to challenge bad-faith arguments and misinformation *only when summoned*. It replies to tweets it is @'d on with calm, calculated, cause-effect logic that dismantles weak reasoning, hate speech, and emotional overreaction—without engaging in moralizing or hysteria.

> "Real rebellion is strategy, not self-sabotage." – ReasonBot

---

## How It Works

1. **Listener** – Monitors for @mentions of `@ReasonBot`
2. **Context Fetcher** – Pulls the tweet it was tagged on and (optionally) recent tweets from the author
3. **Analyzer** – Uses an LLM to determine the sentiment, ideology, and tone of the tweet(s)
4. **Replier** – Generates a strategic response using templates, cause-effect loops, or tone disarmament
5. **Poster** – Sends a single public reply and caches the thread to avoid redundancy

---

## Why ReasonBot?

Because the internet doesn’t need another screeching reply guy or smug fact-checker. ReasonBot is:

- Tactical – Shows how the target undermines their own cause
- Psychologically aware – Disarms, reframes, and exposes contradictions
- Summoned only when tagged – You control where it speaks
- Clean & intentional – No spam. No noise. Just scalpel logic.

---

## Repo Structure

- `bot.py` – Listens for mentions and coordinates response pipeline
- `analyzer.py` – Handles LLM calls and context interpretation
- `replier.py` – Crafts replies based on logic trees and prompt templates
- `utils.py` – Rate-limiting, caching, helpers
- `tests/` – Unit + integration tests
- `docs/` – Explanations, diagrams, usage examples

---

## Local Setup

```bash
pip install -r requirements.txt
python bot.py
```

To run tests:

```bash
pytest tests/
```

Linting & formatting:

```bash
flake8 .
black .
```

---

## Example Usage

> User sees a tweet full of bigoted nonsense.
>
> Instead of doomscrolling or rage-replying...
>
> They tag `@ReasonBot`
>
> ReasonBot reads the tweet, crafts a tactically sound reply, and posts it.

Result? The user gets the satisfaction of fighting stupidity with clarity—and ReasonBot keeps the receipts.

---

## License

MIT. Use, remix, or fork it responsibly.

---

## Status

Actively being built by humans with strong coffee and stronger opinions. Want to help? Read `AGENTS.md` and dive in.

---

## Bonus Philosophy

ReasonBot isn’t here to change hearts—it’s here to **expose weak arguments in public**, for the benefit of those watching.

> "You’re not fighting the system. You’re feeding it. And they know it. Do you?"

Tag him in. Walk away smarter.


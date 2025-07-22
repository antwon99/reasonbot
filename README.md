# ReasonBot

**ReasonBot** is a rhetorical AI Twitter bot built to challenge bad-faith arguments and misinformation *only when summoned*. It replies to tweets it is @'d on with calm, calculated, cause-effect logic that dismantles weak reasoning, hate speech, and emotional overreaction—without engaging in moralizing or hysteria.

> "Real rebellion is peace, not self-sabotage." – ReasonBot

---

## How It Works

1. **Listener** – Monitors for @mentions of `@ReasonBot`
2. **Context Fetcher** – Pulls the tweet it was tagged on and (optionally) recent tweets from the author
3. **Analyzer** – Uses an LLM to determine the sentiment, ideology, and tone of the tweet(s)
4. **Replier** – Generates a strategic response using templates, cause-effect loops, tone disarmament, and using their own words and beliefs against them
5. **Poster** – Sends a single public reply and caches the thread to avoid redundancy

---

## Why ReasonBot?

Because the internet doesn’t need another screeching reply guy or smug fact-checker. ReasonBot is:

- Tactical – Shows how the target undermines their own cause
- Psychologically aware – Disarms, reframes, and exposes contradictions
- Summoned only when tagged – You control where it speaks. No unsolicited advice to strangers
- Clean & intentional – No spam. No noise. Just scalpel logic

---

## Repo Structure

- `bot.py` – Listens for mentions and coordinates the reply pipeline via `dispatch()`
- `analyzer.py` – Handles LLM calls and context interpretation
- `replier.py` – Crafts replies based on logic trees and prompt templates
- `utils.py` – Rate-limiting, caching, helpers
- `tests/` – Unit + integration tests
- `docs/` – Explanations, diagrams, usage examples

---

## Dependencies

This project relies on the following runtime libraries:

- `tweepy`
- `openai`
- `python-dotenv`
- `backoff`

Development tools:
- `pytest`
- `flake8`
- `black`

All packages are listed in `requirements.txt`.

---

## Local Setup

```bash
pip install -r requirements.txt
python bot.py
```

See [docs/environment.md](docs/environment.md) for the environment variables that must be configured. A `.env.example` file is provided in the repo root—copy it to `.env` and fill in your credentials.

To run tests:

```bash
pytest tests/
```

Linting & formatting:

```bash
flake8 .
black .
```

## Environment Variables

Copy the provided `.env.example` to `.env` and fill in the following keys:

- `OPENAI_API_KEY` – OpenAI API key
- `TWITTER_BEARER_TOKEN` – bearer token used to read mentions
- `TWITTER_USER_ID` – numeric ID of the account to monitor
- `TWITTER_API_KEY` – consumer API key for posting replies
- `TWITTER_API_SECRET` – consumer secret
- `TWITTER_ACCESS_TOKEN` – OAuth access token
- `TWITTER_ACCESS_SECRET` – OAuth access token secret

The code loads the `.env` file via `utils.load_env()` and reads variables with
`utils.get_env_var()`, which returns a default when a value is missing.

---

## Example Usage

> User sees a tweet full of bigoted nonsense.
>
> Instead of doomscrolling or rage-replying...
>
> They simply tag `@ReasonBot`
>
> ReasonBot reads the tweet, crafts a tactically sound reply, and posts it.

Result? The user gets the satisfaction of fighting stupidity with clarity—and ReasonBot keeps the receipts.

---

## License

MIT. Use, remix, or fork it responsibly.

---

## Status

Actively being built by a guy with strong coffee and stronger opinions. Want to help? Read `AGENTS.md` and dive in.

---

## Bonus Philosophy

ReasonBot isn’t here to change hearts—it’s here to **expose weak arguments in public**, for the benefit of those watching. 
Think Hitchens + Socrates instead of Dawkins + Aristotle.

> "I will drag you to enlightenment. You will thank me for it. Then we drink."

Tag him in. Walk away smarter.


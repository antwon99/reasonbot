# Environment Variables

ReasonBot requires several API credentials to communicate with Twitter and OpenAI. These are typically set via a `.env` file in the project root.

## Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Fill in each of the following keys with your own values.

## Required Keys

- **`OPENAI_API_KEY`** – API key used to access OpenAI and generate replies.
- **`TWITTER_BEARER_TOKEN`** – bearer token for reading mentions of your account.
- **`TWITTER_USER_ID`** – numeric user ID for the account that ReasonBot monitors.
- **`TWITTER_API_KEY`** – Twitter consumer key used when posting replies.
- **`TWITTER_API_SECRET`** – consumer secret paired with the API key.
- **`TWITTER_ACCESS_TOKEN`** – OAuth access token for publishing tweets.
- **`TWITTER_ACCESS_SECRET`** – OAuth access token secret.

Keep this `.env` file out of version control and store your keys securely.

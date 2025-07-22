# Dispatch Flow

`dispatch()` in `bot.py` ties together the modules that analyze mentions and generate replies.

1. **check_mentions()** – grabs the latest tagged tweets.
2. **analyze_context()** – classifies tone, ideology, etc.
3. **generate_reply()** – crafts a short cause-effect based response.
4. **create_tweet()** – posts the reply in the thread.

A small file (`processed_ids.txt`) tracks which tweets have been handled so the bot doesn't respond more than once.

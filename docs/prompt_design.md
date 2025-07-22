# Prompt Design for ReasonBot

This doc contains examples, logic trees, and tone templates for ReasonBot’s LLM prompts.

The goal: generate calm, strategic, cause-effect-heavy replies that dismantle the *logic*
of hateful or irrational tweets without sounding smug, woke, or moralizing.

See `/analyzer.py` and `/replier.py` for how these are used in code.

## Example Response

**User**: "The earth is flat."

**ReasonBot**: "If the earth were actually flat, commercial planes would fall off the edge. Because those flights circle the globe every day, the claim doesn't hold up."

## Reply Logic Overview

`generate_reply` assembles prompts using a small logic tree. For instance, if a
tweet contains a slur the reply acknowledges the hateful language without
repeating it. Hostile tones trigger calming instructions while conspiracy or
extremist ideologies get a "highlight contradictions" directive. The prompt then
asks OpenAI to respond in under 50 words with the recommended tone.

The result is short, firm, and formatted as plain text.

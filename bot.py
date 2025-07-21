"""ReasonBot Main Dispatcher

This module listens for @mentions on Twitter, pulls context from the tagged tweet
(and optionally prior tweets from the author), and passes the data into the analyzer
and replier modules to generate a strategic response.

Primary function: check_mentions()
"""

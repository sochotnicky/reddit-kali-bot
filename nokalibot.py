#!/usr/bin/env python3
import os
import logging
import re

import praw

REPLY_TEMPLATE = """You seem to have posted a question involving Kali Linux.

Note that Kali Linux development team itself [recommends
against](https://www.kali.org/docs/introduction/should-i-use-kali-linux/) using Kali Linux for those
new to Linux or even as a general-purpose desktop operating system for
experienced users.

People might still want to help you solve your problem, but you are more likely to learn things if
you start with a different distribution. There is a whole subreddit dedicated to finding a
good distribution for you: r/FindMeADistro

Note: If I misunderstood, it's because I am a [stupid bot](https://github.com/sochotnicky/reddit-kali-bot). Apologies
"""

KALI_RE = re.compile(r".*\bkali\b.*")


def main():
    reddit = praw.Reddit(
        user_agent="NoKaliBot 0.1 (by u/podtatranec)",
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        refresh_token=os.environ["CLIENT_REFRESH_TOKEN"],
        username="NoKaliBot"
    )
    reddit.validate_on_submit = True

    subreddit = reddit.subreddit(os.environ["SUBREDDIT"])
    for submission in subreddit.stream.submissions():
        process_submission(submission)


def process_submission(submission):
    text = submission.selftext.lower()
    title = submission.title.lower()
    logging.debug("Processing %s - %s", title, submission.permalink)
    if not (KALI_RE.match(text, re.IGNORECASE) or KALI_RE.match(title, re.IGNORECASE)):
        logging.debug("No kali in text. NOOP")
        return

    if submission.num_comments != 0:
        logging.debug(f"Submission {submission.permalink} has a comment already - skipping")
        return

    logging.info(f"Replying to: {submission.title} - {submission.permalink}")
    submission.reply(REPLY_TEMPLATE)


if __name__ == "__main__":
    log = logging.basicConfig(level=logging.DEBUG)
    for logger_name in ("praw", "prawcore", "urllib3.connectionpool"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)
        logger.addHandler(log)

    main()

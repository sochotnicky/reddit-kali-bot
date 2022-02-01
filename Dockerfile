FROM python

RUN pip install --no-cache-dir praw

COPY nokalibot.py /

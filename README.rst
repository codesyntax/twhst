Introduction
============

twhst provides an easy way to store tweet from Twitter using it's search api (URL). In order to store
tweets, they must have and hashtag, and complain with a ruleset defined for the type of this hashtag.

It also builds a dictionary with the stored statuses. Every hash type has its own dictionary build
rules.

Available rulesets
------------------
- include_all : allways return True
- url: True if status has an url
- no_url: not(url)
- rt: True id status is a retweet
- no_rt: not(rt)
- picture: True if status has an picture
- no_picture: not(picture)
- mentiton: True if someone is mentioned in the status
- no_mention: not(mention)
- definition: True if colon is find in the status
- brackets: True if there are 2 brackets in status
- starts_with_hash: True if status starts with #

Instalation
-----------

pip install twhst

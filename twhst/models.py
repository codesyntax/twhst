import re
import json
from photologue.models import Photo

from django.db import models

from twhst.rules import include_all, definition, no_rt, no_url, picture, no_mention


HASHTAG_TYPE_CHOICES = ((0,'All'),
                        (1,'Dictionary'),
                        (2,'Sentence'),
                        (3,'Picture'))

RULESET_DICT = {0: [include_all],
                1: [definition, no_rt, no_url, no_mention],
                2: [no_rt, no_url, no_mention],
                3: [picture, no_mention]}


class Hashtag(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    description = models.TextField()
    photo = models.ForeignKey(Photo, blank=True, null=True)
    hash_type = models.IntegerField(choices=HASHTAG_TYPE_CHOICES)
    active = models.BooleanField(default=True)
    
    def create_status_from_result(self, result):
        status = Status(hashtag=self)
        for i in result.__dict__.keys():
            if i == 'entities':
                status.entities = json.dumps(getattr(result, i))
                continue
            if hasattr(status, i):
                setattr(status, i, getattr(result, i))
        for i in result.user.__dict__.keys():
            if hasattr(status, u'user_' + i):
                setattr(status, u'user_' + i, getattr(result.user, i))        
        status.twitter_id = result.id
        status.user_id = result.user.id
        status.user_created_at = result.user.created_at
        status.save()
        
    def parse(self, result):
        for rule in RULESET_DICT.get(self.hash_type):
            if not(rule(result)):
                return None
        self.create_status_from_result(result)

    def get_last_statuses(self):
        return self.status_set.all()
    
    def __unicode__(self):
        return self.name
    
class Status(models.Model):
    twitter_id = models.BigIntegerField(unique=True, db_index=True, primary_key=True)
    created_at = models.DateTimeField(db_index=True)
    entities = models.TextField(null=True,blank=True)    
    favorited = models.BooleanField(default=False)
    geo = models.CharField(max_length=160,null=True,blank=True)
    in_reply_to_screen_name = models.CharField(max_length=150,null=True,blank=True)
    in_reply_to_status_id = models.BigIntegerField(null=True,blank=True)
    in_reply_to_user_id = models.BigIntegerField(null=True,blank=True)

    retweet_count = models.CharField(max_length=5,default='0')
    retweeted = models.BooleanField(default=False)
    retweeted_status_id = models.BigIntegerField(null=True,blank=True)
    retweeted_status_created_at = models.DateTimeField(null=True,blank=True)    
    retweeted_status_entities = models.TextField(null=True,blank=True)
    retweeted_status_user_id = models.BigIntegerField(null=True,blank=True)
    retweeted_status_screen_name = models.CharField(max_length=150,null=True,blank=True)
    retweeted_status_user_created_at = models.DateTimeField(null=True,blank=True)
    retweeted_status_user_name = models.CharField(max_length=150,null=True,blank=True)
    retweeted_status_user_profile_image_url = models.CharField(max_length=255,null=True,blank=True)
    retweeted_status_text = models.CharField(max_length=255,null=True,blank=True)

    source = models.CharField(max_length=200,null=True,blank=True)    
    text = models.CharField(max_length=255)
    truncated = models.BooleanField(default=False)

    user_id = models.BigIntegerField(db_index=True)
    user_screen_name = models.CharField(max_length=150)
    user_created_at = models.DateTimeField()
    user_name = models.CharField(max_length=150,null=True,blank=True)
    user_profile_image_url = models.CharField(max_length=255,null=True,blank=True)
    user_description = models.TextField(null=True,blank=True)
    user_favourites_count = models.IntegerField(default=0)
    user_followers_count = models.IntegerField(default=0)  
    user_friends_count = models.IntegerField(default=0)
    user_statuses_count = models.IntegerField(default=0)
    user_listed_count = models.IntegerField(default=0)
    user_url = models.CharField(max_length=255,null=True,blank=True)

    hashtag = models.ForeignKey(Hashtag)

    def show_status(self):
        return re.sub(r'#' + self.hashtag.name, '', self.text,  flags=re.IGNORECASE)

    def _format_media_entity(self, data):
        """
        https://dev.twitter.com/docs/tweet-entities
        """
        to_return = []
        template = u'<a href="%(url)s">%(display_url)s</a>'
        img_template = u'<img src="%(url)s" />'
        for url in data:
            if 'display_url' not in url.keys():
                url['display_url'] = url['url']
            if url.get('type') == u'photo':
                to_return.append([url['indices'][0],url['indices'][1], img_template % {'url': url.get('media_url')}])
            else:
                to_return.append([url['indices'][0],url['indices'][1], template % url])
        return to_return

    def _format_urls_entity(self, data):
        to_return = []
        template = u'<a href="%(url)s">%(display_url)s</a>'
        for url in data:
            if 'display_url' not in url.keys():
                url['display_url'] = url['url']
            to_return.append([url['indices'][0],url['indices'][1], template % url])
        return to_return

    def _format_user_mentions_entity(self, data):
        to_return = []
        template = u'<a href="http://twitter.com/%(screen_name)s">@%(screen_name)s</a>'
        for user in data:
            to_return.append([user['indices'][0], user['indices'][1], template % user])
        return to_return
    
    def _format_hashtags_entity(self, data):
        to_return = []
        template = u'<a href="http://twitter.com/search?q=%%23%(text)s">#%(text)s</a>'
        for hash in data:
            to_return.append([hash['indices'][0],hash['indices'][1], template % hash])
        return to_return
    
    def renderStatus(self):
        """render status as defined by twitter guidelines"""
        html = self.text
        data = self.entities
        entities = []
        for k,v in json.loads(data).items():
            if k == 'media':
                entities += self._format_media_entity(v)
            elif k == 'urls':
                entities += self._format_urls_entity(v)
            elif k == 'user_mentions':
                entities += self._format_user_mentions_entity(v)
            elif k == 'hashtags':
                entities += self._format_hashtags_entity(v)
        from operator import itemgetter
        sorted_entities = sorted(entities, key=itemgetter(0))
        sorted_entities.reverse()
        for entity in sorted_entities:
            html = html[:entity[0]]+entity[2]+html[entity[1]:]
        return html

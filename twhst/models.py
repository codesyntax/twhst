from photologue.models import Photo

from django.db import models

from twhst.rules import include_all, definition, no_rt, no_url, picture


HASHTAG_TYPE_CHOICES = ((0,'All'),
                        (1,'Dictionary'),
                        (2,'Sentence'),
                        (3,'Picture'))

RULESET_DICT = {0: [include_all],
                1: [definition, no_rt, no_url],
                2: [include_all],
                3: [picture]}

class Hashtag(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    description = models.TextField()
    photo = models.ForeignKey(Photo, blank=True, null=True)
    hash_type = models.IntegerField(choices=HASHTAG_TYPE_CHOICES)
    active = models.BooleanField(default=True)
    
    def create_status_from_result(self, result):
        status = Status(hashtag=self)
        for i in result.__dict__.keys():
            if hasattr(status, i):
                setattr(status, i, getattr(result, i))
        for i in result.user.__dict__.keys():
            if hasattr(status, i):
                setattr(status, i, getattr(result.user, i))
        status.twitter_id = result.id
        status.user_id = result.user.id
        status.user_created_at = result.user.created_at
        status.save()
        
    def parse(self, result):
        for rule in RULESET_DICT.get(self.hash_type):
            if not(rule(result)):
                return None
        self.create_status_from_result(result)

            
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
    screen_name = models.CharField(max_length=150)
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

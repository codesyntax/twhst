from django.core.management.base import NoArgsCommand
from twhst.utils import get_tweepy_api
from twhst.models import Hashtag, Status

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        api = get_tweepy_api()
        for hashtag in Hashtag.objects.filter(active=True):
            last_id = Status.objects.filter(hashtag=hashtag)
            name = '#' + hashtag.name
            if last_id.exists():
                last_id = last_id[0]
                print 'LAST ID: ' + str(last_id.twitter_id)
                result = api.search(q=name, since_id=last_id.twitter_id, count=100)
            else:
                result = api.search(q=name,count=100)
            for r in result:
                hashtag.parse(r)

                

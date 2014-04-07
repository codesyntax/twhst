from django.contrib import admin

from twhst.models import Hashtag

class HashtagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
# Register your models here.
admin.site.register(Hashtag, HashtagAdmin)

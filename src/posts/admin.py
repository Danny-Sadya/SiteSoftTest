from django.contrib import admin

from .models import *


admin.site.register(PostModel)
# admin.site.register(PostTagModel)
admin.site.register(PostToScrapeModel)

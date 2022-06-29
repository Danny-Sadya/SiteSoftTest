from django.contrib import admin

from .models import *


# admin.site.register(PostModel)
@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    readonly_fields = ('scraped_date',)


# admin.site.register(PostTagModel)

admin.site.register(PostToScrapeModel)

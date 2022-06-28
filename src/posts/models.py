from django.db import models


class PostModel(models.Model):
    """Модель данных из поста на Хабре"""

    header = models.CharField(max_length=1024, null=True, blank=True)
    author_name = models.CharField(max_length=1024, null=True, blank=True)
    author_url = models.CharField(max_length=1024, null=True, blank=True)
    post_url = models.CharField(max_length=1024, null=True, blank=True, unique=True)
    publication_date = models.DateTimeField(null=True, blank=True)
    scraped_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=2048, null=True, blank=True)

    def __str__(self):
        return self.header

#
# class PostTagModel(models.Model):
#     """Модель тэгов из поста на Хабре"""
#
#     tag = models.CharField(max_length=1024, null=True, blank=True)
#
#     def __str__(self):
#         return self.tag
#

class PostToScrapeModel(models.Model):
    """Модель постов которые нужно отскрейпить на Хабре"""

    post_url = models.CharField(max_length=1024, null=True, blank=True)
    scraped = models.BooleanField(default=False)

    def __str__(self):
        return self.post_url
from celery import shared_task
from config.celery import app
from .models import PostModel, PostToScrapeModel
from .services.habr_scraper import HabrScraper


@shared_task()
def scrape_main_page():
    """Таск, который запускает скрейпер и сохраняет данные в бд"""
    habr_scraper = HabrScraper()
    posts_data = habr_scraper.run_base_scraper()
    for post_data in posts_data:
        same_post = PostModel.objects.filter(post_url=post_data['post_url'])
        if not same_post:
            post_model = PostModel.objects.create(
                header=post_data['header'],
                author_name=post_data['author_name'],
                author_url=post_data['author_url'],
                post_url=post_data['post_url'],
                publication_date=post_data['publication_date'],
                tags=post_data['tags']
            )
            post_model.save()


@shared_task()
def scrape_specific_posts():
    """Таск, который скрейпит посты из отдельной таблицы"""
    objects = PostToScrapeModel.objects.filter(scraped=False)
    url_list = []
    for obj in objects:
        url_list.append(obj.post_url)
    habr_scraper = HabrScraper()
    posts_data = habr_scraper.run_specific_posts_scraper(url_list)
    for post_data in posts_data:
        same_post = PostModel.objects.filter(post_url=post_data['post_url'])
        if not same_post:
            post_model = PostModel.objects.create(
                header=post_data['header'],
                author_name=post_data['author_name'],
                author_url=post_data['author_url'],
                post_url=post_data['post_url'],
                publication_date=post_data['publication_date'],
                tags=post_data['tags']
            )
            post_model.save()

    for obj in objects:
        obj.scraped = True
        obj.save()

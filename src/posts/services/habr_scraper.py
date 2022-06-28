import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

import platform


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class HabrScraper:
    """Скрейпер Хабра"""
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }

        self.final_data = []

    def run_base_scraper(self):
        """Запуск скрейпера, который скрейпит все посты с главной страницы Хабра"""
        asyncio.run(self.scrape_main_page())
        return self.final_data

    def run_specific_posts_scraper(self, url_list):
        asyncio.run(self.scrape_specific_posts(url_list))
        return self.final_data

    async def scrape_specific_posts(self, url_list):
        async with aiohttp.ClientSession() as self.session:
            tasks = []
            for url in url_list:
                task = asyncio.create_task(self.scrape_post(url))
                tasks.append(task)

            await asyncio.gather(*tasks)


    async def scrape_main_page(self):
        async with aiohttp.ClientSession() as self.session:
            response = await self.session.get(url='https://habr.com/ru/all/', headers=self.headers)
            soup = BeautifulSoup(await response.text(), 'lxml')
            post_list = soup.find_all('a', class_='tm-article-snippet__title-link')
            tasks = []
            for post in post_list:
                url = 'https://habr.com' + post.get('href')
                task = asyncio.create_task(self.scrape_post(url))
                tasks.append(task)

            await asyncio.gather(*tasks)

    async def scrape_post(self, post_url):
        try:
            async with self.session.get(url=post_url, headers=self.headers) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')

            try:
                author_name = soup.find('span', class_='tm-user-card__name tm-user-card__name tm-user-card__name_variant-article').text
            except AttributeError:
                author_name = soup.find('a', class_='tm-user-info__username').text.strip()

            header = soup.find('h1', class_='tm-article-snippet__title tm-article-snippet__title_h1').text
            publication_date = datetime.strptime(soup.find('span', class_='tm-article-snippet__datetime-published').find('time').get('datetime'),
                                     "%Y-%m-%dT%H:%M:%S.%fZ")
            author_url = 'https://habr.com/ru/users/' + soup.find('span', class_='tm-user-info__user').text.strip()

            post_tags = ''
            for tag in soup.find_all('span', class_='tm-article-snippet__hubs-item'):
                post_tags += tag.text + '; '

            data = {
                'header': header,
                'tags': post_tags,
                'author_name': author_name,
                'author_url': author_url,
                'publication_date': publication_date,
                'post_url': post_url
            }
            print(data)
            self.final_data.append(data)
        except AttributeError:
            print(f'Cannot find smth at url: {post_url} ')


if __name__ == '__main__':
    scraper = HabrScraper()
    scraper.run_specific_posts_scraper(['https://habr.com/ru/company/getmatch/blog/673794/',
                                        'https://habr.com/ru/company/domclick/blog/673648/'])

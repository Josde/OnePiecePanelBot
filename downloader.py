import traceback

from bs4 import BeautifulSoup
from aiohttp import ClientSession
import asyncio
import aiohttp
import threading
from pathlib import Path
import requests
from time import sleep
import subprocess
import concurrent.futures
BASE_PATH = 'https://onepiecechapters.com'
RESOURCE_PATH = Path.cwd().joinpath("res")
MAX_THREADS = 32
semaphore = threading.BoundedSemaphore(MAX_THREADS)
async def async_parsing():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Accept-Encoding': 'GZIP'}
    timeout = aiohttp.ClientTimeout(total=10)
    link_list = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
    sourceList = requests.get('https://onepiecechapters.com/mangas/5/one-piece').text
    try:
        soup = BeautifulSoup(sourceList, 'html.parser')
        for link in soup.find_all('a', class_='block border border-border bg-card mb-3 p-3 rounded'):
            link_list.append(BASE_PATH + link.get('href'))
        for link in link_list:
            print('Parsing ' + link)
            chapter_number = link.split('-')[-1]
            if int(chapter_number) < 3:
                try:
                    print('{0} threads active.'.format(semaphore._value))
                    downloadChapter(link, chapter_number)
                    #executor.submit(downloadChapter, link, chapter_number)
                    print('Launched thread {0} for chapter {1}'.format(semaphore._value, str(chapter_number)))

                except Exception:
                    traceback.print_exc()
    except Exception:
        traceback.print_exc()
    finally:
        executor.shutdown()

def downloadChapter(link, chapter_number):
    semaphore.acquire(blocking=True)
    chapter_dir = RESOURCE_PATH.joinpath(chapter_number)
    if not chapter_dir.is_dir():
        chapter_dir.mkdir()
    sourceChapter = requests.get(link).text
    index = 1
    soup = BeautifulSoup(sourceChapter, 'html.parser')
    picture_div = soup.find('div', class_='flex flex-col items-center justify-center')
    for picture in picture_div.findAll('picture'):
        file_name = str(index) + '.png'
        file_path = chapter_dir / file_name
        image = picture.find('img')
        print('Downloading chapter {0} page {1}'.format(chapter_number, index))
        index += 1
        image_bin = requests.get(image.get('src')).content
        with file_path.open('wb') as f:
            f.write(image_bin)
    semaphore.release()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_parsing())
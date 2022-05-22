import os
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
import argparse
BASE_PATH = 'https://onepiecechapters.com'
RESOURCE_PATH = Path(os.path.dirname(__file__)).joinpath("res")
MAX_THREADS = 8 #default if not specified
MIN_CHAPTER = 1
MAX_CHAPTER = 10000 #just in case we dont get any arguments passed, this doesnt matter because chapter numbers dont go this high
semaphore = None
async def async_parsing(fromChapter, toChapter, threads, redl):
    link_list = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=threads)
    sourceList = requests.get('https://onepiecechapters.com/mangas/5/one-piece').text
    try:
        soup = BeautifulSoup(sourceList, 'html.parser')
        for link in soup.find_all('a', class_='block border border-border bg-card mb-3 p-3 rounded'):
            link_list.append(BASE_PATH + link.get('href'))
        for link in link_list:
            print('Parsing ' + link)
            chapter_number = link.split('-')[-1]
            if int(chapter_number) >= fromChapter and int(chapter_number) <= toChapter:
                try:
                    print('{0} threads active.'.format(semaphore._value))
                    downloadChapter(link, chapter_number, redl)
                    executor.submit(downloadChapter, link, chapter_number)
                    print('Launched thread {0} for chapter {1}'.format(int(semaphore._value), str(chapter_number)))

                except Exception:
                    traceback.print_exc()
    except Exception:
        traceback.print_exc()
    finally:
        executor.shutdown()

def downloadChapter(link, chapter_number, redownload):
    semaphore.acquire(blocking=True)
    chapter_dir = RESOURCE_PATH.joinpath(chapter_number)
    if chapter_dir.is_dir() and not redownload:
        semaphore.release()
        print('Chapter {0} was already downloaded, ignoring'.format(chapter_number))
        return # do not download already downloadad chapters
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
    parser = argparse.ArgumentParser(description='Downloads all one piece chapter, or chapters in the range specified by min and max parameters')
    parser.add_argument('-min', type=int, help='The earlist chapter from which you want to start downloading (default: 1)',
                        default=MIN_CHAPTER,
                        required=False)
    parser.add_argument('-max', type=int,
                        help='The latest chapter which you want to download (default: 10000)',
                        default=MAX_CHAPTER,
                        required=False)
    parser.add_argument('-redl', type=bool,
                        help='Should chapters which are already downloaded be redownloaded? (default: False)',
                        default=False,
                        required=False)
    parser.add_argument('-threads', type=int,
                        help='Number of threads to use for downloading (default: 8)',
                        default=MAX_THREADS,
                        required=False)
    args = parser.parse_args()
    if not RESOURCE_PATH.is_dir():
        RESOURCE_PATH.mkdir()
    semaphore = threading.BoundedSemaphore(args.threads)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_parsing(args.min, args.max, args.threads, args.redl))
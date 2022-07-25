import os
import logging
import tweepy
from dotenv import load_dotenv
from pathlib import Path
import random
load_dotenv()
logging.basicConfig(filename='tweet.log', format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
RESOURCE_PATH = Path(os.path.dirname(__file__)).joinpath("res")
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuth1UserHandler(
    api_key, api_secret,
    access_token, access_token_secret
)

api = tweepy.API(auth, retry_count=5)

arc_start= {
    1: 'Romance Dawn',
    8: 'Orange Town',
    22: 'Syrup Village',
    42: 'Baratie',
    69: 'Arlong Park',
    96: 'Loguetown',
    101: 'Reverse Mountain',
    106: 'Whisky Peak',
    115: 'Little Garden',
    130: 'Drum Island',
    155: 'Arabasta',
    218: 'Jaya',
    237: 'Skypiea',
    303: 'Long Ring Long Land',
    322: 'Water 7',
    375: 'Enies Lobby',
    431: 'Post Ennies Lobby',
    442: 'Thriller Bark',
    490: 'Sabaody Archipelago',
    514: 'Amazon Lily',
    525: 'Impel Down',
    550: 'Marineford',
    581: 'Post-War',
    598: 'Return to Sabaody',
    603: 'Fish-Man Island',
    654: 'Punk Hazard',
    700: 'Dressrosa',
    802: 'Zou',
    825: 'Whole Cake Island',
    903: 'Levely',
    909: 'Wano Country',
}

def get_next_page(chapter_number, page_number):
    image_path = page_to_file(chapter_number, page_number + 1)
    if image_path.exists():
        return chapter_number, page_number + 1, image_path
    image_path = page_to_file(chapter_number + 1, 1)
    if (image_path.exists()):
        return chapter_number + 1, 1, image_path
    else: # We got to the last page!
        return None, None, None
    
def page_to_file(chapter_number, page_number):
    chapter_dir = RESOURCE_PATH / str(chapter_number)
    image_path = chapter_dir / (str(page_number) + ".png")
    return image_path

def write_page(chapter_number, page_number):
    with open('current_page', 'w+') as f:
        f.write('{0} {1}'.format(chapter_number, page_number))
        
def get_current_page():
    with open('current_page', 'r') as f:
        content = f.readline()
        chapter_number, page_number = content.split(" ")
        return int(chapter_number), int(page_number)
    
def tweet():
    # Use system random to prevent tweeting the same image if the tweet goes up at the same time.
    # If HW random is not available, delete the SystemRandom() part.
    chapter_number, page_number = get_current_page()    
    chapter_number, page_number, page_path = get_next_page(chapter_number, page_number)
    if (page_path is not None and page_path.exists() and page_path.is_file()):
        is_bigger_than_last = True
        for key in arc_start.keys():
            if int(chapter_number) >= key:
                last_key = key
                is_bigger_than_last = True
            elif int(chapter_number) < key and is_bigger_than_last:
                arc = arc_start[last_key]
                break
            else:
                arc = arc_start[list(arc_start.keys())[-1]]

        tweet_string = 'Chapter {0}: Page {1} ({2})'.format(chapter_number, page_number, arc)
        try:
            image = api.media_upload(filename=page_path)
            api.update_status(status=tweet_string, media_ids=[image.media_id_string])
            write_page(chapter_number, page_number)
        except Exception as e:
            logging.error('Exception when uploading tweet: {0}'.format(type(e).__name__))
    else:
        logging.error('File path {0} not found while searching for C{1}-P{2}'.format(page_path, chapter_number, page_number))

    

if __name__ == '__main__':
    tweet()
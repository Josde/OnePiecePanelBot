import os

import tweepy
from dotenv import load_dotenv
from pathlib import Path
import random
load_dotenv()

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

def tweet():
    chapter = random.choice(os.listdir(RESOURCE_PATH))
    chapter_dir = RESOURCE_PATH / chapter
    page = random.choice(os.listdir(chapter_dir))
    page_file = chapter_dir.joinpath(page)

    #get arc
    is_bigger_than_last = True
    for key in arc_start.keys():
        if int(chapter) >= key:
            last_key = key
            is_bigger_than_last = True
        elif int(chapter) < key and is_bigger_than_last:
            arc = arc_start[last_key]
            break
        else:
            arc = arc_start[list(arc_start.keys())[-1]]

    tweet_string = 'Chapter {0}: Page {1} ({2})'.format(chapter, page[:-4], arc)
    image = api.media_upload(filename=page_file)
    api.update_status(status=tweet_string, media_ids=[image.media_id_string])


if __name__ == '__main__':
    tweet()
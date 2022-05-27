# OPPanelBot
## Installation
- Clone this repository  
- Run ``python -m pip install -r requirements.txt``
- Run ``python downloader.py``
- Optionally, configure the following options:
  - \-min: Earliest chapter to download
  - \-max: Latest chapter to download
  - \-redl: Redownload a chapter, even if it has been downloaded before
  - \-threads: The number of threads to use for concurrent downloading
- After downloads have been done, optionally clean up SBS and TCBScans images
- If you have cleaned up these images, run ``python renamer.py`` to fix up page numbers
- Set up Three-Legged OAuth in your Twitter account
- Create a .env file in the project root and config the following variables:
  - API_KEY
  - API_KEY_SECRET
  - ACCESS_TOKEN
  - ACCESS_TOKEN_SECRET
- Set up a cron job to tweet out random panels at whichever pace you want!
- Set up a cron job to periodically download new chapters! **DO NOT USE \-redl** on this job, to prevent excessive load on TCBScans' servers

## Troubleshooting

- If your computer doesn't have hardware random, check out tweet.py's comments.

## Sample

Currently running at https://twitter.com/OPPages!

## Known bugs

- Chapters with a v2, or v3 release will be downloaded in the wrong folder.
  - For the time being, this only happens with chapter 1027, which will be downloaded into chapter 2.

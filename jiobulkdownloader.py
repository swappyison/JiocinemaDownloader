import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import jwt  # Import the jwt module
import yt_dlp  # Import yt-dlp for downloading videos

def replace_invalid_chars(title: str) -> str:
    invalid_chars = {'<': '\u02c2', '>': '\u02c3', ':': '\u02d0', '"': '\u02ba', '/': '\u2044',
                     '\\': '\u29f9', '|': '\u01c0', '?': '\u0294', '*': '\u2217'}

    return ''.join(invalid_chars.get(c, c) for c in title)

with open('access_token.txt', 'r') as file:
    access_token = file.read().strip()  # Read and remove any leading/trailing whitespace
print('\n')

# Read episode URLs from the text file
with open('episode_urls.txt', 'r') as file:
    urls = file.read().splitlines()

m3u8DL_RE = 'N_m3u8DL-RE'

decoded = jwt.decode(access_token, options={"verify_signature": False})

deviceId = decoded['data']['deviceId']
uniqueid = decoded['data']['userId']
appName = decoded['data']['appName']

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers2 = {
    'authority': 'apis-jiovoot.voot.com',
    'accept': 'application/json, text/plain, */*',
    'accesstoken': access_token,
    'appname': appName,
    'content-type': 'application/json',
    'deviceid': deviceId,
    'origin': 'https://www.jiocinema.com',
    'referer': 'https://www.jiocinema.com/',
    'uniqueid': uniqueid,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'versioncode': '560',
    'x-platform': 'androidweb',
    'x-platform-token': 'web',
}

json_data2 = {
    '4k': False,
    'ageGroup': '18+',
    'appVersion': '3.4.0',
    'bitrateProfile': 'xhdpi',
    'capability': {
        'drmCapability': {
            'aesSupport': 'yes',
            'fairPlayDrmSupport': 'yes',
            'playreadyDrmSupport': 'none',
            'widevineDRMSupport': 'yes',
        },
        'frameRateCapability': [
            {
                'frameRateSupport': '30fps',
                'videoQuality': '1440p',
            },
        ],
    },
    'continueWatchingRequired': True,
    'dolby': False,
    'downloadRequest': False,
    'hevc': False,
    'kidsSafe': False,
    'manufacturer': 'Windows',
    'model': 'Windows',
    'multiAudioRequired': True,
    'osVersion': '10',
    'parentalPinValid': True,
}

# Create a yt-dlp instance
ydl_opts = {}

# Iterate through the list of URLs
for link in urls:
    link_id = re.findall(r'.*/(.*)', link)[0].strip()

    try:
        # Send a POST request to get playback information
        response2 = requests.post(f'https://apis-jiovoot.voot.com/playbackjv/v4/{link_id}', headers=headers2,
                                  json=json_data2, verify=False).json()

        contentType = response2['data']['contentType']

        if contentType == 'MOVIE':
            movie_name = response2['data']['name']
            title = f'{movie_name}'

        elif contentType == 'EPISODE':
            showName = response2['data']['show']['name']
            season_num = int(response2['data']['episode']['season'])
            episode_num = int(response2['data']['episode']['episodeNo'])
            episode_title = response2['data']['fullTitle']

            title = f'{showName} - S{season_num:02d}E{episode_num:02d} - {episode_title}'

        else:
            movie_name = response2['data']['name']
            title = f'{movie_name}'

        title = replace_invalid_chars(title)
        print(f'\n{title}\n')

        mpd = response2['data']['playbackUrls'][0]['url']

        print(f'MPD URL: {mpd}\n')

        # Download the video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([mpd])

    except Exception as e:
        print(f"An error occurred: {str(e)}")

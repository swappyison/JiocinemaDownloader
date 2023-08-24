from pathlib import Path
import subprocess
import jwt
import re

access_token = input('access_token:')

print('\ntest link: https://www.jiocinema.com/movies/sergeant-bhojpuri/3767689\ntest link: https://www.jiocinema.com/tv-shows/kaalkoot/1/janam-din/3788001\n')

link = input('link: ')
link_id = re.findall(r'.*/(.*)', link)[0].strip()

m3u8DL_RE = 'N_m3u8DL-RE'

def replace_invalid_chars(title: str) -> str:
    invalid_chars = {'<': '\u02c2', '>': '\u02c3',
    ':': '\u02d0', '"': '\u02ba', '/': '\u2044',
    '\\': '\u29f9', '|': '\u01c0', '?': '\u0294',
    '*': '\u2217'}
    
    return ''.join(invalid_chars.get(c, c) for c in title)

decoded = jwt.decode(access_token, options={"verify_signature": False})
#print(f'\n{decoded}\n')

deviceId = decoded['data']['deviceId']
uniqueid = decoded['data']['userId']
appName = decoded['data']['appName']

######

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
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

response2 = requests.post('https://apis-jiovoot.voot.com/playbackjv/v4/'+link_id+'', headers=headers2, json=json_data2, verify=False).json()

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

lic_url = response2['data']['playbackUrls'][0]['licenseurl']

try:
    import requests
    
    headers03 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    
    response03 = requests.get(mpd, headers=headers03, verify=False).text
    
    pssh = re.findall(r'<cenc:pssh>(.{20,170})</cenc:pssh>', response03)[0].strip()
    print(f'{pssh}\n')

    import base64, requests, sys, xmltodict, json
    from pywidevine.L3.cdm import cdm, deviceconfig
    from base64 import b64encode
    from pywidevine.L3.getPSSH import get_pssh
    from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt
    import time
    import re  
    
    headers = {
        'authority': 'prod.media.jio.com',
        'accesstoken': access_token,
        'appname': appName,
        'content-type': 'application/octet-stream',
        'deviceid': deviceId,
        'devicetype': 'Web',
        'isdownload': 'false',
        'origin': 'https://www.jiocinema.com',
        'os': 'android',
        'referer': 'https://www.jiocinema.com/',
        'uniqueid': uniqueid,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'versioncode': '570',
        'x-feature-code': 'ytvjywxwkn',
        'x-platform': 'Web',
        'x-playbackid': uniqueid,
    }
    
    def WV_Function(pssh, lic_url, cert_b64=None):
        wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)                   
        widevine_license = requests.post(url=lic_url, data=wvdecrypt.get_challenge(), headers=headers, verify=False)
        license_b64 = b64encode(widevine_license.content)
        wvdecrypt.update_license(license_b64)
        Correct, keyswvdecrypt = wvdecrypt.start_process()
        if Correct:
            return Correct, keyswvdecrypt
    Correct, keys = WV_Function(pssh, lic_url)
    
    for key in keys:
        print('--key ' + key)
    
    ke_ys = ' '.join([f'--key {key}' for key in keys]).split()
    
    print()
    subprocess.run([m3u8DL_RE,
                    '-M', 'format=mkv:muxer=ffmpeg',
                    '--concurrent-download',
                    '--log-level', 'INFO',
                    '--save-name', 'video', mpd, *ke_ys])

except IndexError: #DRM free
    print()
    subprocess.run([m3u8DL_RE,
                    '-M', 'format=mkv:muxer=ffmpeg',
                    '--concurrent-download',
                    '--log-level', 'INFO',
                    '--save-name', 'video', mpd])

try:
    Path('video.mkv').rename(''+title+'.mkv')
    print(f'{title}.mkv \nall done!\n')
except FileNotFoundError:
    print("[ERROR] no mkv file")

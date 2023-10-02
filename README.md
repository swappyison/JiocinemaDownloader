# JiocinemaDownloader
Download both DRM and DRM free videos from jiocinema
# Steps
NOTE: please move all the python scripts inside WKS folder before proceeding else you will get ModuleNotFoundError: No module named 'pywidevine.L3' error.
1. Install required dependencies (pip3 install -r requirements.txt)
2. run python script in terminal: python3 jiodownloader.py
3. for the field 'accesstoken' copy your own value like this:
![jios](https://github.com/swappyison/JiocinemaDownloader/assets/88504971/8e9eeef6-095b-459d-86bb-1aa945510dd2)

here i went to network tab under developer tools and typed method:POST. I selected the url with key-jiocinema and scrolled down to see the access token value. I then copied it by right clicking on it. (you can use apis-jiocinema.voot link also)

4. Simply copy and paste the jiocinema url
5. Choose which format to download
6. enjoy!
![jiodownloader](https://github.com/swappyison/JiocinemaDownloader/assets/88504971/d66646a6-b848-4140-9da1-29b21302b857)

NOTE: access token can be retrieved through running jioaccess.js, for this run node jioaccess.js (captures dynamically generated access token using pupeteer which emulates browser {needs chromedriver installed}, if your pc has low RAM you can skip this.)

What each script does?
1. Jiodownloader.py -----> downloads a video based on required resolution set by user.
2. Jioscraper.py -----> scraps the list of all episode urls into episode_urls.txt for bulk downloading purpose.
3. JiobulkdownloaderDRM.py -----> downloads all videos scraped under episode_urls.txt with highest possible quality (if not 4k)
4. Jio4k.py -----> bulk downloads 4k supported videos under episode_urls.txt.

UPDATE: Now you can bulk download episodes from jiocinema:
1. run jio.sh
2. enter url of show
3. enter access token
4. enjoy!

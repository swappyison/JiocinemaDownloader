# JiocinemaDownloader
Download both DRM and DRM free videos from jiocinema
NOTE: please move all the python scripts inside WKS folder before proceeding else you will get ModuleNotFoundError: No module named 'pywidevine.L3' error.
# Steps
1. Install required dependencies (pip3 install -r requirements.txt)
2. run python script in terminal: python3 jiodownloader.py
3. for the field 'accesstoken' copy your own value like this:
![SCR-20230819-jqs](https://github.com/swappyison/JiocinemaDownloader/assets/88504971/310d8f8c-2d28-4c13-946c-6c594fc67914)

here i went to network tab under developer tools and typed method:POST. I selected the url with key-jiocinema and scrolled down to see the access token value. I then copied it by right clicking on it. (you can use apis-jiocinema.voot link also)

4. Simply copy and paste the jiocinema url
5. Choose which format to download
6. enjoy!

NOTE: access token can be retrieved through running jioaccess.js, for this run node jioaccess.js

UPDATE: Now you can bulk download episodes from jiocinema:
1. run jio.sh
2. enter url of show
3. enter access token
4. enjoy!

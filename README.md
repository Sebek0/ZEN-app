# ZEN-app
## How to run?
``` 
uvicorn zen_api.main:app --reload
OR
python3 -m uvicorn zen_api.main:app --reload
```

## .Env file
Should contain this variables

```Bungie API KEY can be found on bungie developer portal```
BUNGIE_API_KEY = ''

**Bungie API URLs**
<ul>
<li>MANIFEST_URL = 'http://www.bungie.net/Platform/Destiny2/Manifest/'</li>
<li>GROUP_URL = 'https://www.bungie.net/Platform/GroupV2/'</li>
<li>USER_URL = 'https://www.bungie.net/Platform/User/'</li>
<li>DESTINY2_URL = 'https://www.bungie.net/Platform/Destiny2/'</li>
</ul>

```Auth token contact owner for one```
ZEN_API_TOKEN = ''

```Destiny2 manifest url```
MANIFEST_URL='http://www.bungie.net/Platform/Destiny2/Manifest/'

```Disk where you saved this project ex. C:```
PROJECT_DIR='C:'
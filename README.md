# ZEN-app
## How to run?
``` 
uvicorn zen_api.main:app --reload
```

## .Env file
Should contain this variables

```Bungie API KEY can be found on bungie developer portal```
BUNGIE_API_KEY = ''

```Bungie API URLs```
MANIFEST_URL = 'http://www.bungie.net/Platform/Destiny2/Manifest/'
GROUP_URL = 'https://www.bungie.net/Platform/GroupV2/'
USER_URL = 'https://www.bungie.net/Platform/User/'
DESTINY2_URL = 'https://www.bungie.net/Platform/Destiny2/'

```Auth token contact owner for one```
ZEN_API_TOKEN = ''

```Destiny2 manifest url```
MANIFEST_URL='http://www.bungie.net/Platform/Destiny2/Manifest/'

```Disk where you saved this project ex. C:```
PROJECT_DIR='C:'
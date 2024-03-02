### Simple Google Spreadsheets Python Client
Simple client with all the dependencies and docs links 
___ 
{как получить google service account} 

{не забыть напомнить про включение APIшек, дать ссылки}
___
To install all dependencies: 
`
pip install -r requirements.txt
`
___
If you want to store credentials of your service account on your machine, I would recommend you to save your credential file in one place on your computer and to [add path to you credential file a environment variable](https://dvmn.org/encyclopedia/pip/pip_requirements_txt/). 

Example of use:

```python
import os
from simple_google_client import GoogleClient

google_service = GoogleClient(os.getenv("GOOGLE_TOKEN_PATH"))
```

### ✨[The Only Nice Google Documentation For Spreadsheets API](https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.html)✨
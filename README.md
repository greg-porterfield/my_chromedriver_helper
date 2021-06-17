# my_chromedriver_helper
There might be an easier way to get/keep the chromedriver binary in sync with the latest changes, but I haven't figured it out, so I wrote this  Quick and simple helper class to get latest chromedriver and unzip it into a project bin folder.

It does very little, but what it does is helpful, at least for me.

## how to use this thing?
Put **chromeselenium.py** in a utils directory, or wherever you want.

import it to your project that you are going to be using ChromeDriver in:
```
from utils.chromeselenium import SelChromHelper
```

get an instance of the class, this will check for the existence of the chromedriver binary in a ./bin directory for the project.  If it is found it will also check the version, and get the latest version online:
```
helper = SelChromHelper(auto_update=True)
```
once the helper has been created, the path to the binary can be passed to webdriver and you are ready to go.
```
driver = webdriver.Chrome(helper.bin_path, options=options)
```

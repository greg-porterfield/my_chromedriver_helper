import pathlib
import os
import sys
import requests
from subprocess import check_output
import zipfile

class SelChromHelper:
    def __init__(self, auto_update=False, path_to_binary=''):
        if path_to_binary == '':
            self.bin_path = self._default_path_to_driver()    
        else:
            self.bin_path = path_to_binary

        self.platform = sys.platform
        
        if auto_update == True:
            self.GetLatestChromeDriver()
        
    def CheckForUpdate(self):
        if self._chromedriver_exists():    
            local_version = self._get_local_chromedriver_version()
        else:
            local_version = "Not Found"
        
        online_version = self._get_online_chromedriver_version()
        
        if local_version == online_version:
            return 0
        else:
            print(f"Local ChromeDriver version {local_version=} {online_version=}")
            return 1

    def GetLatestChromeDriver(self):
        self._unzip_downloaded_file(self._download_latest_chromedriver())
        
    def _default_path_to_driver(self):
        my_path = pathlib.Path(__file__)
        bin_dir = os.path.join(my_path.parent.parent.absolute(), "bin", "chromedriver.exe")

        return bin_dir
    
    def _chromedriver_exists(self):
        if self.bin_path:
            return os.path.exists(self.bin_path)
        else:
            return False
    
    def _get_local_chromedriver_version(self):
        output = check_output([self.bin_path, str('-v')])
        output = output.decode('ascii')

        return output.split(' ')[1]

    def _get_online_chromedriver_version(self):
        url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        response = requests.get(url)
        
        return response.text
    
    def _download_latest_chromedriver(self):
        dl_directory = pathlib.Path(self.bin_path).parent
        zip_file_name = dl_directory.joinpath(f"chromedriver_{self.platform}.zip")
        version = self._get_online_chromedriver_version()
        dl_file = f"chromedriver_{self.platform}.zip"
        download_url = f"https://chromedriver.storage.googleapis.com/{version}/{dl_file}"

        if not os.path.exists(dl_directory):
            print("Creating directory for download (and the binary)")
            os.makedirs(dl_directory)
        
        with open(zip_file_name, 'wb') as fh:
            response = requests.get(download_url)
            if response.status_code != 200:
                raise Exception(f"Non 200 request status received {response.statuscode=} {download_url=}")
            else:
                fh.write(response.content)
        
        return zip_file_name
    
    def _unzip_downloaded_file(self, FileName):
        with zipfile.ZipFile(FileName, 'r') as zip_obj:
            extract_path = pathlib.Path(self.bin_path).parent
            for z in [f for f in zip_obj.namelist() if f == 'chromedriver.exe']:
                zip_obj.extract(z, extract_path)

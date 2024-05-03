import util
credentials = util.getCredentials()
import os
import sys
import shutil
import datetime
import glob
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

tec_List = ['GSM', 'WCDMA', 'LTE', 'NR']

script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
download_directory = os.path.join(script_dir, 'import\BaseAnatel')

def cleanFolder(download_directory):
    if os.path.exists(download_directory):
        try:
            shutil.rmtree(download_directory)
            print(f"Deleted folder: {download_directory}")
        except Exception as e:
            print(f"Error deleting folder: {e}")

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

def is_file_same_date(file_path):
    file_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).date()
    today_date = datetime.date.today()
    return file_date != today_date

def getFilesDate(download_directory):
    downloaded_files = os.listdir(download_directory)
    if len(downloaded_files) == 0:
        return True
    for file_name in downloaded_files:
        file_path = os.path.join(download_directory, file_name)
        if is_file_same_date(file_path):
            return True
    print("Ignoring download .zip files as they have the same date as today.")
    return False

def getFileCount():
    downloaded_files = os.listdir(download_directory)
    return len(downloaded_files)

def wait_for_downloads_to_complete():
    while True:
        downloading_files = glob.glob(os.path.join(download_directory, '*.crdownload'))
        print(downloading_files)
        if not downloading_files:
            break
        time.sleep(1)  # Wait for 1 second and then check again

delayTime = 3

def launchBrowser(state, tec_List):
    cleanFolder(download_directory)
    for i in tec_List:
        servico = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(service=servico, options=chrome_options)
        driver.get(credentials['ANATEL_Mosiac'])
        time.sleep(delayTime)
        driver.find_element('xpath','//*[@id="tblFilter"]/span[5]').click()
        time.sleep(delayTime)
        driver.find_element('xpath',f"//*[@id='fc_8']/option[text()='{state}']").click()
        time.sleep(delayTime)
        element = driver.find_element('xpath','//*[@id="fc_11"]')
        element.clear()
        element.send_keys(i)
        element.send_keys(Keys.RETURN)
        time.sleep(20)
        #driver.find_element('xpath','//*[@id="download_filtradas"]').click()
        driver.find_element('xpath','//*[@id="download_csv"]').click()
        time.sleep(delayTime)
        time.sleep(20)

        # Wait for downloads to complete before renaming
        wait_for_downloads_to_complete()

        # Rename the downloaded files
        rename_downloaded_files(i)
        driver.quit()
    print(f'All {str(getFileCount())} archives were downloaded!')

def rename_downloaded_files(ArchiveName):
    downloaded_files = glob.glob(os.path.join(download_directory, '*.zip'))
    if downloaded_files:
        # Sort the files by modification time in descending order
        downloaded_files.sort(key=os.path.getmtime, reverse=True)
        latest_file_path = downloaded_files[0]  # Get the path of the most recent file
        custom_filename = os.path.join(download_directory, f"{ArchiveName}.zip")
        os.rename(latest_file_path, custom_filename)

def download(stade, tec_List):
  while getFilesDate(download_directory) or getFileCount() <= 3:
      launchBrowser(stade, tec_List)

import util
credentials = util.getCredentials()
import os
import sys
import shutil

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


tec_List = ['GSM','WCDMA','LTE','NR','CDMA']

script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
download_directory = os.path.join(script_dir, 'import\BaseAnatel')
if os.path.exists(download_directory):
    # If it exists, delete it and its contents
    try:
        shutil.rmtree(download_directory)
        print(f"Deleted folder: {download_directory}")
    except Exception as e:
        print(f"Error deleting folder: {e}")

# Create the download directory
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Configure Chrome options
chrome_options = Options()

# Specify the download directory using the 'prefs' dictionary
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

#chrome_options.add_argument("--ignore-certificate-errors")

servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=chrome_options)





delayTime = 2
def launchBrowser():
  driver.get(credentials['ANATEL_Mosiac'])
  time.sleep(delayTime)
  driver.find_element('xpath','//*[@id="tblFilter"]/span[5]').click()
  time.sleep(delayTime)
  #driver.find_element('xpath','//*[@id="fc_8"]').click()
  driver.find_element('xpath',"//*[@id='fc_8']/option[text()='SP']").click()
  time.sleep(delayTime)
  
  for i in tec_List:
    element = driver.find_element('xpath','//*[@id="fc_11"]')
    # Clear the input field before sending new keys
    element.clear()
    element.send_keys(i)
    element.send_keys(Keys.RETURN)
    time.sleep(20)
    driver.find_element('xpath','//*[@id="download_filtradas"]').click()
    time.sleep(delayTime)
  



 
 
  




  '''
  driver.find_element('xpath','//*[@id="Uid"]').send_keys(credentials['MS_login'])
  driver.find_element('xpath','//*[@id="Pwd"]').send_keys(credentials['MS_passwd'])
  driver.find_element('xpath','//*[@id="3054"]').click()
  driver.find_element('xpath','//*[@id="projects_ProjectsStyle"]/table/tbody/tr[2]/td[1]/div/table/tbody/tr/td[2]/a').click()
  driver.find_element('xpath','//*[@id="dktpSectionView"]/a[2]/div[1]').click()
  driver.find_element('xpath','//*[@id="FolderIcons"]/tbody/tr[16]/td[2]/div/table/tbody/tr/td[2]/a').click()
  '''  

  while(True):
      pass
launchBrowser()




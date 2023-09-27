import util
credentials = util.getCredentials()

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico)

#driver = webdriver.Chrome(executable_path=r'C:\Users\f8059678\OneDrive - TIM\Dario\@_PYTHON\@Selenium\chromedriver\chromedriver.exe')

def launchBrowser():
  driver.get(credentials['ANATEL_Mosiac'])
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




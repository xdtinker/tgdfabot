import time
import os
import requests
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSessionIdException
from requests.exceptions import Timeout
from urllib3.exceptions import MaxRetryError
from urllib3.exceptions import ProtocolError

#send msg to tg
def sendTelegram(botMsg):
    bot_token = "bot2023896048:AAE_MnkOljwcRXNXlC6ouEwrTpfYZVeRc1c"
    bot_ChatID = "879252455"
    bot_text = f'https://api.telegram.org/{bot_token}/sendMessage?chat_id={bot_ChatID}&text={botMsg}'

    print("Sending message")

    response = requests.get(bot_text)
#logs to messenger
def tgGetLogs(botLogs):
    bot_token = "bot2054859695:AAGVSXp1MRtrAMP0L5g2AML-tBVvwRfxi4o"
    bot_ChatID = "879252455"
    bot_text = f'https://api.telegram.org/{bot_token}/sendMessage?chat_id={bot_ChatID}&text={botLogs}'

    response = requests.get(bot_text)

def webdrv():
    global driver
    site = "https://www.passport.gov.ph/appointment"
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2,
         "profile.default_content_setting_values.notifications":2,
         "profile.managed_default_content_settings.stylesheets":2,
         "profile.managed_default_content_settings.cookies":2,
         "profile.managed_default_content_settings.javascript":1,
         "profile.managed_default_content_settings.plugins":1,
         "profile.managed_default_content_settings.popups":2,
         "profile.managed_default_content_settings.geolocation":2,
         "profile.managed_default_content_settings.media_stream":2,}
    
    chrome_options.add_experimental_option("prefs",prefs)
    
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(site)
    return driver


def closeWebdrv():
    try:
        driver.quit()
        
        tgGetLogs("Service Terminated.\n\nIf you wish to restart the Service use /sudostart\n\n")
    except Exception as e:
        tgGetLogs(f"Service is not running.")



def checkprocess():
    tgGetLogs('testing phase')
    webdrv()
    try:      
        print('browsing in headless mode')
        driver.find_element_by_class_name('checkbox')                                       #checkbox
        tgGetLogs('✅ Step 1.....Passed')
        ######################################### 
        driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/a[1]').click()                 #Start button
        tgGetLogs('✅ Step 2.....Passed')
        #########################################
        time.sleep(2)
        #########################################
        driver.find_element(By.ID, "SiteID").click()                                  #select site number 10
        tgGetLogs('✅ Step 3.....Passed')  
        Select(driver.find_element(By.ID, "SiteID")).select_by_index(10)                                        #select site number 10
        tgGetLogs('✅ Step 4.....Passed')
        #########################################
        time.slepp(1)
        driver.find_element(By.XPATH, "//input[@name='pubpow-notif-checkbox']").click()                        #agree tos
        tgGetLogs('✅ Step 5.....Passed')
        #########################################                                  
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submitcommand"))).click()     #sumbit
        tgGetLogs('✅ Initialization complete. checking started. ')     

        loop = True
        sites = [1,2,3,4,5,7,8,9]
        while loop:
            for option in sites:
                sitename = "sitename"
                ####GET TIME####
                time.sleep(3)
                slot = driver.find_element(By.XPATH, "//div[@id='schedule-container']").text
                Select(driver.find_element(By.ID, "SiteID")).select_by_index(option)
                today = datetime.now()
                dateToday = today.strftime("%m/%d/%Y %I:%M %p")


                if(option == 1):
                    sitename = "Robinsons Las Pinas - Temporary Off-site Passport Service"
                elif(option == 2):
                    sitename = "Robinsons Magnolia - Temporary Off-site Passport Service"
                elif(option == 3):
                    sitename = "SM Aura - Temporary Off-site Passport Service"
                elif(option == 4):
                    sitename = "SM Mall of Asia - Temporary Off-site Passport Service"
                elif(option == 5):
                    sitename = "SM North Edsa -Temporary Off-site Passport Service"
                elif(option == 7):
                    sitename = "Newport Mall - Temporary Off-site Passport Service"
                elif(option == 8):
                    sitename = "San Pedro Laguna - Temporary Off-site Passport Service"
                else:
                    sitename = "SM Seaside Cebu - Temporary Off-site Passport Service"


                if("Timeslots will be available soon." in slot):
                    tgGetLogs(f"NO APPOINTMENT AVAILABLE\n  \n{sitename}\n \n{dateToday}\n")
                    print(f"\n*************************** NO APPOINTMENT AVAILABLE IN {sitename} ***************************\n")              
                else:
                    print(f"\n********************** APPOINTMENT AVAILABLE IN {sitename} ***********************************\n")
                    #sendMsg()
                    sendTelegram(f' **New Appointment**\n \nSITE : {sitename}\n \n{dateToday}\n')  
                    print("Message sent.")

    except (ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, InvalidSessionIdException, Timeout) as e:
        tgGetLogs(f'❌ Error occured:  {e.msg}\n\nuse /sudostart to restart the process.\n\n')
    except (MaxRetryError, ProtocolError) as e:
        print(f' Error occured: {e.args}\n\nuse /sudostart to restart the process.\n\n')
    except ConnectionError as e:
        print(f' Error occured: Connection aborted')
    except AttributeError as e:
        tgGetLogs(f'❌ Error occured:  {e.name}\n\nuse /sudostart to restart the process.\n\n')
    finally:
        closeWebdrv()

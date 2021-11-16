
import time
import os
import requests
import pytz
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
from urllib3.exceptions import MaxRetryError, TimeoutStateError
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

def web_driver():
    global driver
    site = "https://www.passport.gov.ph/appointment"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    driver.get(site)
    return driver

def kill_driver():
    try:
        driver.quit()    
        tgGetLogs("Process ended.\n\nIf you wish to restart the service use /sudostart\n\n")
    except Exception as e:
        tgGetLogs(f"No process running.")


def start_driver():
    #initialize web driver
    web_driver()
    try:
        driver.find_element_by_class_name('checkbox').click()                                          #checkbox
        tgGetLogs('✅ Step 1.....Passed')
        #########################################
        driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/a[1]').click()                #Start button
        tgGetLogs('✅ Step 2.....Passed')
        #########################################
        driver.implicitly_wait(5)  
        #########################################)                              #select site number 10
        tgGetLogs('✅ Step 3.....Passed') 
        select = Select(driver.find_element(By.ID, "SiteID"))
        select.select_by_index(10)                                       #select site number 10
        #########################################
        time.sleep(10)                               
        tos = driver.find_element_by_xpath('//*[@id="pubpow-notif"]/label')
        driver.implicitly_wait(5)
        tos.click()
        tgGetLogs('✅ Step 4.....Passed')
        #########################################                                  
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submitcommand"))).click()     #sumbit
        tgGetLogs('✅ Initialization complete. checking started. \n\n  @DFAPassport_bot')     

        loop = True
        sites = [1,2,3,4,5,7,8,9]
        while loop:
            for option in sites:
                sitename = "sitename"
                ####GET TIME####
                time.sleep(3)
                date = driver.find_element(By.ID, "next-available-date").text
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


                if("No available date" in date):
                    tgGetLogs(f"❌NO APPOINTMENT AVAILABLE\n  \n{sitename}\n \n{dateToday}\n")
                    print(f"\n*************************** NO APPOINTMENT AVAILABLE IN {sitename} ***************************\n")              
                else:
                    print(f"\n********************** APPOINTMENT AVAILABLE IN {sitename} ***********************************\n")
                    #sendMsg()
                    sendTelegram(f'✅New Appointment\n \nSite: {sitename}\nEarliest available date: {date}\n\n{dateToday}\n')  
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
        driver.quit()
        print('driver closed.')
        tgGetLogs('driver closed.')

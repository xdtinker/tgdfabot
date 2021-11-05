import os
import telebot
import constant as keys
import smtplib
import time
import os
import requests
from selenium.webdriver.support.color import Color
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

bot = telebot.TeleBot(keys.API_KEY)
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

site = "https://www.passport.gov.ph/appointment"
path = "C:/Users/Aziz/Desktop/Automation/chromedriver.exe"

def sendTelegram(botMsg):
    bot_token = "bot2023896048:AAE_MnkOljwcRXNXlC6ouEwrTpfYZVeRc1c"
    bot_ChatID = "879252455"
    bot_text = f'https://api.telegram.org/{bot_token}/sendMessage?chat_id={bot_ChatID}&text={botMsg}'

    response = requests.get(bot_text)
    
def tgGetLogs(botLogs):
    bot_token = "bot2054859695:AAGVSXp1MRtrAMP0L5g2AML-tBVvwRfxi4o"
    bot_ChatID = "879252455"
    bot_text = f'https://api.telegram.org/{bot_token}/sendMessage?chat_id={bot_ChatID}&text={botLogs}'

    response = requests.get(bot_text)

def main():
    tgGetLogs("Process has started")
    #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
    user-agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    driver.get(site)

    time.sleep(3)
    try:
        driver.find_element(By.CLASS_NAME, "checkbox").click()                                                  #checkbox
        print('step 1')                                             
        driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/a[1]').click()                 #Start button
        print('step 2')
        time.sleep(3)                 
        driver.find_element(By.ID, "SiteID").click()                                                            #site selection
        print('step 3')                                                            
        Select(driver.find_element(By.ID, "SiteID")).select_by_index(10)                                        #select site number 10
        print('step 4')
        time.sleep(3)                                         
        driver.find_element_by_xpath('//*[@id="pubpow-notif"]/label').click()                                 #agree tos
        print('step 5')                                  
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submitcommand"))).click()     #sumbit
        print('Process done')  
   
        loop = True
        sites = [1,2,3,4,5,7,8,9]
        while loop:
            for option in sites:
                time.sleep(5)
                timeSlots = driver.find_element(By.ID, "schedule-container").text
                Select(driver.find_element(By.ID, "SiteID")).select_by_index(option)
                sitename = ""
                ####GET TIME####
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

                if("Timeslots will be available soon." in timeSlots):
                    tgGetLogs(f"NO APPOINTMENT AVAILABLE\n  \n{sitename}\n \n{dateToday}\n")
                    print(f"\n*************************** NO APPOINTMENT AVAILABLE IN {sitename} ***************************\n")
                    time.sleep(3)                   
                else:
                    print(f"\n********************** APPOINTMENT AVAILABLE IN {sitename} ***********************************\n")
                    #sendMsg()
                    sendTelegram(f' **New Appointment**\n \nSITE : {sitename}\n \n{dateToday}\n')  
                    print("Message sent.")      
    except (NoSuchElementException,TimeoutException) as e:
        tgGetLogs(f"\nError occured during process.\n \nError Message: {e.args}\n")
        driver.quit()

@bot.message_handler(commands=['start'])
def response(message):
    bot.send_message(message.chat.id, 'Greetings, Human.')

@bot.message_handler(commands=['hi'])
def response(message):
    bot.send_message(message.chat.id, 'Hi Dev')
 
@bot.message_handler(commands=['help'])
def response(message):
    bot.send_message(message.chat.id, "There's no help")

@bot.message_handler(commands=['sudostart'])
def response(message):
    bot.send_message(message.chat.id, 'Ok. It might take a while to initialize please be patient.')
    main()

@bot.message_handler(commands=['sudostop'])
def response(message):
    bot.send_message(message.chat.id, 'Process terminated')
    driver.quit()

bot.polling()

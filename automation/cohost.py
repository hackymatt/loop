import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# load environment variables from .env file
load_dotenv()

# read email and password from environment variables
email = os.getenv("MEETINGS_EMAIL")
password = os.getenv("MEETINGS_PASSWORD")

# check if email or password is missing
if not email:
    raise ValueError("Email is missing from the environment variables.")
if not password:
    raise ValueError("Password is missing from the environment variables.")


# set options and driver
service = webdriver.ChromeService(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-search-engine-choice-screen")
driver = webdriver.Chrome(service=service, options=chrome_options)

# login to google
driver.get("https://accounts.google.com/signin")
time.sleep(5)

# enter email
email_input = driver.find_element(By.ID, "identifierId")
email_input.send_keys(email)
email_input.send_keys(Keys.ENTER)
time.sleep(2)

# enter password
password_input = driver.find_element(By.NAME, "Passwd")
password_input.send_keys(password)
password_input.send_keys(Keys.ENTER)
time.sleep(5)

# find tomorrow date
# tomorrow = datetime.now() + timedelta(days=1)
tomorrow = datetime.now() - timedelta(days=1)
formatted_date = f"{tomorrow.year}/{tomorrow.month}/{tomorrow.day}"

# open day calendar
driver.get(f"https://calendar.google.com/calendar/u/0/r/day/{formatted_date}?pli=1")
time.sleep(5)

# find events
events = driver.find_elements(By.XPATH, "//div[@role='gridcell']//div[@role='button']")

# iterate over events
for event in events:
    # open event
    event.click()
    time.sleep(2)

    # edit event
    edit_button = driver.find_element(By.XPATH, "//button[@aria-label='Edit event']")
    edit_button.click()
    time.sleep(5)

    # video call options
    options_button = driver.find_element(
        By.XPATH, "//button[@aria-label='Video call options']"
    )
    options_button.click()
    time.sleep(5)

    # TODO: add cohost

    # switch to video call options frame
    iframe_element = driver.find_element(
        By.XPATH, "//iframe[@title='Video call options']"
    )
    driver.switch_to.frame(iframe_element)
    time.sleep(2)

    # save video call options
    save_button = driver.find_element(By.XPATH, "//span[text()='Save']")
    save_button.click()
    time.sleep(2)

    # switch back to main window
    driver.switch_to.default_content()
    time.sleep(2)

    # save meeting
    save_button = driver.find_element(By.XPATH, "//button[@aria-label='Save']")
    save_button.click()
    time.sleep(2)


# close browser
driver.quit()

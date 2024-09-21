import os
import time
import urllib.parse
from dotenv import load_dotenv


from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def send_messages(email, password, query, message):
    # set options and driver
    service = webdriver.ChromeService(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # login to linkedin
    driver.get("https://www.linkedin.com/login")

    # enter email
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(email)

    # enter password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    query_encoded = urllib.parse.quote(query)

    # search for term
    people_url = "https://www.linkedin.com/search/results/people/"
    driver.get(
        f"{people_url}?keywords={query_encoded}&origin=SWITCH_SEARCH_VERTICAL&sid=aAl"
    )
    time.sleep(5)

    # determine last page number
    pagination = driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator")
    if pagination:
        last_page = int(pagination[-1].text)
    else:
        last_page = 1

    # iterate over pages
    sent_messages = 0
    not_sent_messages = 0
    for page in range(1, last_page):
        # search for page
        driver.get(
            f"{people_url}?keywords={query_encoded}&origin=SWITCH_SEARCH_VERTICAL&page={page}&sid=aAl"
        )
        time.sleep(5)

        # get results
        profiles = driver.find_elements(
            By.CLASS_NAME, "reusable-search__result-container"
        )

        # iterate over profiles
        for profile in profiles:
            try:
                # open profile in new tab
                profile_link = profile.find_element(By.CSS_SELECTOR, "a").get_attribute(
                    "href"
                )
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(profile_link)
                time.sleep(5)

                # click message button
                message_button = driver.find_elements(
                    By.XPATH, "//button[contains(@aria-label, 'Message')]"
                )[1]
                message_button.click()
                time.sleep(2)

                # check if message box opened
                message_boxes = driver.find_elements(
                    By.CSS_SELECTOR, "div.msg-form__contenteditable"
                )
                if len(message_boxes) > 0:
                    # enter message text
                    message_box = message_boxes[0]
                    message_box.send_keys(message)
                    time.sleep(2)

                    # send message
                    # send_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                    # send_button.click()
                    sent_messages += 1
                else:
                    print(f"Could not send message for profile: {profile_link}")
                    not_sent_messages += 1

            except Exception as error:
                not_sent_messages += 1
                print(f"Could not send message for profile. Error: {error}")
                continue

            # close profile tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            success_rate = (sent_messages / (sent_messages + not_sent_messages)) * 100
            print(f"Success rate: {success_rate:.2f}%")

    # close browser
    driver.quit()


if __name__ == "__main__":
    # load environment variables from .env file
    load_dotenv()

    # read email and password from environment variables
    email_secret = os.getenv("LINKEDIN_EMAIL")
    password_secret = os.getenv("LINKEDIN_PASSWORD")

    # check if email or password is missing
    if not email_secret:
        raise ValueError("Email is missing from the environment variables.")
    if not password_secret:
        raise ValueError("Password is missing from the environment variables.")

    send_messages(
        email=email_secret,
        password=password_secret,
        query="nauczyciel programowania",
        message="Cześć",
    )

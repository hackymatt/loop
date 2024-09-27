import os
import sys
import time
import urllib.parse
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import set_up_chrome, record_exists_in_file, append_to_file


def send_messages(email, password, tracker_path, query, message):
    # set options and driver
    driver = set_up_chrome()

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
        f'{people_url}?geoUrn=%5B"105072130"%5D&keywords={query_encoded}&origin=SWITCH_SEARCH_VERTICAL&sid=aAl'
    )
    time.sleep(10)

    # Scroll to ensure any lazy-loaded elements are rendered
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(10)

    # determine last page number
    pagination = driver.find_elements(By.XPATH, '//ul[contains(@class, "artdeco-pagination__pages")]/li')

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
            f'{people_url}?geoUrn=%5B"105072130"%5D&keywords={query_encoded}&origin=SWITCH_SEARCH_VERTICAL&page={page}&sid=aAl'
        )
        time.sleep(5)

        # get results
        profiles = driver.find_elements(
            By.CLASS_NAME, "reusable-search__result-container"
        )

        # iterate over profiles
        for profile in profiles:
            profile_opened = False
            try:
                # open profile in new tab
                profile_link = profile.find_element(By.CSS_SELECTOR, "a").get_attribute(
                    "href"
                )
                if not record_exists_in_file(
                    file_path=tracker_path, record=profile_link
                ):
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(profile_link)
                    profile_opened = True
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
                        append_to_file(
                            file_path=tracker_path,
                            text=";".join([profile_link, "True"]),
                        )
                    else:
                        print(f"Could not send message for profile: {profile_link}")
                        sys.stdout.flush()
                        not_sent_messages += 1
                        append_to_file(
                            file_path=tracker_path,
                            text=";".join([profile_link, "False"]),
                        )
                else:
                    print(f"Skipping profile: {profile_link}")
                    sys.stdout.flush()
                    sent_messages += 1

            except Exception as error:
                not_sent_messages += 1
                print(f"Could not send message for profile. Error: {error}")
                sys.stdout.flush()
                continue

            # close profile tab
            if profile_opened:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            success_rate = (sent_messages / (sent_messages + not_sent_messages)) * 100
            print(f"Success rate: {success_rate:.2f}%")
            sys.stdout.flush()

    # close browser
    driver.quit()


if __name__ == "__main__":
    # load environment variables from .env file
    load_dotenv()

    # read email and password from environment variables
    email_secret = os.getenv("LINKEDIN_EMAIL")
    password_secret = os.getenv("LINKEDIN_PASSWORD")
    tracker_path_secret = os.getenv("TRACKER_PATH")

    # check if email or password is missing
    if not email_secret:
        raise ValueError("Email is missing from the environment variables.")
    if not password_secret:
        raise ValueError("Password is missing from the environment variables.")
    if not tracker_path_secret:
        raise ValueError("Tracker path is missing from the environment variables.")

    try:
        send_messages(
            email=email_secret,
            password=password_secret,
            tracker_path=tracker_path_secret,
            query="(instruktor OR nauczyciel OR wykładowca OR trener OR lecturer) AND (Giganci Programowania)",
            message="Cześć",
        )
    except Exception as error:
        print(error)
        sys.stdout.flush()

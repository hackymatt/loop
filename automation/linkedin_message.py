import os
import sys
import time
import urllib.parse
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utils import set_up_chrome, record_exists_in_file, append_to_file, random_scroll
import random


def send_messages(
    email, password, tracker_path, message_limit, query, message, short_message
):
    # set options and driver
    driver = set_up_chrome()

    # login to linkedin
    driver.get("https://www.linkedin.com/login")

    time.sleep(5)

    # enter email
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(email)

    # enter password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(15)

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
    pagination = driver.find_elements(
        By.XPATH, '//ul[contains(@class, "artdeco-pagination__pages")]/li'
    )

    if pagination:
        last_page = int(pagination[-1].text)
    else:
        last_page = 1

    # iterate over pages
    sent_messages = 0
    not_sent_messages = 0
    early_exit = False
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

                    name_element = driver.find_element(By.TAG_NAME, "h1")
                    full_name = name_element.text
                    first_name = full_name.split()[0]

                    random_scroll(driver=driver, duration=random.randint(10, 30))

                    # click message button
                    message_button = driver.find_elements(
                        By.XPATH, "//button[contains(@aria-label, 'Message')]"
                    )[1]
                    message_button.click()
                    time.sleep(5)

                    # check if message box opened
                    message_boxes = driver.find_elements(
                        By.XPATH,
                        "//header//h2[text()='New message']//following::div[contains(@class, 'msg-form__contenteditable')]",
                    )
                    if len(message_boxes) > 0:
                        message_box = message_boxes[0]

                        time.sleep(15)

                        # enter message text
                        message_box.send_keys(message.replace("[Imię]", first_name))
                        time.sleep(15)

                        # send message
                        send_button = driver.find_element(
                            By.XPATH, "//button[@type='submit']"
                        )
                        send_button.click()
                        sent_messages += 1
                        append_to_file(
                            file_path=tracker_path,
                            text=";".join([profile_link, "True"]),
                        )
                    else:
                        print(f"Could not send message for profile: {profile_link}")
                        sys.stdout.flush()

                        try:
                            dismiss_button = driver.find_element(
                                By.XPATH,
                                "//button[@aria-label='Dismiss']",
                            )
                            dismiss_button.click()
                            time.sleep(2)

                            invite_button = driver.find_element(
                                By.XPATH,
                                "//button[@aria-label[contains(., 'Invite')] and contains(@class, 'artdeco-button--primary') and contains(@class, 'pvs-profile-actions__action')]",
                            )
                            invite_button.click()
                            time.sleep(2)

                            note_button = driver.find_element(
                                By.XPATH,
                                "//button[@aria-label='Add a note']",
                            )
                            note_button.click()
                            time.sleep(2)

                            message_box = driver.find_element(
                                By.XPATH,
                                "//textarea[@name='message']",
                            )
                            # enter message text
                            message_box.send_keys(
                                short_message.replace("[Imię]", first_name)
                            )
                            time.sleep(15)

                            # send message
                            send_button = driver.find_element(
                                By.XPATH,
                                "//button[@aria-label='Send invitation']",
                            )
                            send_button.click()
                            sent_messages += 1
                            append_to_file(
                                file_path=tracker_path,
                                text=";".join([profile_link, "True"]),
                            )
                            if sent_messages == message_limit:
                                print(f"Reached message limit: {message_limit}")
                                sys.stdout.flush()
                                early_exit = True
                                break
                        except:
                            not_sent_messages += 1
                            append_to_file(
                                file_path=tracker_path,
                                text=";".join([profile_link, "False"]),
                            )
                else:
                    print(f"Skipping profile: {profile_link}")
                    sys.stdout.flush()
                    sent_messages += 1
                    if sent_messages == message_limit:
                        print(f"Reached message limit: {message_limit}")
                        sys.stdout.flush()
                        early_exit = True
                        break

            except Exception as error:
                not_sent_messages += 1
                print(f"Could not send message for profile. Error: {error}")
                sys.stdout.flush()
                continue

            # close profile tab
            if profile_opened:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(random.uniform(10, 60))  # random delay

            success_rate = (sent_messages / (sent_messages + not_sent_messages)) * 100
            print(f"Success rate: {success_rate:.2f}%")
            sys.stdout.flush()

        if early_exit:
            print("Exiting earlier due to message limit.")
            sys.stdout.flush()
            break

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
            message_limit=100,
            query="(instruktor OR nauczyciel OR wykładowca OR trener OR lecturer) AND (Coders Lab)",
            message="""Cześć [Imię]!

Piszę do Ciebie, bo prowadzę nowo otwartą szkołę programowania online, loop, i uważam, że mógłbyś/mogłabyś świetnie wpasować się do naszego zespołu instruktorów! Stawiamy na elastyczność — każdy instruktor sam ustala swój grafik w 30-minutowych slotach, co daje pełną kontrolę nad czasem pracy.

Oferujemy różne formy wynagrodzenia do wyboru: stawkę godzinową, prowizyjną lub mieszaną. Chętnie porozmawiamy o Twoich oczekiwaniach finansowych, więc śmiało podaj nam swoją propozycję stawki!

Dopiero zaczynamy, więc dołączając teraz, będziesz mieć realny wpływ na rozwój naszej szkoły. Zachęcamy również do proponowania swoich kursów — napisz, czego chciałbyś/chciałabyś uczyć lub w jakich tematach mógłbyś/mogłabyś prowadzić zajęcia. Materiały są podzielone na lekcje, więc nie musisz znać się na całym kursie, wystarczy, że będziesz prowadzić wybrane zajęcia zgodne z Twoją specjalizacją.

Współpracujemy na umowę zlecenie lub B2B, zależnie od preferencji. Naszym celem jest stworzenie szkoły, która oferuje praktyczne umiejętności dostosowane do rynku, a jednocześnie pozwala instruktorom na pełną swobodę i satysfakcjonującą współpracę.

Będzie mi bardzo miło, jeśli zajrzysz na naszą stronę: https://loop.edu.pl i dowiesz się więcej. Jeśli masz pytania lub chciałbyś/chciałabyś omówić szczegóły, jestem do dyspozycji.

Pozdrawiam serdecznie,
Mateusz Szczepek
Założyciel szkoły loop""",
            short_message="""Cześć [Imię]!

Piszę do Ciebie, bo prowadzę nowo otwartą szkołę programowania online, https://loop.edu.pl, i uważam, że pasujesz do naszego zespołu instruktorów! Jeśli masz pytania, jestem do dyspozycji.

Pozdrawiam serdecznie,
Mateusz Szczepek
Założyciel szkoły loop""",
        )
    except Exception as error:
        print(error)
        sys.stdout.flush()

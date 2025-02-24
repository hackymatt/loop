import os
import sys
import time
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils import set_up_chrome, record_exists_in_file, append_to_file, random_scroll
import random


def get_categories(folder_path):
    # set options and driver
    driver = set_up_chrome()

    main_url = "https://aleo.com/pl/firmy"
    driver.get(main_url)
    time.sleep(10)

    categories = driver.find_elements(
        By.XPATH, "//app-root-category-tree//span[@class='space-x-2']"
    )

    categories_dict = {}
    for category in categories:
        category_element = category.find_element(By.CSS_SELECTOR, "a")
        category_url = category_element.get_attribute(
            "href"
        )
        category_name = category_element.text
        category_folder = f"{folder_path}\\{category_name}"
        os.makedirs(category_folder, exist_ok=True)
        categories_dict[category_name] = {"url": category_url, "folder": category_folder}

    return categories_dict


def get_subcategories(folder_path, category_url):
    # set options and driver
    driver = set_up_chrome()

    driver.get(category_url)
    time.sleep(10)

    subcategories = driver.find_elements(
        By.XPATH, "//app-catalog-menu//span[contains(@class, 'space-x-1')]"
    )

    subcategories_dict = {}
    for subcategory in subcategories:
        subcategory_element = subcategory.find_element(By.CSS_SELECTOR, "a")
        subcategory_url = subcategory_element.get_attribute(
            "href"
        )
        subcategory_name = subcategory_element.text
        subcategory_folder = f"{folder_path}\\{subcategory_name}"
        os.makedirs(subcategory_folder, exist_ok=True)
        subcategories_dict[subcategory_name] = {"url": subcategory_url, "folder": subcategory_folder}

    return subcategories_dict

def get_data(
    folder_path, subcategory_url
):
    tracker_path = f"{folder_path}\\data.txt"
    headers = ";".join(["CompanyName", "NIP", "Address", "Website", "Email", "PhoneNumber", "Url"]) + "\n"

    # Create the file and write headers if it does not exist
    if not os.path.exists(tracker_path):
        with open(tracker_path, "w", encoding="utf-8") as file:
            file.write(headers)

    # set options and driver
    driver = set_up_chrome()
    # search for term
    driver.get(subcategory_url)

    # determine last page number
    pagination = driver.find_elements(
        By.XPATH, "//app-catalog-pagination//nav//ul//li"
    )

    if pagination:
        last_page = int(pagination[-2].text)
    else:
        last_page = 1

    print(f"Last page: {last_page}")
    sys.stdout.flush()

    # iterate over pages
    for page in range(1, last_page):
        # search for page
        driver.get(f"{subcategory_url}/{page}")

        # get results
        records = driver.find_elements(
            By.XPATH, "//app-base-catalog-row"
        )

        # iterate over profiles
        for record in records:
            opened = False
            try:
                link = record.find_element(By.CSS_SELECTOR, "a").get_attribute(
                    "href"
                )
                print(f"Reading: {link}")
                sys.stdout.flush()

                if not record_exists_in_file(
                    file_path=tracker_path, record=link
                ):
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(link)
                    opened = True

                    time.sleep(10)

                    try:
                        name_element = driver.find_element(By.XPATH, "//span[contains(@class, 'text-company-name')]")
                        company_name = name_element.text
                    except NoSuchElementException:
                        company_name = ""

                    try:
                        nip_element = driver.find_element(By.XPATH, "//div[contains(@class, 'tax-id')]//span[contains(@class, 'pre-mobile:text-xs-small-line')]")
                        nip_number = nip_element.text
                    except NoSuchElementException:
                        nip_number = ""

                    try:
                        address_element = driver.find_element(By.XPATH, "//div[contains(@class, 'address-data')]")
                        address = address_element.text
                    except NoSuchElementException:
                        address = ""

                    try:
                        phone_element = driver.find_element(By.XPATH, "//app-company-contact//div[contains(@class, 'phone')]//span[contains(@class, 'questo-paywall')]")
                        phone_number = phone_element.text
                    except NoSuchElementException:
                        phone_number = ""

                    try:
                        website_element = driver.find_element(By.XPATH, "//app-company-contact//div[contains(@class, 'site')]//span[contains(@class, 'questo-paywall')]")
                        website = website_element.text
                    except NoSuchElementException:
                        website = ""

                    try:
                        email_element = driver.find_element(By.XPATH, "//app-company-contact//div[contains(@class, 'e-mail ')]//span[contains(@class, 'questo-paywall')]")
                        email = email_element.text
                    except NoSuchElementException:
                        email = ""

                    random_scroll(driver=driver, duration=random.randint(10, 30))

                    time.sleep(random.uniform(1, 5))

                    append_to_file(
                        file_path=tracker_path,
                        text=";".join([company_name, nip_number, address, website, email, phone_number, link]),
                    )
                else:
                    print(f"Skipping record: {link}")
                    sys.stdout.flush()

            except Exception as error:
                print(f"Could not get record. Error: {error}")
                sys.stdout.flush()
                continue

            # close tab
            if opened:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(random.uniform(10, 30))  # random delay

    # close browser
    driver.quit()


if __name__ == "__main__":
    # load environment variables from .env file
    load_dotenv()

    folder_path_secret = "C:\\Users\\szcze\\OneDrive\\Pulpit\\aleo"

    if not folder_path_secret:
        raise ValueError("Tracker path is missing from the environment variables.")

    try:
        categories = get_categories(folder_path=folder_path_secret)
        for category_key, category in categories.items():
            print(f"Reading category {category_key}")
            sys.stdout.flush()
            subcategories = get_subcategories(folder_path=category["folder"], category_url=category["url"])
            for subcategory_key, subcategory in subcategories.items():
                print(f"Reading subcategory {subcategory_key}")
                sys.stdout.flush()
                get_data(folder_path=subcategory["folder"], subcategory_url=subcategory["url"])
    except Exception as error:
        print(error)
        sys.stdout.flush()

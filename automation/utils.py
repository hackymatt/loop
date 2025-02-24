import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import random


def set_up_chrome():
    service = webdriver.ChromeService(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=service, options=chrome_options)


def record_exists_in_file(file_path, record):
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return record in content


def append_to_file(file_path, text):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(text + "\n")


def random_scroll(driver, duration):
    start_time = time.time()
    scrolling_down = True  # Start by scrolling down

    while time.time() - start_time < duration:
        scroll_distance = random.randint(100, 300)  # Random scroll distance
        scroll_pause = random.uniform(0.5, 2)  # Random pause

        if scrolling_down:
            driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        else:
            driver.execute_script(f"window.scrollBy(0, {-scroll_distance});")

        time.sleep(scroll_pause)

        # Get current scroll position
        current_scroll = driver.execute_script("return window.scrollY;")
        max_scroll = driver.execute_script("return document.body.scrollHeight - window.innerHeight;")

        # If we reach the bottom, start scrolling up
        if current_scroll >= max_scroll:
            scrolling_down = False

        # If we reach the top, start scrolling down
        elif current_scroll <= 0:
            scrolling_down = True

    driver.execute_script("window.scrollTo(0, 0);")

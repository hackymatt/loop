import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def set_up_chrome():
    service = webdriver.ChromeService(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-search-engine-choice-screen")
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

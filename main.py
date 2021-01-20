import os
from time import sleep
from typing import List

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

SCREEN_COUNT = 0


def take_screenshot(driver: WebDriver) -> None:
    global SCREEN_COUNT
    SCREEN_COUNT += 1
    print(f"Screenshot for step {SCREEN_COUNT}")
    driver.get_screenshot_as_file(f"screenshots/step_{SCREEN_COUNT}.png")


def create_driver() -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def login(driver: WebDriver, username: str, password: str) -> None:
    input_username = driver.find_element_by_css_selector("input#username")
    input_username.send_keys(username)
    input_password = driver.find_element_by_css_selector("input#password")
    input_password.send_keys(password)
    sleep(.1)
    take_screenshot(driver)
    driver.find_element_by_css_selector("button[type='submit']").click()


def get_grades(driver: WebDriver) -> List[dict]:
    carousel = driver.find_element_by_css_selector(".carrouselwidget0 ul")
    carousel_next = driver.find_element_by_css_selector(".carrouselwidget0 .ui-carousel-next-button")

    grades_count = len(driver.find_elements_by_css_selector(".carrouselwidget0 ul > li"))
    grade_list = list()

    for _ in range(grades_count):
        take_screenshot(driver)
        grade = carousel.text.split("\n")
        grade_list.append({
            "grade": grade[0],
            "subject": grade[1],
            "date": grade[2]
        })
        carousel_next.click()
        sleep(.25)
    return grade_list


def main() -> None:
    driver = create_driver()
    driver.get("https://webaurion.esiee.fr/faces/Login.xhtml")
    take_screenshot(driver)

    login(driver, os.getenv("WEBAURION_USERNAME"), os.getenv("WEBAURION_PASSWORD"))
    for element in get_grades(driver):
        print(element)
    driver.close()


if __name__ == '__main__':
    load_dotenv()
    main()

from random import randint
from time import sleep
from random import triangular
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

from os import system

from Models.modesl import Accounts
from WEB_ELEMENTS import ELEMENTS_GET_USERNAME_ID, ELEMENTS_DM
from parsing_accounts import Scraping
from setting.info import message, information


class InstagramDmBot:
    person = 0
    calculation = 0

    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=option)
        self.scraper = Scraping(self.driver)
        self.driver.maximize_window()
        self.__username = information["USERNAME"]
        self.__password = information["PASSWORD"]
        self.login()

    def login(self):
        system('cls')
        self.driver.get("https://www.instagram.com/")
        sleep(3)
        login_btn = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        login_btn.send_keys(self.__username)
        password_btn = WebDriverWait(self.driver, 15) \
            .until(ec.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
        sleep(triangular(4, 12, 8))
        password_btn.clear()
        password_btn.send_keys(self.__password)
        sleep(triangular(4, 12, 8))
        password_btn.send_keys(Keys.RETURN)
        sleep(5)

    def get_username_id(self, pages, quantity) -> None:
        self.person = 0

        print('Feel free to keep working while we scan for id(s)')

        for page in pages:
            try:
                self.driver.maximize_window()

                self.driver.get(url=f"https://instagram.com/{page}")

                sleep(5)

                info = self.driver.find_elements(By.CLASS_NAME, ELEMENTS_GET_USERNAME_ID["information"])

                if not info:
                    print("Sorry, this page isn't available.")

                    continue

                sleep(5)
                self.driver.get(f'https://instagram.com/{page}/followers')
                sleep(triangular(5, 7, 6))

                self.driver.set_window_size(400, 843)

                sleep(triangular(5, 7, 6))

                list_users = self.scraper.get_accounts(quantity // len(pages))

                self.calculation += len(list_users)

                for user in list_users:
                    Accounts.create(
                        username=user
                    )
            except Exception as e:
                print(f"Sorry, something went wrong! ---> {e}")

                self.get_username_id(pages, quantity)

        sleep(2)

        self.driver.maximize_window()

        self.send_messages(quantity)

    def send_messages(self, quantity):
        self.driver.get('https://www.instagram.com/direct/new/')

        usernames = Accounts.select().filter(Accounts.status == Accounts.PENDING_SEND)[0:quantity]

        try:
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable
                                                 ((By.XPATH, '//button[text() = "Not Now"]'))).click()
        except:
            pass

        sent = 0
        for user in usernames:
            self.driver.get('https://www.instagram.com/direct/new/')

            sleep(5)

            try:
                title = self.driver.find_element(By.CLASS_NAME, ELEMENTS_DM['title'])
            except NoSuchElementException:
                print('ERROR HAS OCCURRED\nThat means maybe about your connection\nor about instagram (account.!)  ')
                continue

            if not title:
                print('ERROR HAS OCCURRED\nThat means maybe about your connection\nor about instagram (account.!)  ')

                continue

            try:
                search_box = self.driver.find_element(By.NAME, ELEMENTS_DM['search_box'])

                sleep(2)

                search_box.click()
            except NoSuchElementException:
                print('ERROR HAS OCCURRED\nThat means maybe about your connection\nor about instagram (account.!)  ')

                continue

            search_box.send_keys(user.username)

            sleep(3)

            try:
                users_elements = self.driver.find_elements(By.CLASS_NAME, ELEMENTS_DM['user_in_dm'])
            except NoSuchElementException:
                print('ERROR HAS OCCURRED\nThat means maybe about your connection\nor about instagram (account.!)  ')

                continue

            try:
                for elem in users_elements:
                    if user.username == elem.text:
                        elem.click()
                        break
            except:
                print('ERROR HAS OCCURRED\nThat means maybe about your connection\nor about instagram (account.!)  ')

                continue

            sleep(5)

            try:
                nxt_btn = self.driver.find_element(By.CLASS_NAME, ELEMENTS_DM['next_btn'])

                nxt_btn.click()
            except NoSuchElementException:
                print('ERROR HAS OCCURRED\nThat means maybe about your connection\nor about instagram (account.!)  ')

                continue

            sleep(10)

            try:
                text_area = self.driver.find_element(By.XPATH, ELEMENTS_DM['text_area'])

                text_area.click()
            except NoSuchElementException:
                print('ERROR HAS OCCURRED\nThat means maybe about your connection\nor about instagram (account.!)  ')

                continue

            sleep(2)

            for char in message["msg"]:
                sleep(randint(1, 2))

                text_area.send_keys(char)

            text_area.send_keys(Keys.ENTER)

            user.status = user.SENT
            user.save()

            sent += 1

            print(sent)

            sleep(10)

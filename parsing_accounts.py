from time import sleep

from parser_elements import parse_web_elements
from selenium.webdriver.common.by import By
from WEB_ELEMENTS import ELEMENTS_GET_USERNAME_ID


class Scraping:

    def __init__(self, driver):
        self.driver = driver

    def get_accounts(self, count) -> list:
        accounts = set()
        scroll_body = self.driver.find_element(By.XPATH, ELEMENTS_GET_USERNAME_ID["f_body"])

        while True:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', scroll_body)

            sleep(2.5)

            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', scroll_body)

            sleep(2.5)

            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', scroll_body)

            accounts.update(self.driver.find_elements(By.CLASS_NAME, ELEMENTS_GET_USERNAME_ID["usernames_elem"]))

            if len(accounts) >= count:
                print('DONE')
                break

        return parse_web_elements(accounts)[0:count]

    @staticmethod
    def parse_elements(elements) -> list:
        unfollow_accounts = list()

        for elem in elements:
            each_user = elem.text.split(' ')

            if each_user[1] == 'started':
                status = tuple(each_user[3].split('.')[-1].split('\n')[0])  # this line returned ('1', '2', 'w')
                # ----> information's what time passed from follow our account, last index is time type
                if status[-1] == 'd':
                    unfollow_accounts.append(each_user[0])
                elif status[-1] == 'w':
                    unfollow_accounts.append(each_user[0])
                elif status[-1] == 'h':
                    data = ', '.join(status)

                    hour = data.replace(', ', '').replace('h', '')

                    if int(hour) >= 24:
                        unfollow_accounts.append(each_user[0])
                else:
                    pass

        return unfollow_accounts

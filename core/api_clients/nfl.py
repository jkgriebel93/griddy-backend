import json
import requests
import time

import browser_cookie3

from typing import Dict

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class NFLProClient:
    access_token_url = settings.NFL_AUTH_URL
    api_base_url = settings.NFL_API_BASE_URL

    def __init__(self):
        with open(settings.NFL_AUTH_REQ_HEADERS_FILE, "r") as infile:
            self.auth_req_headers = json.load(infile)

        with open(settings.NFL_API_REQ_HEADERS_FILE, "r") as infile:
            self.api_req_headers = json.load(infile)

        self.auth_data = self._init_access_token()
        self.api_req_headers["Authorization"] = f"Bearer {self.auth_data['accessToken']}"

        self.auth_data = self._init_access_token()
        self.cookies = browser_cookie3.firefox(cookie_file=settings.FIREFOX_COOKIES_DB)


    def _init_access_token(self) -> Dict:
        access_token_req_payload = {
            "clientKey": settings.NFL_CLIENT_KEY,
            "clientSecret": settings.NFL_CLIENT_SECRET,
            "deviceId": settings.NFL_DEVICE_ID,
            "deviceInfo": settings.NFL_DEVICE_INFO,
            "networkType": settings.NFL_NETWORK_TYPE,
        }

        auth_response = requests.post(self.access_token_url,
                                      headers=self.auth_req_headers,
                                      data=json.dumps(access_token_req_payload))
        auth_response.raise_for_status()
        return auth_response.json()

    def _refresh_access_token(self):
        # TODO: Implement
        pass

    def _api_request(self, method:str, path: str, **kwargs) -> Dict:
        self._refresh_access_token()
        full_url = f"{self.api_base_url}{path}"
        http_method_func = getattr(requests, method.lower())

        response =  http_method_func(full_url,
                                     headers=self.api_req_headers,
                                     cookies=self.cookies,
                                     **kwargs)
        response.raise_for_status()
        requests.get
        return response.json()

    def get_teams(self) -> Dict:
        return self._api_request("get", "/teams/all")

def get_local_storage_item(driver, key):
    return driver.execute_script(f"return window.localStorage.getItem('{key}');")


class NFLProSeleniumClient:
    login_url = settings.NFL_PRO_LOGIN_URL
    pro_stats_url = "https://pro.nfl.com/"

    def __init__(self, email: str = settings.NFL_EMAIL, password: str = settings.NFL_PASSWORD):
        self.email = email
        self.password = password
        self.session_cookies = None
        self.auth_data = None

        options = Options()
        self.driver = webdriver.Chrome(service=Service(),
                                       options=options)

    def _extract_cookies_and_auth(self):
        cookies = self.driver.get_cookies()
        self.session_cookies = {c["name"]: c["value"] for c in cookies}



    def login(self):
        self.driver.get(self.login_url)
        self.driver.find_element(By.ID, "email-input-field").send_keys(self.email)
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(5)
        # TODO: This is brittle - is there a better way?
        password_sign_in_button_xpath = "/html/body/div[1]/div/div/div[2]/div/div[4]/button"
        self.driver.find_element(By.XPATH, password_sign_in_button_xpath).click()
        time.sleep(5)

        self.driver.find_element(By.ID, "password-input-field").send_keys(self.password)
        # Grabbing the _first_ button, which is correct for now
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(5)
        self.driver.get(self.pro_stats_url)
        time.sleep(5)

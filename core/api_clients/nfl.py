import json
import requests

import browser_cookie3

from typing import Dict

from django.conf import settings


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
        return response.json()

    def get_teams(self) -> Dict:
        return self._api_request("get", "/teams/all")
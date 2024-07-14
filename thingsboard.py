import json
import requests

class ThingsBoardAPI:

    tb_url = ""
    username = ""
    password = ""
    token = ""
    s_headers = ""

    def __init__(self):
        print("[ThingsBoard] Thingsboard Init")

    def printHi(self):
        print("hi")

    def login_tb(self, url, username, password):
        self.setURL(url)
        self.setUsername(username)
        self.setPassword(password)
        self.getAuthorizationToken()

    def setURL(self, tb_url):
        self.tb_url = tb_url

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def getURL(self):
        return self.tb_url

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getAuthorizationToken(self, json_login_payload):
        login_head = {"Content-Type": "application/json", "Accept": "application/json"}
        self.session = requests.session()
        tb_login_result = self.session.post(
            self.tb_url + "/api/auth/login",
            data=json_login_payload,
            headers=login_head,
            verify=False,
        )
        print(tb_login_result.text)
        self.token = json.loads(tb_login_result.text)["token"]

    def getAuthorizationToken(self):
        login_head = {"Content-Type": "application/json", "Accept": "application/json"}
        payload = {"username": self.username, "password": self.password}

        json_login_payload = json.dumps(payload)
        self.session = requests.session()
        tb_login_result = self.session.post(
            self.tb_url + "/api/auth/login",
            data=json_login_payload,
            headers=login_head,
            verify=False,
        )
        tb_login_result.raise_for_status()

        print("[ThingsBoard] Access token obtained")
        self.token = json.loads(tb_login_result.text)["token"]  # 2 hour
        self.refreshToken = json.loads(tb_login_result.text)["refreshToken"]  # 7 days

        return self.token

    def refreshAuthorizationToken(self):
        if self.refreshToken is not None:
            header = {"Content-Type": "application/json", "Accept": "application/json"}

            payload = {"refreshToken": self.refreshToken}
            response = self.session.post(
                self.tb_url + "/api/auth/token", json=payload, headers=header
            )
            response.raise_for_status()
            self.token = json.loads(response.text)["token"]

    def HeadersHandling(self):
        if self.token is not None:

            s_headers = {}
            s_headers["Content-Type"] = "application/json"
            s_headers["Accept"] = "application/json"
            s_headers["X-Authorization"] = "Bearer " + self.token
            self.s_headers = s_headers

    def sessionClose(self):
        self.session.close()

    def postTelemetry(self, DeviceToken, payload):
        if self.token is not None:
            self.HeadersHandling()

            url = self.tb_url + "/api/v1/" + DeviceToken + "/telemetry"

            response = self.session.post(url, json=payload, headers=self.s_headers)
            response.raise_for_status()
            print(
                "[ThingsBoard] Post Telemetry Successful"
            )

            return response

    def printWarning(self, string):
        print("\033[2;37;41m " + string + " \033[0;0m")

    def getCurrentAccessToken(self):
        return self.token
from playwright.sync_api import Page

import config


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator('[data-test="username"]')
        self.password = page.locator('[data-test="password"]')
        self.submit = page.locator('[data-test="login-button"]')
        self.error = page.locator('[data-test="error"]')

    def open(self) -> "LoginPage":
        self.page.goto(config.SAUCEDEMO_URL + "/")
        return self

    def login(self, username: str, password: str = config.SAUCE_PASSWORD) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()

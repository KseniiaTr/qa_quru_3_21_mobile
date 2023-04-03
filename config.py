from typing import Literal, Optional

import pydantic
from appium.options.android import UiAutomator2Options

import utils2.file

EnvContext = Literal['emulation', 'real', 'browser']


class Settings(pydantic.BaseSettings):
    context: EnvContext = 'browser'

    # --- Appium Capabilities ---
    platformName: str = None
    platformVersion: str = None
    deviceName: str = None
    app: Optional[str] = None
    appName: Optional[str] = None
    appWaitActivity: Optional[str] = None
    newCommandTimeout: Optional[int] = 60

    # --- > BrowserStack Capabilities ---
    projectName: Optional[str] = None
    buildName: Optional[str] = None
    sessionName: Optional[str] = None
    # --- > > BrowserStack credentials---
    userLogin: Optional[str] = None
    accessKey: Optional[str] = None
    udid: Optional[str] = None

    # --- Remote Driver ---
    remote_url: str = 'http://127.0.0.1:4723/wd/hub'  # it's a default appium server url

    # --- Selene ---
    timeout: float = 6.0

    @property
    def run_on_browserstack(self):
        if self.context == 'browser':
            return 'hub.browserstack.com' in self.remote_url
        return False

    @property
    def driver_options(self):
        options = UiAutomator2Options()
        if self.deviceName:
            options.device_name = self.deviceName
        if self.platformName:
            options.platform_name = self.platformName

        options.app = (
            utils2.file.path_to_apk(self.app)
            if self.app and (self.app.startswith('./') or self.app.startswith('../'))
            else self.app
        )
        options.new_command_timeout = self.newCommandTimeout
        if self.udid:
            options.udid = self.udid
            options.ignore_hidden_api_policy_error = True
        if self.appWaitActivity:
            options.app_wait_activity = self.appWaitActivity
        if self.run_on_browserstack:
            options.load_capabilities(
                {
                    'platformVersion': self.platformVersion,
                    'bstack:options': {
                        'projectName': self.projectName,
                        'buildName': self.buildName,
                        'sessionName': self.sessionName,
                        'userName': self.userLogin,
                        'accessKey': self.accessKey,
                    },
                }
            )

        return options

    @classmethod
    def in_context(cls, env: Optional[EnvContext] = None) -> 'Settings':
        """
        factory method to init Settings with values from corresponding .env file
        """
        asked_or_current = env or cls().context
        return cls(
            _env_file=utils2.file.path_to_apk(f'config.{asked_or_current}.env')
        )


settings = Settings.in_context()
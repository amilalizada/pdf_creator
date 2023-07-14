from pydantic import BaseSettings
from fastapi_jwt_auth import AuthJWT

class AppSettings(BaseSettings):
    app_title: str = "PDF Creator API"
    app_description: str = "API for PDF creating"
    api_version: str = "v1"
    api_prefix = "/v1"
    env_url: str = ""
    app_env: str = "development"
    db_name: str = "jl_pdf_db"
    db_password: str = "12345"
    db_user: str = "root"
    db_port: int = 3309
    # authjwt_secret_key: str = "secret"
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    class Config:
        env_file = ".env"

    def __init__(self):
        super().__init__()
        # self.check_env()
        # if self.app_env != "production":
        #     self.set_env()
        return super().__init__()

    # @staticmethod
    # def check_env():
    #     if "APP_ENV" not in os.environ:
    #         raise SettingsError("'APP_ENV' environment variable is not defined")
    #     elif "ENV_HOST" not in os.environ:
    #         raise SettingsError("'ENV_HOST' environment variable is not defined")
    #     elif "ENV_TOKEN" not in os.environ:
    #         raise SettingsError("'ENV_TOKEN' environment variable is not defined")
    #     return None

    # def get_vault_data(self, url, token):
    #     """Gets data from vault"""

    #     if not url and token:
    #         error_msg = "Url or Host not found"
    #         SlackMessageSender.send(
    #             error_msg,
    #             self.app_title,
    #             self.error_slack_url,
    #         )
    #         raise SettingsError(error_msg)
    #     response = requests.get(url, headers={"X-Vault-Token": token})
    #     if response.status_code != 200:
    #         error_msg = f"Credentials not found wrong status code {url} {token}"
    #         SlackMessageSender.send(
    #             error_msg,
    #             self.app_title,
    #             self.error_slack_url,
    #         )
    #         raise SettingsError(error_msg)
    #     SlackMessageSender.send(
    #         "Credentials fetched from vault successfully",
    #         self.app_title,
    #         self.error_slack_url,
    #     )

    #     return json.loads(response.content)["data"]["data"]

    # def set_env(self):
    #     """Creates or updates .env file"""
    #     # app_url = os.getenv("ENV_URL", self.env_url)
    #     env_host = os.getenv("ENV_HOST", self.env_host)
    #     token = os.getenv("ENV_TOKEN", self.env_token)
    #     prefix = "v1/configs/data"
    #     try:
    #         partner_data = self.get_vault_data(f"{env_host}{prefix}/partners", token)
    #         api_data = self.get_vault_data(f"{env_host}{prefix}/api_conf", token)
    #         open(".env", "w").close()
    #         for k, v in api_data.items():
    #             with open(".env", mode="a+", encoding="utf-8") as f:
    #                 v = json.dumps(v) if isinstance(v, dict) else v
    #                 f.write(f"{k}={v}\n")
    #         with open(".env", mode="a+", encoding="utf-8") as f:
    #             f.write(
    #                 f"partners={json.dumps(partner_data)}\n"
    #                 f"api_data={json.dumps(api_data)}\n"
    #             )
    #     except Exception as e:
    #         error_msg = f"Error occurred when creating env file: {e}"
    #         SlackMessageSender.send(
    #             error_msg,
    #             self.app_title,
    #             self.error_slack_url,
    #         )

    #         logger.error(error_msg)
    #         raise SettingsError(f"Credentials not found wrong status code {e}")
    #     SlackMessageSender.send(
    #         "Env file .",
    #         self.app_title,
    #         self.error_slack_url,
    #     )

    #     return None


def get_app_settings() -> AppSettings:
    return AppSettings()


settings = get_app_settings()

# fastapi-jwt-auth conf load
def get_config():
    # settings.authjwt_secret_key = settings.app.auth_token
    return settings

# @AuthJWT.load_config
# def get_config():
#     return AppSettings()

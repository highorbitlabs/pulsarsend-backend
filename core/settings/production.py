from core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    title: str = "Vaultz API Prod app"

    class Config(AppSettings.Config):
        env_file = ".env"

"""
Implements the configuration pydantic model
"""
import pydantic


# pylint: disable=too-few-public-methods
class Settings(pydantic.BaseSettings):
    """
    Class for settings, which can be set via environment variables
    """
    class Config(pydantic.BaseConfig):
        """Config class for pydantic"""
        env_file = 'configs/config.dev'
        secrets_dir = 'secrets'

    scan_directory: str = "D:\\Benutzer\\mstuebner\\Eigene Dateien\\ScanSnap"
    output_path: str = "D:\\Benutzer\\mstuebner\\Eigene Dateien\\ScanSnap\\Ev-Autoimport\\matthias"
    timeout: int = 5
    filepattern = ["*.pdf"]


settings = Settings()

# GiG

from pathlib import Path
from pydantic import BaseModel, ConfigDict
from digio.utils import utils


class DatabaseConfigs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    db_file_path: Path
    db_prefix: str

    def get_db_url(self) -> str:
        return f"{self.db_prefix}{self.db_file_path.absolute()}"


class GlobalConfigs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    db_configs: DatabaseConfigs

    @staticmethod
    def load_from_path(file_path: Path) -> "GlobalConfigs":
        data = utils.load_toml(file_path)
        configs = GlobalConfigs.model_validate(data)
        return configs

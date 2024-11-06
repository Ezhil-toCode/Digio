################################
from pathlib import Path

import uvicorn
from loguru import logger

from digio.models.config_models import GlobalConfigs
from digio.web_services.web_server import app


################################


def start_uvicorn():
    port_no = 8000
    # change to warning during prod
    log_level = "debug"  # "warning"
    # log_level='warning' prevents logging of all normal requests
    uvicorn.run(app, host="127.0.0.1", port=port_no, log_level=log_level)


def setup_db():
    from digio.models.db_engine import initialize_dbs

    gc = GlobalConfigs.load_from_path(Path("implementation/demo/configs.toml"))
    initialize_dbs(gc.db_configs)
    # configure_logging_client(gc.logging_configs, logger)


if __name__ == "__main__":
    setup_db()
    start_uvicorn()
    logger.debug("engine started")

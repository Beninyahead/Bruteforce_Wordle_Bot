from .configs import log_config

from dotenv import load_dotenv

log_config.set_up_logging()

load_dotenv()

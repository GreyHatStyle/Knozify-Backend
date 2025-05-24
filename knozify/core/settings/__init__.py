from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include, optional

# INITIALIZING ENVIRONMENT VARIABLES
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(
    __file__).resolve().parent.parent.parent  # Getting the right path

include(
    'base.py',
    'custom.py',
    'databases.py',
    'drf_conf.py',
    'logging.py',
    'redis.py',
    'simple_jwt.py',
    'sentry.py',
    'social_auths.py',
)

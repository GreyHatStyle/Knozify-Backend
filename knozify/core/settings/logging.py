import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Ensure logs directory exists
LOGS_DIR = PROJECT_ROOT / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # "file": {
        #     "class":
        #     "logging.FileHandler",
        #     "filename":
        #     str(LOGS_DIR / os.environ.get('DJANGO_LOG_FILE', 'django.log')),
        #     "level":
        #     os.environ.get('DJANGO_LOG_LEVEL'),
        #     "formatter":
        #     "verbose",
        # },
        'logtail': {
            'class': 'logtail.LogtailHandler',
            'source_token': os.environ.get("BETTERSTACK_SOURCE_TOKEN"),
            'host': os.environ.get("BETERSTACK_INGESTING_HOST"),
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": os.environ.get('DJANGO_LOG_LEVEL'),
            "formatter": "simple",
        },
    },
    "loggers": {
        "account": {
            "level": os.environ.get('DJANGO_LOG_LEVEL'),
            "handlers": ["console", "logtail"],
        },
    },
    "formatters": {
        "simple": {
            "format": "{levelname} [{asctime}]: {message}",
            "style": "{",
        },
        "verbose": {
            "format":
            "{levelname}[{asctime}] - ({name} -> {module}.py line={lineno:d}): {message}",
            "style": "{",
        }
    }
}

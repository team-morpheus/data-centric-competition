import os
import sys
from datetime import datetime

import common.logger_config  # noqa: used to initialize the logger

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
PROJECT_NAME = "dc_comp"
USER_ROOT_DIR = os.path.dirname(os.path.dirname(PROJECT_ROOT))

# consistent for all projects
LONG_TERM_DIR = "/media/yonatanz/yz/"
LONG_TERM_DIR = LONG_TERM_DIR if os.path.exists(LONG_TERM_DIR) else "/cortex/users/jonzarecki/long_term/"

PROJ_LONG_TERM_DIR = os.path.join(LONG_TERM_DIR, PROJECT_NAME)
DATA_LONG_TERM_DIR = os.path.join(LONG_TERM_DIR, "data")
MODEL_LONG_TERM_DIR = os.path.join(LONG_TERM_DIR, "models")

_curr_time = datetime.now().isoformat(" ", "seconds")

TENSORBOARD_DIR = os.path.join(PROJ_LONG_TERM_DIR, "logs")
STATE_DIR = os.path.join(PROJ_LONG_TERM_DIR, "expr_state")
PROJ_MODELS_LONG_TERM_DIR = os.path.join(PROJ_LONG_TERM_DIR, "models")

CURRENT_RUN_DIR = os.path.join(PROJ_LONG_TERM_DIR, os.path.basename(sys.argv[0]), _curr_time)
SAVED_MODEL_DIR = os.path.join(CURRENT_RUN_DIR, "models")
TMP_EXPR_FILES_DIR = os.path.join(CURRENT_RUN_DIR, "project_files")

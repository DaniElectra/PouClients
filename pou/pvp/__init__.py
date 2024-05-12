# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.pvp.host import PvPHost
from pou.pvp import settings

import logging

logging.basicConfig(format = settings.get_setting("log_format"))

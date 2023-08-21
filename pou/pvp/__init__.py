# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.pvp.host import PvPHost
from pou.pvp import settings

import logging

logging.basicConfig(format = settings.get_setting("log_format"))

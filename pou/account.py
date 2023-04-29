# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.site import VersionInfo
from pou.user import BasicUserInfo

import json

class BasicAccountInfo(BasicUserInfo):
	"""Stores the basic private user information about the specified account.
	This class does not store the game save.

	Attributes:
	hP -- unknown argument
	account_id -- the account ID
	nickname -- the account nickname
	favorites_count -- the number of favorites the account has
	likers_count -- the number of likers the account has
	t -- unknown argument
	"""

	def __init__(self):
		super().__init__()

		self.hP = False
		self.favorites_count = 0
		self.t = ""

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		super().from_response(response)

		self.hP = response["hP"]
		self.favorites_count = int(response["nF"])
		self.t = response["t"]

class AccountInfo(BasicAccountInfo):
	"""Provides the full private user information about the account the client is logged into.

	Attributes:
	email -- the account email address
	hP -- unknown argument
	account_id -- the account ID
	l -- unknown argument
	nickname -- the account nickname
	favorites_count -- the number of favorites the account has
	likers_count -- the number of likers the account has
	t -- unknown argument
	"""

	def __init__(self):
		super().__init__()

		self.email = ""
		self.l = 0

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		super().from_response(response)

		self.email = response["e"]
		self.l = int(response["l"])

class AccountData(BasicAccountInfo):
	"""Contains the basic user information of a specified account. This class
	also has the game save data of the account, with its version and
	revision.

	Attributes:
	hP -- unknown argument
	account_id -- the account ID
	nickname -- the account nickname
	favorites_count -- the number of favorites the account has
	likers_count -- the number of likers the account has
	t -- unknown argument
	version_info -- the save data version and revision
	save_state -- the gave save data
	"""

	def __init__(self):
		super().__init__()

		self.version_info = VersionInfo()
		self.save_state = {}

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		super().from_response(response)

		self.version_info = VersionInfo()
		self.version_info.from_response(response)

		self.save_state = json.loads(response["state"])

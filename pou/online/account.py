# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

import json

class AccountInfo:
	"""Provides the full private user information about the account the
	client is logged into.

	Attributes:
	account_id -- the account ID
	email -- the account email address
	has_password -- if the account has a password set
	nickname -- the account nickname
	t -- unknown argument
	l -- unknown argument
	favorites_count -- the number of favorites the account has
	likers_count -- the number of likers the account has
	"""

	def __init__(self):
		self.account_id = 0
		self.email = ""
		self.has_password = False
		self.nickname = ""
		self.t = ""
		self.l = 0
		self.favorites_count = 0
		self.likers_count = 0

	@staticmethod
	def from_response(response: dict):
		"""Fills the attributes of this class from a server response."""

		account_info = AccountInfo()
		account_info.account_id = int(response["i"])
		account_info.email = response["e"]
		account_info.has_password = response["hP"]
		account_info.nickname = response["n"]
		account_info.t = response["t"]
		account_info.l = int(response["l"])
		account_info.favorites_count = int(response["nF"])
		account_info.likers_count = int(response["nL"])

		return account_info

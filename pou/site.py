# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

class Captcha:
	"""Stores all the information about the server captcha upon registering a
	new account.

	Attributes:
	captcha_id -- the captcha ID
	captcha_length -- the number of characters of the captcha
	captcha_img -- the captcha stored as a base64 PNG
	"""

	def __init__(self):
		self.captcha_id = ""
		self.captcha_length = 0
		self.captcha_img = ""

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		self.captcha_id = response["capId"]
		self.captcha_length = response["capLen"]
		self.captcha_img = response["capImg"]

class RegistrationInfo:
	"""Contains the basic user information of a newly registered account.

	Attributes:
	nickname -- the user nickname
	account_id -- the account ID
	n -- same as nickname
	"""
	def __init__(self):
		self.nickname = ""
		self.account_id = 0
		self.n = ""

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		self.nickname = response["nickname"]
		self.account_id = response["i"]
		self.n = response["n"]

class VersionInfo:
	"""Stores the version of the game save data stored on the servers. This version
	is updated with the client, and newer clients are backwards compatible
	with older revisions of saves.

	Attributes:
	version -- the save data version
	revision -- the save data revision
	"""

	def __init__(self):
		self.version = 0
		self.revision = 0

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		self.version = response["version"]
		self.revision = response["revision"]

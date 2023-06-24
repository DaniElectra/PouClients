# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

import json

class UserScoreInfo:
	"""Holds information about the user's relationship with the client's
	account and the score it has on a certain game.

	Attributes:
	account_id -- the account ID of the user
	nickname -- the user nickname
	min_info -- the information about the Pou of the user
	l -- unknown argument
	likers_count -- the number of likers the user has
	score -- the score of the user
	i_like -- if the account of the client likes this user
	likes_me -- if the user likes the client's account
	"""
	def __init__(self):
		self.account_id = 0
		self.nickname = ""
		self.min_info = {}
		self.l = 0
		self.likers_count = 0
		self.i_like = False
		self.likes_me = False
		self.score = 0

	@staticmethod
	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		user_score_info = UserScoreInfo()
		user_score_info.account_id = int(response["i"])
		user_score_info.nickname = response["n"]
		user_score_info.min_info = json.loads(response["minI"])
		user_score_info.l = int(response["l"])
		user_score_info.likers_count = int(response["nL"])
		user_score_info.score = int(response["s"])

		# "i_like" and "likes_me" don't appear if we're not logged in
		if "iL" in response:
			user_score_info.i_like = bool(response["iL"])

		if "lM" in response:
			user_score_info.likes_me = bool(response["lM"])

		return user_info

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

	@staticmethod
	def from_response(response: dict):
		"""Fills the attributes of this class from a server response."""

		captcha = Captcha()
		captcha.captcha_id = response["capId"]
		captcha.captcha_length = response["capLen"]
		captcha.captcha_img = response["capImg"]

		return captcha

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

	@staticmethod
	def from_response(response: dict):
		"""Fills the attributes of this class from a server response."""

		registration_info = RegistrationInfo()
		registration_info.nickname = response["nickname"]
		registration_info.account_id = response["i"]
		registration_info.n = response["n"]

		return registration_info

class UserLogin:
	"""Contains the user information provided by the server when logging into
	an account.

	Attributes:
	account_id -- the account ID
	nickname -- the account nickname
	t -- unknown argument
	hP -- unknown argument
	favorites_count -- the number of favorites the account has
	likers_count -- the number of likers the account has
	save_state -- the gave save data
	version -- the save data version
	revision -- the save data revision
	"""

	def __init__(self):
		self.account_id = 0
		self.nickname = ""
		self.t = ""
		self.hP = False
		self.favorites_count = 0
		self.likers_count = 0
		self.save_state = {}
		self.version = 0
		self.revision = 0

	@staticmethod
	def from_response(response: dict):
		"""Fills the attributes of this class from a server response."""

		user_login = UserLogin()
		user_login.account_id = response["i"]
		user_login.nickname = response["n"]
		user_login.t = response["t"]
		user_login.hP = response["hP"]
		user_login.favorites_count = int(response["nF"])
		user_login.likers_count = int(response["nL"])
		user_login.save_state = json.loads(response["state"])
		user_login.version = response["version"]
		user_login.revision = response["revision"]

		return user_login

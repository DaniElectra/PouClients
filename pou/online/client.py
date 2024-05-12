# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.online import account, request, site, user

import hashlib, json
import requests

class PouClient:
	"""Pou client that connects to the game server.

	Attributes:
	api -- an indicator to access the API, should not be changed
	c -- unknown argument sent to server
	version -- the client version
	revision -- the client revision
	host -- the server host
	session -- the session for handling the requests
	"""
	def __init__(self):
		self.api = 1
		self.c = 1
		self.version = 4
		self.revision = 263
		self.host = "http://app.pou.me"
		self.session = requests.Session()

		self.session.cookies.set("unn_session", None)

	@staticmethod
	def from_version(api: int, c: int, version: int, revision: int):
		"""Creates a new PouClient using the provided client version and the
		common parameters of the server.
		"""
		client = PouClient()
		client.api = api
		client.c = c
		client.version = version
		client.revision = revision

		return client

# ---------------------
# --- Site endpoint ---
# ---------------------

	async def check_email(self, email: str):
		"""Checks if a provided email address is registered inside the server.
		Returns a Captcha for registration if the email is not registered, and
		None if it is.
		"""
		params = { "e": email }
		response = request.pou_request(self, "/ajax/site/check_email", "POST", params)

		if not response["registered"]:
			captcha = site.Captcha.from_response(response)
			return captcha

	async def top_likes(self):
		"""Gets the 20 most liked users on the Pou game server. Returns an
		array showing the information of each user.
		"""

		response = request.pou_request(self, "/ajax/site/top_likes", "GET")

		if response["ok"]:
			user_list = []

			for pou_user in response["items"]:
				user_info = user.UserInfo.from_response(pou_user)
				user_list.append(user_info)

			return user_list

	async def register(self, email: str, captcha_id: str, captcha_answer: str):
		"""Tries to register an account with the given email address using the
		provided answer to the captcha. Returns an RegistrationInfo with the
		registered user information if it succeeds.

		If the captcha is wrong, the function returns a new Captcha for
		retrying the registration.
		"""

		params = { "e": email, "cI": captcha_id, "cA": captcha_answer }
		response = request.pou_request(self, "/ajax/site/register", "POST", params)

		if "error" in response:
			if response["error"]["type"] == "ICap":
				captcha = site.Captcha.from_response(response)
				return captcha

		if response["success"]:
			registration_info = site.RegistrationInfo.from_response(response)
			return registration_info

	async def top_scores(self, game_id: int, period: str):
		"""Gets the ranking of the 20 users with the highest score on a selected
		game during a period of time.

		The period can be represented as "today", "week", "month" or
		"alltime".

		Returns an array showing the score information of each user.
		"""

		params = { "g": game_id, "d": period }
		response = request.pou_request(self, "/ajax/site/top_scores", "GET")

		if response["ok"]:
			user_list = []

			for pou_user in response["items"]:
				user_info = site.UserScoreInfo.from_response(pou_user)
				user_list.append(user_info)

			return user_list

	async def login(self, email: str, password: str):
		"""Tries to login to Pou game servers with the specified account. If the
		login succeeds, returns a UserLogin class with the details of the
		account, and returns None if it fails.
		"""

		# The server requires the password to be sent as an MD5 hash
		p = hashlib.md5(password.encode("utf-8")).hexdigest()

		params = {"e": email, "p": p}
		response = request.pou_request(self, "/ajax/site/login", "POST", params)

		if response["success"]:
			user_login = site.UserLogin.from_response(response)
			return user_login

# ------------------------
# --- Account endpoint ---
# ------------------------

	async def save(self, save_state: dict, min_info: dict):
		"""Saves the Pou, game state and online scores to the server. Returns a
		bool telling if the save succeeds.
		"""

		payload = {"minInfo": json.dumps(min_info), "state": json.dumps(save_state)}

		str_payload = json.dumps(payload)
		cookies = self.session.cookies.get_dict()
		unn_session = cookies["unn_session"]

		# c = MD5("p@v_" + str_payload + unn_session)
		confirmation = "p@v_" + str_payload + unn_session
		c = hashlib.md5(confirmation.encode("utf-8")).hexdigest()

		params = {"c": c}
		response = request.pou_request(self, "/ajax/account/save", "POST", params, payload)

		return response["success"]

	async def logout(self):
		"""Logs off the server if the session is logged in to an account. Returns
		a bool telling if the logout succeeds.
		"""

		response = request.pou_request(self, "/ajax/account/logout", "POST")

		return response["success"]

	async def delete(self):
		"""Deletes the account of the client from the server. All information
		relating the account will be deleted. Returns a bool telling if the
		deletion succeeds.
		"""
		cookies = self.session.cookies.get_dict()
		unn_session = cookies["unn_session"]

		# c = MD5("p@v_" +  unn_session)
		confirmation = "p@v_" +  unn_session
		c = hashlib.md5(confirmation.encode("utf-8")).hexdigest()

		params = {"c": c}
		response = request.pou_request(self, "/ajax/account/delete", "POST", params)

		return response["success"]

	async def account_info(self):
		"""Gets the full private information about the account the client is logged
		into. Returns an AccountInfo with the account information.
		"""

		response = request.pou_request(self, "/ajax/account/info", "GET")

		if response["ok"]:
			account_info = account.AccountInfo.from_response(response)
			return account_info

	async def check_password(self, password: str):
		"""Checks if the password given matches with the password of the client's
		account. Returns a bool telling if the password is correct.
		"""

		# The server requires the password to be sent as an MD5 hash
		p = hashlib.md5(password.encode("utf-8")).hexdigest()

		params = {"p": p}
		response = request.pou_request(self, "/ajax/account/check_password", "POST", params)

		return response["ok"]

# ---------------------
# --- User endpoint ---
# ---------------------

	async def favorites(self, account_id: int, since: int = 0):
		"""Gets the accounts that a user has liked before a specified timestamp.
		Returns a UserList showing the information of each account, and a next
		argument if the list has 20 or more users.
		"""

		params = { "id": account_id, "s": since }
		response = request.pou_request(self, "/ajax/user/favorites", "GET", params)

		if response["ok"]:
			user_list = user.UserList.from_response(response)
			return user_list

	async def likers(self, account_id: int, since: int = 0):
		"""Gets the accounts that have liked a user before a specified timestamp.
		Returns a UserList showing the information of each account, and a next
		argument if the list has 20 or more users.
		"""

		params = { "id": account_id, "s": since }
		response = request.pou_request(self, "/ajax/user/likers", "GET", params)

		if response["ok"]:
			user_list = user.UserList.from_response(response)
			return user_list

	async def visitors(self, account_id: int, since: int = 0):
		"""Gets the accounts that have visited a user before a specified timestamp.
		Returns a UserVisitors showing the information of each account, and a
		next argument if the list has 20 or more users.
		"""

		params = { "id": account_id, "s": since }
		response = request.pou_request(self, "/ajax/user/visitors", "GET", params)

		if response["ok"]:
			user_list = user.UserVisitors.from_response(response)
			return user_list

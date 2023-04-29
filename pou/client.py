# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou import account, request, site, user

import hashlib, json
import requests

class PouClient:
	"""Pou client that connects to the game server.

	Attributes:
	a -- unknown argument sent to server
	c -- unknown argument sent to server
	version -- the client version
	revision -- the client revision
	host -- the server host
	session -- the session for handling the requests
	"""
	def __init__(self):
		self.a = 1
		self.c = 1
		self.version = 4
		self.revision = 256
		self.host = "http://app.pou.me"
		self.session = requests.Session()

		self.session.cookies.set("unn_session", None)

	@staticmethod
	def from_version(a: int, c: int, version: int, revision: int):
		"""Creates a new PouClient using the provided client version and the
		common parameters of the server.
		"""
		client = PouClient()
		client.a = a
		client.c = c
		client.version = version
		client.revision = revision

		return client

	async def check_email(self, email: str):
		"""Checks if a provided email address is registered inside the server.
		Returns a Captcha for registration if the email is not registered, and
		None if it is.
		"""
		params = { "e": email }
		response = request.pou_request(self, "/ajax/site/check_email", "POST", params)

		if not response["registered"]:
			captcha = site.Captcha()
			captcha.from_response(response)
			return captcha

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
				captcha = site.Captcha()
				captcha.from_response(response)
				return captcha

		if response["success"]:
			registration_info = site.RegistrationInfo()
			registration_info.from_response(response)
			return registration_info

	async def login(self, email: str, password: str):
		"""Tries to login to Pou game servers with the specified account. If the
		login succeeds, returns an AccountData with the details of the
		account, and returns None if it fails.
		"""

		# The server requires the password to be sent as an MD5 hash
		p = hashlib.md5(password.encode("utf-8")).hexdigest()

		params = {"e": email, "p": p}
		response = request.pou_request(self, "/ajax/site/login", "POST", params)

		if response["success"]:
			account_data = account.AccountData()
			account_data.from_response(response)
			return account_data

	async def logout(self):
		"""Logs off the server if the session is logged in to an account. Returns
		a bool telling if the logout succeeds or not.
		"""

		response = request.pou_request(self, "/ajax/account/logout", "POST")

		return response["success"]

	async def account_info(self):
		"""Gets the full private information about the account the client is logged
		into. Returns an AccountInfo with the account information.
		"""

		response = request.pou_request(self, "/ajax/account/info", "GET")

		if response["ok"]:
			account_info = account.AccountInfo()
			account_info.from_response(response)
			return account_info

	async def favorites(self, account_id: int, since: int = 0):
		"""Gets the accounts that a user has liked before a specified timestamp.
		Returns a UserList showing the information of each account, and a next
		argument if the list has 20 or more users.
		"""

		params = { "id": account_id, "s": since }
		response = request.pou_request(self, "/ajax/user/favorites", "GET", params)

		if response["ok"]:
			user_list = user.UserList()
			user_list.from_response(response)
			return user_list

	async def likers(self, account_id: int, since: int = 0):
		"""Gets the accounts that have liked a user before a specified timestamp.
		Returns a UserList showing the information of each account, and a next
		argument if the list has 20 or more users.
		"""

		params = { "id": account_id, "s": since }
		response = request.pou_request(self, "/ajax/user/likers", "GET", params)

		if response["ok"]:
			user_list = user.UserList()
			user_list.from_response(response)
			return user_list

	async def top_likes(self):
		"""Gets the 20 most liked users on the Pou game server. Returns a
		UserList showing the information of each user.
		"""

		response = request.pou_request(self, "/ajax/site/top_likes", "GET")

		if response["ok"]:
			user_list = user.UserList()
			user_list.from_response(response)
			return user_list

	async def save(self, save_state: dict, min_info: dict):
		"""Saves the Pou, game state and online scores to the server. Returns a
		bool telling if the save succeeds or not.
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

	async def delete(self):
		"""Deletes the account of the client from the server. All information
		relating the account will be deleted. Returns a bool telling if the
		deletion succeeds or not.
		"""
		cookies = self.session.cookies.get_dict()
		unn_session = cookies["unn_session"]

		# c = MD5("p@v_" +  unn_session)
		confirmation = "p@v_" +  unn_session
		c = hashlib.md5(confirmation.encode("utf-8")).hexdigest()

		params = {"c": c}
		response = request.pou_request(self, "/ajax/account/delete", "POST", params)

		return response["success"]



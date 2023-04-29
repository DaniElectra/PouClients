# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

import json

class BasicUserInfo:
	"""Stores the basic public user information about an account. This class
	does not store the game save of the user.

	Attributes:
	account_id -- the account ID of the user
	nickname -- the user nickname
	likers_count -- the number of likers the user has
	"""
	def __init__(self):
		self.account_id = 0
		self.nickname = ""
		self.likers_count = 0

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		self.account_id = int(response["i"])
		self.nickname = response["n"]
		self.likers_count = int(response["nL"])

class UserInfo(BasicUserInfo):
	"""Contains the public user information about an account and the
	relationship with the client's account.

	Attributes:
	account_id -- the account ID of the user
	i_like -- if the account of the client likes this user
	l -- unknown argument
	likes_me -- if the user likes the client's account
	nickname -- the user nickname
	min_info -- the information about the Pou of the user
	likers_count -- the number of likers the user has
	"""

	def __init__(self):
		super().__init__()

		self.i_like = False
		self.l = 0
		self.likes_me = False
		self.min_info = {}

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		super().from_response(response)

		# "i_like" and "likes_me" don't appear if we're not logged in
		if "iL" in response:
			self.i_like = bool(response["iL"])

		if "lM" in response:
			self.likes_me = bool(response["lM"])

		self.l = int(response["l"])

		if response["minI"] != "":
			self.min_info = json.loads(response["minI"])

class UserList:
	"""Provides a list of users which belong to the likers or favorites of
	the client's account or another user.
	The list is ordered by the date when the action was taken, and if it
	goes to 20 or more, a "next" argument is provided to go to the next
	part.

	Attributes:
	count -- the total number of users
	items -- the list of users
	next -- a Unix timestamp to show the older entries
	"""

	def __init__(self):
		self.count = 0
		self.items = []
		self.next = 0

	def from_response(self, response: dict):
		"""Fills the attributes of this class from a server response."""

		# The "top_likes" ranking doesn't have a count value
		if "count" in response:
			self.count = response["count"]

		for user in response["items"]:
			user_info = UserInfo()
			user_info.from_response(user)
			self.items.append(user_info)

		if "next" in response:
			self.next = response["next"]

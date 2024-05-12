# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.online import common

import json

class UserInfo:
	"""Holds information about the user's relationship with the client's
	account and the number of likes it has.

	Attributes:
	account_id -- the account ID of the user
	nickname -- the user nickname
	min_info -- the information about the Pou of the user
	l -- unknown argument
	likers_count -- the number of likers the user has
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

	@staticmethod
	def from_response(response: dict):
		"""Fills the attributes of this class from a server response."""

		user_info = UserInfo()
		user_info.account_id = int(response["i"])
		user_info.nickname = response["n"]

		if response["minI"]:
			user_info.min_info = common.PouMinInfo.from_response(json.loads(response["minI"]))

		user_info.l = int(response["l"])
		user_info.likers_count = int(response["nL"])

		# "i_like" and "likes_me" don't appear if we're not logged in
		if "iL" in response:
			user_info.i_like = bool(response["iL"])

		if "lM" in response:
			user_info.likes_me = bool(response["lM"])

		return user_info

class UserList:
	"""Provides a list of users which belong to the likers or favorites of
	the client's account or another user.
	The list is ordered by the date when the action was taken, and if it
	goes to 20 or more, a "next" argument is provided to go to the next
	part.

	Attributes:
	items -- the list of users
	next -- a Unix timestamp to show the older entries
	count -- the total number of users
	"""

	def __init__(self):
		self.count = 0
		self.items = []
		self.next = 0

	@staticmethod
	def from_response(response: dict):
		"""Fills the attributes of this class from a server response."""

		user_list = UserList()

		for user in response["items"]:
			user_info = UserInfo.from_response(user)
			user_list.items.append(user_info)

		if "next" in response:
			user_list.next = int(response["next"])

		user_list.count = int(response["count"])

		return user_list

class UserVisitors:
	"""Provides a list of users which have been visitors of the client's
	account or another user.
	The list is ordered by the date when the action was taken, and if it
	goes to 20 or more, a "next" argument is provided to go to the next
	part.

	Attributes:
	items -- the list of users
	next -- a Unix timestamp to show the older entries
	"""

	def __init__(self):
		self.items = []
		self.next = 0

	@staticmethod
	def from_response(response: dict):
		"""Fills the attributes of this class from a server response."""

		user_list = UserVisitors()

		for user in response["items"]:
			user_info = UserInfo.from_response(user)
			user_list.items.append(user_info)

		if "next" in response:
			user_list.next = int(response["next"])

		return user_list

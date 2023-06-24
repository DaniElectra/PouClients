# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

class ClientOutdated(Exception):
	"""Expection raised when the client is too old than the minimum required
	by the server. This is determined by the version and revision values
	provided to the server on each request.

	Attributes:
	message -- the error message of the server
	diff_client -- unknown argument provided by the server
	"""

	def __init__(self, message: str, diff_client: bool):
		self.message = message
		self.diff_client = diff_client

class EmailAlreadyRegistered(Exception):
	"""Exception raised when trying to register a new account with an email
	address that is being used by an existing account on the server.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class EmailNotRegistered(Exception):
	"""Exception raised when trying to login with an email address that is
	not registered on the server.

	Attributes:
	message -- the error message of the server
	email -- the email address that was used to login
	"""

	def __init__(self, message: str, email: str):
		self.message = message
		self.email = email

class FeatureMaintenance(Exception):
	"""Raised if the feature requested by the client isn't available for
	maintenance reasons.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class IncorrectPassword(Exception):
	"""Exception raised if the user provides an invalid password.
	This means that the original password provided when trying to change
	the password of the account is incorrect.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class IncorrectUserCredentials(Exception):
	"""Exception raised if the user provides invalid credentials when trying
	to log into the server.
	This means that the password provided by the client is incorrect.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class InvalidArgumentFormat(Exception):
	"""Exception raised when the user tries to set a nickname that doesn't
	comply with the server requirements.

	Attributes:
	message -- the error message of the server
	argument -- a set which states the name of the invalid argument
	"""

	def __init__(self, message: str, argument: dict):
		self.message = message
		self.argument = argument

class InvalidRequest(Exception):
	"""Raised if the request path is invalid.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class NicknameNotAvailable(Exception):
	"""Raised if the nickname that a user tried to use is taken and not
	available.

	Attributes:
	message -- the error message of the server
	nickname -- the nickname that has been used
	"""

	def __init__(self, message: str, nickname: str):
		self.message = message
		self.nickname = nickname

class NotYourTurn(Exception):
	"""Raised if the client has tried to update a game session when the
	opponent has the turn on the game.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class ObjectNotFound(Exception):
	"""Exception raised when a query of an object failed.

	Attributes:
	message -- the error message of the server
	resource -- a set providing the type of the query and its value
	"""

	def __init__(self, message: str, resource: dict):
		self.message = message
		self.resource = resource

class PermissionDenied(Exception):
	"""Raised if the client tries to access a resource or perform a request
	that requires permissions that the client doesn't have.
	This can happen if a client tries to view a game where other
	participants are playing.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class SiteOffline(Exception):
	"""Raised if the server is currently undergoing maintenance.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class TooManyRegisterAttempts(Exception):
	"""Exception raised when the client tries to register a new account, but
	fails the captcha too many times.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class TooManySocialActions(Exception):
	"""Raised if the user has performed too many requests to the server on a
	single day.
	The main server limit is of 5000 requests.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class UserBanned(Exception):
	"""Exception raised if the user target of a request has been banned from
	the server.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class UserIsMe(Exception):
	"""Raised when trying to make a search about your own user the client is
	logged into.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

class UserNotLoggedIn(Exception):
	"""Raised if the user cookie of the request is missing or invalid.
	This can happen if you haven't made a login request to the server.

	Attributes:
	message -- the error message of the server
	"""

	def __init__(self, message: str):
		self.message = message

pou_errors = {
	"ClientOutdated": ClientOutdated,
	"EmailAlreadyRegistered": EmailAlreadyRegistered,
	"EmailNotRegistered": EmailNotRegistered,
	"FeatureMaintenance": FeatureMaintenance,
	"IncorrectPassword": IncorrectPassword,
	"IncorrectUserCredentials": IncorrectUserCredentials,
	"InvalidArgumentFormat": InvalidArgumentFormat,
	"InvalidRequest": InvalidRequest,
	"NicknameNotAvailable": NicknameNotAvailable,
	"NotYourTurn": NotYourTurn,
	"ObjectNotFound": ObjectNotFound,
	"PermissionDenied": PermissionDenied,
	"SiteOffline": SiteOffline,
	"TMR": TooManyRegisterAttempts,
	"TMSA": TooManySocialActions,
	"UserBanned": UserBanned,
	"UserIsMe": UserIsMe,
	"UserNotLoggedIn": UserNotLoggedIn
}

# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou import errors
import requests

def pou_request(client, path, method, params = None, payload = None):
	'''Makes a request to Pou game servers. Returns a dict unless the server
	returns an error, for which an Exception will be thrown.'''
	request_params = {
		"_a": client.a,
		"_c": client.c,
		"_v": client.version,
		"_r": client.revision
	}

	if params:
		request_params.update(params)

	url = client.host + path

	session = client.session

	response = session.request(method = method, url = url, params = request_params, json = payload)
	response = response.json()

	pou_errors = {
		"ClientOutdated": errors.ClientOutdated,
		"EmailAlreadyRegistered": errors.EmailAlreadyRegistered,
		"EmailNotRegistered": errors.EmailNotRegistered,
		"FeatureMaintenance": errors.FeatureMaintenance,
		"IncorrectPassword": errors.IncorrectPassword,
		"IncorrectUserCredentials": errors.IncorrectUserCredentials,
		"InvalidArgumentFormat": errors.InvalidArgumentFormat,
		"InvalidRequest": errors.InvalidRequest,
		"NicknameNotAvailable": errors.NicknameNotAvailable,
		"NotYourTurn": errors.NotYourTurn,
		"ObjectNotFound": errors.ObjectNotFound,
		"PermissionDenied": errors.PermissionDenied,
		"SiteOffline": errors.SiteOffline,
		"TMR": errors.TooManyRegisterAttempts,
		"TMSA": errors.TooManySocialActions,
		"UserBanned": errors.UserBanned,
		"UserIsMe": errors.UserIsMe,
		"UserNotLoggedIn": errors.UserNotLoggedIn
	}

	if "error" in response:
		error_type = response["error"]["type"]
		if error_type == "ClientOutdated":
			raise pou_errors[error_type](response["error"]["message"], response["error"]["diffClient"])
		elif error_type == "EmailNotRegistered":
			raise pou_errors[error_type](response["error"]["message"], response["error"]["email"])
		elif error_type == "InvalidArgumentFormat":
			raise pou_errors[error_type](response["error"]["message"], response["error"]["argument"])
		elif error_type == "NicknameNotAvailable":
			raise pou_errors[error_type](response["error"]["message"], response["error"]["nickname"])
		elif error_type == "ObjectNotFound":
			raise pou_errors[error_type](response["error"]["message"], response["error"]["resource"])
		elif error_type in pou_errors:
			raise pou_errors[error_type](response["error"]["message"])

	return response

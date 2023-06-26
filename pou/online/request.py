# SPDX-FileCopyrightText: 2023 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.online import errors
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

	if "error" in response:
		error_type = response["error"]["type"]
		if error_type == "ClientOutdated":
			raise errors.ClientOutdated(response["error"]["message"], response["error"]["diffClient"])
		elif error_type == "EmailNotRegistered":
			raise errors.EmailNotRegistered(response["error"]["message"], response["error"]["email"])
		elif error_type == "InvalidArgumentFormat":
			raise errors.InvalidArgumentFormat(response["error"]["message"], response["error"]["argument"])
		elif error_type == "NicknameNotAvailable":
			raise errors.NicknameNotAvailable(response["error"]["message"], response["error"]["nickname"])
		elif error_type == "ObjectNotFound":
			raise errors.ObjectNotFound(response["error"]["message"], response["error"]["resource"])
		elif error_type in errors.pou_errors:
			raise errors.pou_errors[error_type](response["error"]["message"])

	return response

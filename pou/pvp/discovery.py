# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.pvp import settings

import logging
import socketserver
import hashlib, json

class DiscoveryUDPProtocolHandler(socketserver.BaseRequestHandler):
	"""The UDP protocol handler used for Pou vs Pou discovery packets.

	Attributes:
	logger -- the logger used for logging the server status
	"""
	def setup(self):
		self.logger = logging.getLogger("Discovery host")

	def handle(self):
		packet_json = json.loads(self.request[0].strip())
		self.logger.debug("Received Pou vs Pou discovery packet")

		if "rN" in packet_json:
			self.logger.debug("Random number: " + str(packet_json["rN"]))
		else:
			self.logger.error("Missing random number!")
			return

		if "mC" in packet_json:
			self.logger.debug("Hash: " + packet_json["mC"])
		else:
			self.logger.error("Missing hash!")
			return

		if "gI" in packet_json:
			self.logger.debug("Game ID: " + str(packet_json["gI"]))
		else:
			self.logger.error("Missing game ID!")
			return

		game_id = settings.get_setting("server.game_id")
		if game_id != packet_json["gI"]:
			self.logger.info("Game ID mismatch: got %d, expected %d", packet_json["gI"], game_id)
			return

		discovery_validate = "p0v" + str(packet_json["rN"]) + "s"
		discovery_hash = hashlib.md5(discovery_validate.encode("utf-8")).hexdigest()

		if discovery_hash != packet_json["mC"]:
			self.logger.error("Hash doesn't match!")
			return

		reply_validate = "p0v" + str(packet_json["rN"]) + "m"
		reply_hash = hashlib.md5(reply_validate.encode("utf-8")).hexdigest()

		server_name = settings.get_setting("server.name")

		reply = {"n": server_name, "mC": reply_hash}
		reply_json = json.dumps(reply)

		response = bytes(reply_json, 'utf-8')

		socket = self.request[1]
		socket.sendto(response, self.client_address)

class DiscoveryUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
	"""The UDP server used for Pou vs Pou discovery."""
	pass

class DiscoveryServer:
	"""Pou server that allows discovery of Pou vs Pou sessions.

	Attributes:
	ip -- the IP used for the discovery server
	port -- the port used for the discovery server
	logger -- the logger used for the discovery server
	server -- the server used for discovery
	"""
	def __init__(self):
		self.ip = "0.0.0.0"
		self.port = 27110
		self.logger = logging.getLogger("Discovery host")

		self.server = None

	def start(self):
		"""Starts the Pou vs Pou discovery server."""
		self.server = DiscoveryUDPServer((self.ip, self.port), DiscoveryUDPProtocolHandler)
		with self.server:
			self.server.serve_forever()

	def shutdown(self):
		"""Shuts down the Pou vs Pou discovery server."""
		self.server.shutdown()


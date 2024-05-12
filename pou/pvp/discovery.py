# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.pvp import settings

import logging
import socket
import hashlib, json

class DiscoveryUDPServer():
	"""The UDP server used for Pou vs Pou discovery."""

	def __init__(self, address: tuple):
		self.logger = logging.getLogger("Discovery host")
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(address)
		self.socket.setblocking(False)
		self.stop = False

	def start(self):
		"""Starts the UDP discovery server."""
		try:
			while True:
				if self.stop:
					break
				try:
					request, client_address = self.socket.recvfrom(1024)
				except BlockingIOError:
					continue
				packet_json = json.loads(request.strip())
				self.logger.debug("Received Pou vs Pou discovery packet")

				if "rN" in packet_json:
					self.logger.debug("Random number: " + str(packet_json["rN"]))
				else:
					self.logger.error("Missing random number!")
					continue

				if "mC" in packet_json:
					self.logger.debug("Hash: " + packet_json["mC"])
				else:
					self.logger.error("Missing hash!")
					continue

				if "gI" in packet_json:
					self.logger.debug("Game ID: " + str(packet_json["gI"]))
				else:
					self.logger.error("Missing game ID!")
					continue

				game_id = settings.get_setting("server.game_id")
				if game_id != packet_json["gI"]:
					self.logger.info("Game ID mismatch: got %d, expected %d", packet_json["gI"], game_id)
					continue

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
				self.socket.sendto(response, client_address)
		except KeyboardInterrupt:
			self.logger.info("Caught keyboard interrupt, exiting")
		finally:
			self.socket.close()

	def shutdown(self):
		self.stop = True

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
		self.server = DiscoveryUDPServer((self.ip, self.port))
		self.server.start()

	def shutdown(self):
		"""Shuts down the Pou vs Pou discovery server."""
		self.server.shutdown()


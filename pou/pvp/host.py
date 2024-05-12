# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

from pou.pvp import discovery, settings

import threading

class PvPHost:
	"""Pou server that hosts a Pou vs Pou session. The server uses two
	sockets: a discovery UDP socket and the game socket over TCP.

	Attributes:
	discovery -- the discovery server
	"""
	def __init__(self):
		self.discovery = discovery.DiscoveryServer()

	def set_server_name(self, name: str):
		"""Sets the server name used for the Pou vs Pou session. The default name
		is "Pou vs Pou server".
		"""
		settings.set_setting("server.name", name)

	def set_game_id(self, game_id: int):
		"""Sets the Game ID used for the Pou vs Pou session. The default Game ID
		is 19 (Water Hop).
		"""
		settings.set_setting("server.game_id", game_id)

	def start(self):
		"""Starts the Pou vs Pou discovery and game server."""
		threads = []

		discovery_thread = threading.Thread(target = self.discovery.start)

		threads.append(discovery_thread)

		# Start all threads
		for x in threads:
			x.start()

		# Wait for all of them to finish
		for x in threads:
			x.join()

	def shutdown(self):
		"""Shuts down the Pou vs Pou discovery and game server."""
		self.discovery.shutdown()

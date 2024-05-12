# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

class Settings:
	"""Global settings for Pou vs Pou servers and clients. This class is for
	internal use, and the global functions should be used to modify the
	settings.

	Attributes:
	settings -- a dict with the settings
	"""
	def __init__(self):
		self.settings = {
			"log_format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",

			"server.game_id": 0,
			"server.name": "Pou vs Pou server"
		}

	def __getitem__(self, name):
		return self.settings[name]

	def __setitem__(self, name, value):
		if name not in self.settings:
			raise KeyError("Unknown setting: %s", name)

		self.settings[name] = value

_settings = Settings()

def get_setting(setting: str):
	"""Returns the value of a given setting."""
	return _settings[setting]

def set_setting(key, value):
	"""Applies a given setting."""
	_settings[key] = value

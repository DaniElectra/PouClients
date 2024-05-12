# SPDX-FileCopyrightText: 2024 DaniElectra
#
# SPDX-License-Identifier: MIT

class PouMinInfo:
	"""Holds information about the aspect of the Pou of a user.

	Attributes:
	size -- size of the Pou
	obesity -- obesity of the Pou
	mustache -- numeric value of the mustache
	lipstick -- numeric value of the lipstick
	body_color -- numeric value of body color
	outfit -- numeric value of the outfit
	neck_accesory -- numeric value of the neck accesory
	eyes_color -- numeric value of eyes color
	eyelash -- numeric value of the eyelash
	eyeliner -- numeric value of the eyeliner
	eyes_shadow_color -- numeric value of eyes shadow color
	eyeglasses -- numeric value of eyeglasses
	mask -- numeric value of the mask
	beard -- numeric value of the beard
	wig -- numeric value of the wig
	headband -- numerc value of the headband
	hat -- numeric value of the hat
	sticker -- numeric value of the sticker
	shoes -- numeric value of the shoes
	"""
	def __init__(self):
		self.size = 0.0
		self.obesity = 0.0
		self.mustache = 0
		self.lipstick = 0
		self.body_color = 0
		self.outfit = 0
		self.neck_accesory = 0
		self.eyes_color = 0
		self.eyelash = 0
		self.eyeliner = 0
		self.eyes_shadow_color = 0
		self.eyeglasses = 0
		self.mask = 0
		self.beard = 0
		self.wig = 0
		self.headband = 0
		self.hat = 0
		self.sticker = 0
		self.shoes = 0

	@staticmethod
	def from_response(response: dict):
		"""Fills the attributes of this class from a server response."""
		min_info = PouMinInfo()
		min_info.size = response["sz"]
		min_info.obesity = response["ob"]

		if "mus" in response:
			min_info.mustache = response["mus"]

		if "lip" in response:
			min_info.lipstick = response["lip"]

		min_info.body_color = response["bCo"]

		if "ouf" in response:
			min_info.outfit = response["ouf"]

		if "nek" in response:
			min_info.neck_accesory = response["nek"]

		min_info.eyes_color = response["eCo"]

		if "ela" in response:
			min_info.eyelash = response["ela"]

		if "eli" in response:
			min_info.eyeliner = response["eli"]

		if "esh" in response:
			min_info.eyes_shadow_color = response["esh"]

		if "egl" in response:
			min_info.eyeglasses = response["egl"]

		if "msk" in response:
			min_info.mask = response["msk"]

		if "brd" in response:
			min_info.beard = response["brd"]

		if "wig" in response:
			min_info.wig = response["wig"]

		if "hBa" in response:
			min_info.headband = response["hBa"]

		if "hat" in response:
			min_info.hat = response["hat"]

		if "stk" in response:
			min_info.sticker = response["stk"]

		if "sho" in response:
			min_info.shoes = response["sho"]

		return min_info

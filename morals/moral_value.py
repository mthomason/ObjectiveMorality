#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

from enum import Enum, EnumMeta, auto
from abc import ABC, ABCMeta, abstractmethod

class MoralValue(Enum):
	"""
	The fundamental, shared moral valuations for cross-philosophical comparison.
	"""
	GOOD = auto()			# Good, excellent, permissible, righteous
	BAD = auto()			# Bad, impermissible, vicious, corrupt
	NEUTRAL = auto()	# Permissible... the continent state

	def is_positive(self):
		return self == self.GOOD
	
	def is_negative(self):
		return self == self.BAD
	
	def is_neutral(self):
		return self == self.NEUTRAL

	def to_core(self):
		"""Maps any MoralValue to itself. This is the foundation."""
		return self

	def __str__(self):
		"""Pretty print value."""
		return self.name.title()
	
class AbcEnumMeta(ABCMeta, EnumMeta):
	"""Metaclass for combining ABC and Enum functionality"""
	pass

class PhilosophicalMoralValue(ABC, Enum, metaclass=AbcEnumMeta):
	"""
	Abstract base class for all philosophical moral value enum types.
	"""
	@abstractmethod
	def to_core(self) -> MoralValue:
		"""Maps this specific philosophical value to the universal MoralValue. """
		pass

	@abstractmethod
	def moral_quality(self) -> str:
		pass

	def __str__(self) -> str:
		"""Pretty print value."""
		return self.name.title()

class UtilitarianMoralValue(PhilosophicalMoralValue):
	"""
	A utilitarian moral state.
	"""
	PERMISSIBLE = auto()
	IMPERMISSIBLE = auto()
	NEUTRAL = auto()

	def to_core(self) -> MoralValue:
		"""Map utilitarian evaluation to core moral values."""
		if self == self.PERMISSIBLE:
			return MoralValue.GOOD
		elif self == self.IMPERMISSIBLE:
			return MoralValue.BAD
		else:
			return MoralValue.NEUTRAL


class AristotelianMoralValue(PhilosophicalMoralValue):
	"""
	Aristotle's four character states from Nicomachean Ethics.
	"""
	VIRTUOUS = auto()		# Excellence (ἀρετή): right action + right desire
	VICIOUS = auto()		# Corruption (κακία): wrong action + wrong desire
	CONTINENT = auto()		# Self-control (ἐγκράτεια): right action + wrong desire  
	INCONTINENT = auto()	# Weakness (ἀκρασία): wrong action + right desire

	def to_core(self) -> MoralValue:
		"""Map Aristotle's nuanced evaluation to core moral values."""
		if self == self.VIRTUOUS:
			return MoralValue.GOOD
		elif self == self.VICIOUS:
			return MoralValue.BAD
		else:  # CONTINENT or INCONTINENT
			return MoralValue.NEUTRAL

	def moral_quality(self) -> str:
		"""Describe the moral quality in Aristotelian terms."""
		if self == self.VIRTUOUS:
			return "Excellence of character (right action + right desire)"
		elif self == self.VICIOUS:
			return "Corruption of character (wrong action + wrong desire)"
		elif self == self.CONTINENT:
			return "Self-control (right action + wrong desire)"
		elif self == self.INCONTINENT:
			return "Weakness of will (wrong action + right desire)"
		else:
			raise ValueError(f"Unknown value: {self}")

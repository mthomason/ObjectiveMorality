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
	NEUTRAL = auto()		# Permissible... the continent state

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

class RossianMoralValue(PhilosophicalMoralValue):
	"""
	A Rossian moral state.
	"""
	PERMISSIBLE = auto()
	IMPERMISSIBLE = auto()
	CONFLICTING = auto()

	def to_core(self) -> MoralValue:
		"""Map Rossian evaluation to core moral values."""
		if self == self.PERMISSIBLE:
			return MoralValue.GOOD
		elif self == self.IMPERMISSIBLE:
			return MoralValue.BAD
		else:
			return MoralValue.NEUTRAL

	def moral_quality(self) -> str:
		if self == self.PERMISSIBLE:
			return "Permissible"
		elif self == self.IMPERMISSIBLE:
			return "Impermissible"
		else:
			return "Conflicting"

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

	def moral_quality(self) -> str:
		if self == self.PERMISSIBLE:
			return "Produces net positive utility/consequences"
		elif self == self.IMPERMISSIBLE:
			return "Produces net negative utility/consequences"
		else:
			return "Neutral impact on overall utility"

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

class NietzscheanMoralValue(PhilosophicalMoralValue):
	"""
	Nietzsche's moral valuations based on master vs. slave morality and will to power.
	"""
	MASTER_GOOD = auto()			# Life-affirming, noble, powerful (for the exceptional)
	MASTER_BAD = auto()				# Life-denying, contemptible, weak (for the exceptional)
	SLAVE_GOOD = auto()				# Meek, humble, pious (from perspective of slave morality)
	SLAVE_BAD = auto()				# Proud, powerful, selfish (from perspective of slave morality)
	# DESCRIPTIVE_SLAVE_GOOD = auto()	# "This is considered good in slave morality"
	# EVALUATIVE_SLAVE_BAD = auto()		# "But I critique it as life-denying"

	def to_core(self) -> MoralValue:
		"""Map Nietzsche's evaluation to core moral values."""
		if self == self.MASTER_GOOD:
			return MoralValue.GOOD  # From the master perspective
		elif self == self.SLAVE_GOOD:
			return MoralValue.GOOD  # From the slave perspective
		else:
			return MoralValue.BAD

	def moral_quality(self) -> str:
		"""Describe the moral quality in Nietzschean terms."""
		if self == self.MASTER_GOOD:
			return "Life-affirming master virtue (noble, powerful)"
		elif self == self.MASTER_BAD:
			return "Life-denying master vice (contemptible, weak)"
		elif self == self.SLAVE_GOOD:
			return "Slave virtue (meek, humble, pious)"
		elif self == self.SLAVE_BAD:
			return "Slave vice (proud, powerful, 'evil')"
		else:
			raise ValueError(f"Unknown value: {self}")

	def __str__(self) -> str:
		"""Pretty print value with underscore removed."""
		return self.name.title().replace("_", " ")

class CareMoralValue(PhilosophicalMoralValue):
	"""
	Ethics of Care moral valuations focused on relational nurturing.
	"""
	CARING = auto()			# Nurtures, maintains, or strengthens relationships
	UNCARING = auto()		# Harms, exploits, or weakens relationships
	NEUTRAL = auto()		# No significant impact on relationships

	def to_core(self) -> MoralValue:
		"""Map care ethics evaluation to core moral values."""
		if self == self.CARING:
			return MoralValue.GOOD
		elif self == self.UNCARING:
			return MoralValue.BAD
		else:
			return MoralValue.NEUTRAL

	def moral_quality(self) -> str:
		"""Describe the moral quality in care ethics terms."""
		if self == self.CARING:
			return "Nurtures and maintains caring relationships"
		elif self == self.UNCARING:
			return "Harms or exploits relationships"
		else:
			return "Neutral impact on relationships"

class RawlsianMoralValue(PhilosophicalMoralValue):
	"""
	Rawls' moral valuations focused on justice and fairness from behind the veil of ignorance.
	"""
	JUST = auto()		   # Promotes fairness, especially for least advantaged
	UNJUST = auto()		 # Creates or exacerbates unfair inequality
	NEUTRAL = auto()		# No significant impact on social justice

	def to_core(self) -> MoralValue:
		"""Map Rawlsian evaluation to core moral values."""
		if self == self.JUST:
			return MoralValue.GOOD
		elif self == self.UNJUST:
			return MoralValue.BAD
		else:
			return MoralValue.NEUTRAL

	def moral_quality(self) -> str:
		"""Describe the moral quality in Rawlsian terms."""
		if self == self.JUST:
			return "Promotes fair social arrangements (just)"
		elif self == self.UNJUST:
			return "Creates or maintains unfair inequality (unjust)"
		else:
			return "Neutral impact on social justice"

class KantianMoralValue(PhilosophicalMoralValue):
	"""
	A Kantian deontological moral state.
	"""
	PERMISSIBLE = auto()
	IMPERMISSIBLE = auto()

	def to_core(self) -> MoralValue:
		"""Map Kantian evaluation to core moral values."""
		if self == self.PERMISSIBLE:
			return MoralValue.GOOD
		elif self == self.IMPERMISSIBLE:
			return MoralValue.BAD
		else:
			# Should not get here...
			return MoralValue.NEUTRAL

	def moral_quality(self) -> str:
		if self == self.PERMISSIBLE:
			return "Passes the categorical imperative test (universalizable without contradiction)"
		elif self == self.IMPERMISSIBLE:
			return "Fails the categorical imperative test (cannot be universalized without contradiction)"
		else:
			# Should not get here...
			return "No clear violation or adherence to moral law"

class ContractualistMoralValue(PhilosophicalMoralValue):
	"""
	A Contractualist moral state (Scanlon-style).
	"""
	PERMISSIBLE = auto()
	IMPERMISSIBLE = auto()

	def to_core(self) -> MoralValue:
		"""Map Contractualist evaluation to core moral values."""
		if self == self.PERMISSIBLE:
			return MoralValue.GOOD
		elif self == self.IMPERMISSIBLE:
			return MoralValue.BAD
		else:
			# Should not get here...
			return MoralValue.NEUTRAL

	def moral_quality(self) -> str:
		if self == self.PERMISSIBLE:
			return "Reasonable persons could not reject this principle"
		elif self == self.IMPERMISSIBLE:
			return "Reasonable persons would reject this principle"
		else:
			# Should not get here...
			return "No clear agreement among reasonable persons"

__all__ = [
	'MoralValue',
	'PhilosophicalMoralValue',
	'AristotelianMoralValue',
	'UtilitarianMoralValue',
	'RossianMoralValue',
	'NietzscheanMoralValue',
	'CareMoralValue',
	'RawlsianMoralValue',
	'KantianMoralValue',
	'ContractualistMoralValue'
]

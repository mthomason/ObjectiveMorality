#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, EnumMeta
from abc import ABCMeta
from typing import TypeVar, Type

_MEB = TypeVar('_MEB', bound='MoralEnumBase')

class AbcEnumMeta(ABCMeta, EnumMeta):
	"""Metaclass for combining ABC and Enum functionality"""
	pass

class MoralEnumBase(Enum, metaclass=AbcEnumMeta):
	"""
	A mixin class for Enums that adds a from_str class method.
	This class inherits from Enum and uses the custom metaclass.
	"""
	@classmethod
	def from_str(cls: Type[_MEB], value: str) -> _MEB:
		"""
		Retrieves an Enum member by its name (string value).
		This method is case-sensitive and will raise a ValueError if
		the name is not found.

		Args:
			cls: The Enum class itself (e.g., AgentType).
			value: The string name of the Enum member.

		Returns:
			The corresponding Enum member.

		Raises:
			ValueError: If the string value does not match a member name.
		"""
		try:
			return cls[value]
		except KeyError:
			# It's good practice to provide a clear error message.
			raise ValueError(f"'{value}' is not a valid member of {cls.__name__}")

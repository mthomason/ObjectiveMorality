#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

from dataclasses import dataclass

@dataclass(frozen=True)
class UniversalizedResult:
	"""
	Represents the result of universalizing a moral principle.
	"""
	self_collapse: bool

	def __post_init__(self):
		if not isinstance(self.self_collapse, bool):
			raise TypeError("self_collapse must be a boolean")

@dataclass(frozen=True)
class Consequences:
	"""
	Quantifies the net flourishing resulting from an action.
	"""
	net_flourishing: int

	def __post_init__(self):
		if not isinstance(self.net_flourishing, int):
			raise TypeError("net_flourishing must be an integer")

@dataclass(frozen=True)
class CooperativeOutcome:
	"""
	Indicates whether cooperation was stable in the scenario.
	"""
	stable: bool

	def __post_init__(self):
		if not isinstance(self.stable, bool):
			raise TypeError("stable must be a boolean")

@dataclass(frozen=True)
class TrustImpact:
	"""
	Records whether trust was breached in the interaction.
	"""
	breach: bool

	def __post_init__(self):
		if not isinstance(self.breach, bool):
			raise TypeError("breach must be a boolean")

@dataclass(frozen=True)
class MoralContext:
	"""
	Comprehensive moral evaluation context combining multiple ethical frameworks.
	"""
	universalized_result: UniversalizedResult
	consequences: Consequences
	cooperative_outcome: CooperativeOutcome
	trust_impact: TrustImpact

	def __post_init__(self):
		# Type validation
		if not isinstance(self.universalized_result, UniversalizedResult):
			raise TypeError("universalized_result must be a UniversalizedResult instance")
		if not isinstance(self.consequences, Consequences):
			raise TypeError("consequences must be a Consequences instance")
		if not isinstance(self.cooperative_outcome, CooperativeOutcome):
			raise TypeError("cooperative_outcome must be a CooperativeOutcome instance")
		if not isinstance(self.trust_impact, TrustImpact):
			raise TypeError("trust_impact must be a TrustImpact instance")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

from dataclasses import dataclass, field
from enum import Enum, auto

# Enums Defining Types and Categories

class AgentType(Enum):
	"""
	Rough categorization of the moral agent's role or nature.
	"""
	STRANGER = auto()
	FRIEND = auto()
	FAMILY_MEMBER = auto()
	STATE_OFFICIAL = auto()
	MASTER = auto()
	SLAVE = auto()
	VIRTUOUS = auto()
	VICIOUS = auto()

class Virtue(Enum):
	"""
	A list of positive character traits (Aristotelian virtues).
	"""
	HONESTY = auto()
	COURAGE = auto()
	LOYALTY = auto()
	COMPASSION = auto()
	JUSTICE = auto()
	TEMPERANCE = auto()
	WISDOM = auto()

class Vice(Enum):
	"""
	A list of negative character traits.
	"""
	DISHONESTY = auto()
	COWARDICE = auto()
	BETRAYAL = auto()
	CRUELTY = auto()
	UNFAIRNESS = auto()
	INDULGENCE = auto()
	FOOLISHNESS = auto()

class DutyType(Enum):
	"""
	W.D. Ross's Prima Facie duties.
	"""
	FIDELITY = auto()			# Duty to keep promises
	REPARATION = auto()			# Duty to correct past wrongs
	GRATITUDE = auto()			# Duty to repay favors
	JUSTICE = auto()			# Duty to ensure fair distribution
	BENEFICENCE = auto()		# Duty to improve the lives of others
	SELF_IMPROVEMENT = auto()	# Duty to improve oneself
	NON_MALEFICENCE = auto()	# Duty to avoid harming others

class RelationshipImpact(Enum):
	"""
	Types of impacts for an Ethics of Care framework.
	"""
	NURTURES = auto()
	EXPLOITS = auto()
	STRENGTHENS = auto()
	WEAKENS = auto()
	BREACHES_TRUST = auto()
	BUILDS_TRUST = auto()

class TimeHorizon(Enum):
	"""
	Time horizon type. This is used for calculating `effective_utility()` from `net_utility`.
	"""
	SHORT = auto()
	MEDIUM = auto()
	LONG = auto()

@dataclass(frozen=True)
class UniversalizedResult:
	"""
	Represents the result of universalizing a moral principle.
	"""
	self_collapse: bool = False
	contradiction_in_will: bool = False

	def __post_init__(self):
		if not isinstance(self.self_collapse, bool):
			raise TypeError("self_collapse must be a boolean")
		if not isinstance(self.contradiction_in_will, bool):
			raise TypeError("contradiction_in_will must be a boolean")

@dataclass(frozen=True)
class Consequences:
	"""
	Quantifies the net flourishing resulting from an action.
	"""
	net_flourishing: int = 0
	net_utility: int = 0
	power_expression: int = 0	# Nietzschean metric
	individual_impact: dict[str, int] = field(default_factory=dict)
	time_horizon: TimeHorizon = TimeHorizon.MEDIUM

	def __post_init__(self):
		if not isinstance(self.net_flourishing, int):
			raise TypeError("net_flourishing must be an integer")
		if not isinstance(self.net_utility, int):
			raise TypeError("net_utility must be an integer")
		if not isinstance(self.power_expression, int):
			raise TypeError("power_expression must be an integer")
		if not isinstance(self.time_horizon, TimeHorizon):
			raise TypeError("time_horizon must be type TimeHorizon")
	
	def effective_utility(self) -> int:
		"""Discount future utility appropriately"""
		if self.time_horizon == TimeHorizon.SHORT:
			return self.net_utility
		elif self.time_horizon == TimeHorizon.MEDIUM:
			return int(self.net_utility * 0.8)
		else:  # TimeHorizon.LONG
			return int(self.net_utility * 0.6)

@dataclass(frozen=True)
class CooperativeOutcome:
	"""
	Indicates whether cooperation was stable in the scenario (Game Theory / Aristotelian).
	"""
	stable: bool = True
	societal_trust_change: int = 0 # e.g., +1 for strengthens, -1 for weakens

	def __post_init__(self):
		if not isinstance(self.stable, bool):
			raise TypeError("stable must be a boolean")
		if not isinstance(self.societal_trust_change, int):
			raise TypeError("societal_trust_change must be a integer")

@dataclass(frozen=True)
class TrustImpact:
	"""
	Records whether trust was breached in the interaction.
	"""
	breach: bool = False
	relationships_affected: list[str] = field(default_factory=list)
	impact_type: list[RelationshipImpact] = field(default_factory=list)

	def __post_init__(self):
		if not isinstance(self.breach, bool):
			raise TypeError("breach must be a boolean")

@dataclass(frozen=True)
class Agent:
	"""
	Represents the person performing the action (Virtue Ethics / Nietzschean)
	"""
	agent_type: AgentType = AgentType.STRANGER
	virtues: list[Virtue] = field(default_factory=list)
	vices: list[Vice] = field(default_factory=list)

	def __post_init__(self):
		if not isinstance(self.agent_type, AgentType):
			raise TypeError("agent_type must be an AgentType type")

@dataclass(frozen=True)
class DutyAssessment:
	"""
	A list of duties relevant to the action (Rossian Deontology).
	"""
	duties_upheld: list[DutyType] = field(default_factory=list)
	duties_violated: list[DutyType] = field(default_factory=list)

@dataclass(frozen=True)
class MoralContext:
	"""
	Comprehensive moral evaluation context combining multiple ethical frameworks.
	"""
	universalized_result: UniversalizedResult = field(default_factory=UniversalizedResult)
	consequences: Consequences = field(default_factory=Consequences)
	cooperative_outcome: CooperativeOutcome = field(default_factory=CooperativeOutcome)
	trust_impact: TrustImpact = field(default_factory=TrustImpact)
	agent: Agent = field(default_factory=Agent)
	duty_assessment: DutyAssessment = field(default_factory=DutyAssessment)
	action_description: str = "An action was performed."

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
		
		if not isinstance(self.agent, Agent):
			raise TypeError("agent must be a Agent instance")
		if not isinstance(self.duty_assessment, DutyAssessment):
			raise TypeError("duty_assessment must be a DutyAssessment instance")
		if not isinstance(self.action_description, str):
			raise TypeError("action_description must be a string")

__all__ = [
	'MoralContext',
	'TrustImpact',
	'CooperativeOutcome',
	'Consequences',
	'UniversalizedResult',
	'DutyAssessment',
	'Agent',
	'Virtue',
	'Vice',
	'DutyType',
	'AgentType',
	'RelationshipImpact',
	'TimeHorizon'
]

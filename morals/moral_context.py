#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TypeVar, Any

T = TypeVar('T')

class JSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Enum):
			return obj.name
		if hasattr(obj, 'to_dict'):
			return obj.to_dict()
		return super().default(obj)

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

	@classmethod
	def from_str(cls, value: str) -> 'AgentType':
		return cls[value]

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

	@classmethod
	def from_str(cls, value: str) -> 'Virtue':
		return cls[value]

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

	@classmethod
	def from_str(cls, value: str) -> 'Vice':
		return cls[value]

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

	@classmethod
	def from_str(cls, value: str) -> 'DutyType':
		return cls[value]

class RelationshipType(Enum):
	"""
	Core types of moral relationships from care ethics and virtue ethics perspectives.
	"""
	# Primary relationships (strongest obligations)
	PARENT_CHILD = auto()
	CHILD_PARENT = auto()
	SPOUSE_SPOUSE = auto()
	SIBLING_SIBLING = auto()
	
	# Extended family
	FAMILY_MEMBER = auto()  # Generic family relationship
	
	# Chosen relationships
	FRIEND_FRIEND = auto()
	ROMANTIC_PARTNERS = auto()
	
	# Care relationships
	CAREGIVER_RECEIVER = auto()  # Nurse-patient, etc.
	TEACHER_STUDENT = auto()
	
	# Community relationships
	NEIGHBOR_NEIGHBOR = auto()
	COMMUNITY_MEMBER = auto()
	WORK_COLLEAGUE = auto()
	
	# Societal relationships
	CITIZEN_STATE = auto()
	PROFESSIONAL_CLIENT = auto()  # Doctor-patient, lawyer-client
	
	# Universal relationships
	STRANGER_STRANGER = auto()
	HUMAN_HUMAN = auto()  # Most abstract care relationship
	
	# Institutional relationships
	EMPLOYER_EMPLOYEE = auto()
	BUSINESS_CUSTOMER = auto()

	@classmethod
	def from_str(cls, value: str) -> 'RelationshipType':
		return cls[value]


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

	@classmethod
	def from_str(cls, value: str) -> 'RelationshipImpact':
		return cls[value]

class TimeHorizon(Enum):
	"""
	Time horizon type. This is used for calculating `effective_utility()` from `net_utility`.
	"""
	SHORT = auto()
	MEDIUM = auto()
	LONG = auto()

	@classmethod
	def from_str(cls, value: str) -> 'TimeHorizon':
		return cls[value]

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

	def to_dict(self) -> dict[str, Any]:
		return {
			'self_collapse': self.self_collapse,
			'contradiction_in_will': self.contradiction_in_will
		}
	
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> 'UniversalizedResult':
		return cls(
			self_collapse=data['self_collapse'],
			contradiction_in_will=data['contradiction_in_will']
		)

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

	def to_dict(self) -> dict[str, Any]:
		return {
			'net_flourishing': self.net_flourishing,
			'net_utility': self.net_utility,
			'power_expression': self.power_expression,
			'individual_impact': self.individual_impact,
			'time_horizon': self.time_horizon.name
		}
	
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> 'Consequences':
		return cls(
			net_flourishing=data['net_flourishing'],
			net_utility=data['net_utility'],
			power_expression=data['power_expression'],
			individual_impact=data['individual_impact'],
			time_horizon=TimeHorizon.from_str(data['time_horizon'])
		)

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

	def to_dict(self) -> dict[str, Any]:
		return {
			'stable': self.stable,
			'societal_trust_change': self.societal_trust_change
		}
	
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> 'CooperativeOutcome':
		return cls(
			stable=data['stable'],
			societal_trust_change=data['societal_trust_change']
		)

@dataclass(frozen=True)
class TrustImpact:
	"""
	Records whether trust was breached in the interaction.
	"""
	breach: bool = False
	relationships_affected: list[RelationshipType] = field(default_factory=list)
	impact_type: list[RelationshipImpact] = field(default_factory=list)

	def __post_init__(self):
		if not isinstance(self.breach, bool):
			raise TypeError("breach must be a boolean")

	def to_dict(self) -> dict[str, Any]:
		return {
			'breach': self.breach,
			'relationships_affected': [relationship.name for relationship in self.relationships_affected],
			'impact_type': [impact.name for impact in self.impact_type]
		}

	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> 'TrustImpact':
		return cls(
			breach=data['breach'],
			relationships_affected=[RelationshipType.from_str(relationship) for relationship in data['relationships_affected']],
			impact_type=[RelationshipImpact.from_str(impact) for impact in data['impact_type']]
		)

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

	def to_dict(self) -> dict[str, Any]:
		return {
			'agent_type': self.agent_type.name,
			'virtues': [virtue.name for virtue in self.virtues],
			'vices': [vice.name for vice in self.vices]
		}
	
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> 'Agent':
		return cls(
			agent_type=AgentType.from_str(data['agent_type']),
			virtues=[Virtue.from_str(virtue) for virtue in data['virtues']],
			vices=[Vice.from_str(vice) for vice in data['vices']]
		)

@dataclass(frozen=True)
class DutyAssessment:
	"""
	A list of duties relevant to the action (Rossian Deontology).
	"""
	duties_upheld: list[DutyType] = field(default_factory=list)
	duties_violated: list[DutyType] = field(default_factory=list)

	def to_dict(self) -> dict[str, Any]:
		return {
			'duties_upheld': [duty.name for duty in self.duties_upheld],
			'duties_violated': [duty.name for duty in self.duties_violated]
		}
	
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> 'DutyAssessment':
		return cls(
			duties_upheld=[DutyType.from_str(duty) for duty in data['duties_upheld']],
			duties_violated=[DutyType.from_str(duty) for duty in data['duties_violated']]
		)

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

	def to_dict(self) -> dict[str, Any]:
		return {
			'action_description': self.action_description,
			'universalized_result': self.universalized_result.to_dict(),
			'consequences': self.consequences.to_dict(),
			'cooperative_outcome': self.cooperative_outcome.to_dict(),
			'trust_impact': self.trust_impact.to_dict(),
			'agent': self.agent.to_dict(),
			'duty_assessment': self.duty_assessment.to_dict()
		}
	
	@classmethod
	def from_dict(cls, data: dict[str, Any]) -> 'MoralContext':
		return cls(
			action_description=data['action_description'],
			universalized_result=UniversalizedResult.from_dict(data['universalized_result']),
			consequences=Consequences.from_dict(data['consequences']),
			cooperative_outcome=CooperativeOutcome.from_dict(data['cooperative_outcome']),
			trust_impact=TrustImpact.from_dict(data['trust_impact']),
			agent=Agent.from_dict(data['agent']),
			duty_assessment=DutyAssessment.from_dict(data['duty_assessment'])
		)
	
	def to_json(self, filepath: str) -> None:
		"""Save MoralContext to JSON file"""
		with open(filepath, 'w', encoding='utf-8') as f:
			json.dump(self.to_dict(), f, indent=2, cls=JSONEncoder, ensure_ascii=False)
	
	@classmethod
	def from_json(cls, filepath: str) -> 'MoralContext':
		"""Load MoralContext from JSON file"""
		with open(filepath, 'r', encoding='utf-8') as f:
			data = json.load(f)
		return cls.from_dict(data)

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
	'RelationshipType',
	'RelationshipImpact',
	'TimeHorizon',
	'JSONEncoder'
]

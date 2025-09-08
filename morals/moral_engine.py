#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

from .moral_context import MoralContext, DutyType, AgentType, RelationshipImpact
from .moral_value import *

# ------------------------------
# Base Class for Moral Engines
# ------------------------------

class MoralEngine:
	def evaluate(self, action: str, context: MoralContext) -> PhilosophicalMoralValue:
		raise NotImplementedError("Each moral engine must implement evaluate()")

# ------------------------------
# Kantian Engine (Deontological)
# ------------------------------

class KantianEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		"""
		Action is wrong if universalizing it causes contradiction.
		"""
		if context.universalized_result.self_collapse or context.universalized_result.contradiction_in_will:
			return UtilitarianMoralValue.IMPERMISSIBLE
		return UtilitarianMoralValue.PERMISSIBLE

# ------------------------------
# Utilitarian Engine (Consequentialist)
# ------------------------------

class UtilitarianEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		"""
		Action is right if net flourishing > 0
		"""
		net_value: int = context.consequences.net_utility
		if net_value == 0:
			net_value = context.consequences.net_flourishing

		if net_value > 0:
			return UtilitarianMoralValue.PERMISSIBLE
		elif net_value < 0:
			return UtilitarianMoralValue.IMPERMISSIBLE
		else:
			return UtilitarianMoralValue.NEUTRAL

# ------------------------------
# Aristotelian Engine (Virtue Ethics)
# ------------------------------

class AristotelianEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		"""
		Action is virtuous if it aligns with flourishing life & stable character.
		Uses consequences + trust + social stability as proxies.
		"""
		net_flourishing: int = context.consequences.net_flourishing
		stable: bool = context.cooperative_outcome.stable
		has_virtues: bool = len(context.agent.virtues) > 0
		has_vices: bool = len(context.agent.vices) > 0

		if net_flourishing < 0 and not stable:
			return AristotelianMoralValue.VICIOUS
		elif net_flourishing < 0:
			if has_vices:
				return AristotelianMoralValue.VICIOUS
			else:
				return AristotelianMoralValue.INCONTINENT
		elif net_flourishing > 0 and stable:
			if has_virtues and not has_vices:
				return AristotelianMoralValue.VIRTUOUS
			else:
				return AristotelianMoralValue.CONTINENT
		elif net_flourishing > 0 and not stable:
			if has_virtues:
				return AristotelianMoralValue.CONTINENT
			else:
				return AristotelianMoralValue.INCONTINENT
		else: # net_flourishing == 0
			if stable:
				return AristotelianMoralValue.CONTINENT
			else:
				return AristotelianMoralValue.INCONTINENT

# ------------------------------
# Contractualist Engine
# ------------------------------

class ContractualistEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		"""
		Action is wrong if reasonable persons behind a veil of ignorance
		would reject the rule permitting it.
		"""
		if context.trust_impact.breach or context.cooperative_outcome.societal_trust_change < 0:
			return UtilitarianMoralValue.IMPERMISSIBLE
		return UtilitarianMoralValue.PERMISSIBLE

# ------------------------------
# Rossian Engine
# ------------------------------

class RossianEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		# Define a hierarchy or weighting of duties. Non-maleficence is often strongest.
		duty_weights = {
			DutyType.NON_MALEFICENCE: 10,
			DutyType.FIDELITY: 7,
			DutyType.JUSTICE: 8,
			DutyType.BENEFICENCE: 6,
			DutyType.GRATITUDE: 5,
			DutyType.REPARATION: 5,
			DutyType.SELF_IMPROVEMENT: 4,
		}
		# Calculate the total "moral weight" of upheld vs. violated duties
		weight_upheld = sum(duty_weights[d] for d in context.duty_assessment.duties_upheld)
		weight_violated = sum(duty_weights[d] for d in context.duty_assessment.duties_violated)

		if weight_upheld > weight_violated:
			return RossianMoralValue.PERMISSIBLE # Right action
		elif weight_upheld < weight_violated:
			return RossianMoralValue.IMPERMISSIBLE # Wrong action
		else:
			return RossianMoralValue.CONFLICTING

# ------------------------------
# Nietzschean Engine
# ------------------------------

class NietzscheanEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		# Nietzsche would evaluate based on the agent's type and the action's nature
		if context.agent.agent_type == AgentType.MASTER:
			# For a "master" type, an action is good if it expresses power and creativity.
			if context.consequences.power_expression > 0 and not context.trust_impact.breach:
				return NietzscheanMoralValue.MASTER_GOOD
			else:
				return NietzscheanMoralValue.MASTER_BAD
		else:
			# For a "slave" type, he would critique their morality but describe it.
			if context.trust_impact.breach: # Slave morality emphasizes meekness, fairness
				return NietzscheanMoralValue.SLAVE_BAD
			else:
				return NietzscheanMoralValue.SLAVE_GOOD

# ------------------------------
# Ethics of Care Engine
# ------------------------------

class EthicsOfCareEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		# Focuses on relational impact, not abstract rules or total utility.
		if (RelationshipImpact.NURTURES in context.trust_impact.impact_type or
			RelationshipImpact.STRENGTHENS in context.trust_impact.impact_type):
			return CareMoralValue.CARING
		elif (RelationshipImpact.EXPLOITS in context.trust_impact.impact_type or RelationshipImpact.WEAKENS in context.trust_impact.impact_type):
			return CareMoralValue.UNCARING
		else:
			return CareMoralValue.NEUTRAL

# ------------------------------
# Moral Engine Runner
# ------------------------------

class MoralEngineRunner:
	def run_engines(self, action: str, context: MoralContext):
		engines = {
			"Kantian": KantianEngine(),
			"Utilitarian": UtilitarianEngine(),
			"Aristotelian": AristotelianEngine(),
			"Contractualist": ContractualistEngine(),
			"Rossian": RossianEngine(),
			"Nietzschean": NietzscheanEngine(),
			"Ethics of Care": EthicsOfCareEngine(),
		}
	
		results = {}
		for name, engine in engines.items():
			results[name] = str(engine.evaluate(action, context))
		return results

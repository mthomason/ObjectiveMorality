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
			return KantianMoralValue.IMPERMISSIBLE
		return KantianMoralValue.PERMISSIBLE

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
			return ContractualistMoralValue.IMPERMISSIBLE
		return ContractualistMoralValue.PERMISSIBLE

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
# Rawlsian Engine
# ------------------------------

class RawlsianEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		# An action is unjust if it increases inequality or harms the least advantaged.
		# We use `societal_trust_change` as a proxy for social stability/justice.
		if context.cooperative_outcome.societal_trust_change < 0:
			return RawlsianMoralValue.UNJUST
		else:
			return RawlsianMoralValue.JUST

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
			"Rawlsian": RawlsianEngine(),
		}
		
		results = {}
		for name, engine in engines.items():
			moral_value = engine.evaluate(action, context)
			results[name] = {
				'value_obj': moral_value,  # Store the actual enum object
				'value_str': str(moral_value),
				'quality': moral_value.moral_quality(),
				'core': moral_value.to_core()  # Store the MoralValue enum, not string
			}
		return results

	def display_results(self, action: str, results: dict):
		"""Display the results in a rich, formatted way."""
		print(f"\n{'='*60}")
		print(f"MORAL ANALYSIS: {action.upper()}")
		print(f"{'='*60}")
		
		# Group by core moral value ENUM for quick overview
		core_groups: dict[MoralValue, list] = {
			MoralValue.GOOD: [],
			MoralValue.BAD: [],
			MoralValue.NEUTRAL: []
		}
		
		for philosopher, data in results.items():
			core_value = data['core']  # This is now the MoralValue enum
			core_groups[core_value].append(f"  {philosopher:.<25}: {data['value_str']}")
		
		print("\nQUICK CONSENSUS:")
		print(f"✓ GOOD ({len(core_groups[MoralValue.GOOD])}):")
		for item in core_groups[MoralValue.GOOD]:
			print(f"   {item}")
		
		print(f"\n✗ BAD ({len(core_groups[MoralValue.BAD])}):")
		for item in core_groups[MoralValue.BAD]:
			print(f"   {item}")
		
		neutral_count = len(core_groups[MoralValue.NEUTRAL])
		if neutral_count > 0:
			print(f"\n~ NEUTRAL ({neutral_count}):")
			for item in core_groups[MoralValue.NEUTRAL]:
				print(f"   {item}")
		
		print(f"\n{'─'*60}")
		print("DETAILED ANALYSIS:")
		print(f"{'─'*60}")
		
		for philosopher, data in results.items():
			print(f"\n{philosopher}:")
			print(f"  Verdict: {data['value_str']}")
			print(f"  Meaning: {data['quality']}")
			print(f"  Core: {data['core'].name}")  # Use .name for the enum constant name
		
		# Optional: Show the core moral value mapping
		print(f"\n{'─'*60}")
		print("CORE MORAL VALUE MAPPING:")
		print(f"{'─'*60}")
		core_summary: dict = {}
		for philosopher, data in results.items():
			core_value = data['core']
			if core_value not in core_summary:
				core_summary[core_value] = []
			core_summary[core_value].append(philosopher)
		
		for core_value, philosophers in core_summary.items():
			print(f"{core_value.name}: {', '.join(philosophers)}")

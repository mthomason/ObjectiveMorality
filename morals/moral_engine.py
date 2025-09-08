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
		# Context-sensitive duty weights
		duty_weights = self._calculate_contextual_weights(context)

		weight_upheld = sum(duty_weights[d] for d in context.duty_assessment.duties_upheld)
		weight_violated = sum(duty_weights[d] for d in context.duty_assessment.duties_violated)

		# Add margin for Ross's "moral uncertainty"
		if abs(weight_upheld - weight_violated) < 3:  # Too close to call
			return RossianMoralValue.CONFLICTING
		elif weight_upheld > weight_violated:
			return RossianMoralValue.PERMISSIBLE
		else:
			return RossianMoralValue.IMPERMISSIBLE

	def _calculate_contextual_weights(self, context: MoralContext) -> dict[DutyType, int]:
		"""Duty stringency depends on context - this is key to Ross's theory"""
		base_weights = {
			DutyType.NON_MALEFICENCE: 10,
			DutyType.FIDELITY: 7,
			DutyType.JUSTICE: 8,
			DutyType.BENEFICENCE: 6,
			DutyType.GRATITUDE: 5,
			DutyType.REPARATION: 5,
			DutyType.SELF_IMPROVEMENT: 4,
		}

		# Adjust based on context (example logic)
		if context.consequences.net_utility < -10:
			base_weights[DutyType.NON_MALEFICENCE] += 5  # Harm prevention becomes more urgent

		return base_weights

# ------------------------------
# Nietzschean Engine
# ------------------------------

class NietzscheanEngine(MoralEngine):
	def evaluate(self, action, context) -> PhilosophicalMoralValue:
		"""
		Authentic Nietzschean evaluation based on:
		1. Does the action express will to power or will to weakness?
		2. Is it active/creative or reactive/resentful?
		3. Does it affirm or deny life?
		4. Does it originate from strength or fear?
		"""
		# Nietzschean analysis of the action's character
		is_active = (context.consequences.power_expression > 2 and 
					not context.trust_impact.breach)
		
		is_reactive = (context.trust_impact.breach or 
					  context.consequences.power_expression < 0)
		
		is_life_affirming = (context.consequences.net_flourishing > 0 or
							context.consequences.power_expression > 5)
		
		is_life_denying = (context.consequences.net_flourishing < -5 or
						  context.cooperative_outcome.societal_trust_change < -3)
		
		originates_from_strength = (context.consequences.power_expression > 3 and
								   len(context.agent.virtues) > len(context.agent.vices))
		
		originates_from_fear = (context.consequences.power_expression < 0 or
							   context.cooperative_outcome.stable == False)

		# Master morality: active, creative, life-affirming, from strength
		if (is_active and is_life_affirming and originates_from_strength):
			return NietzscheanMoralValue.MASTER_GOOD
			
		# Slave morality: reactive, resentful, life-denying, from fear/weakness  
		elif (is_reactive and is_life_denying and originates_from_fear):
			return NietzscheanMoralValue.SLAVE_BAD
			
		# Borderline cases that might align with slave morality's "good"
		elif (not context.trust_impact.breach and 
			  context.consequences.net_flourishing >= 0):
			return NietzscheanMoralValue.SLAVE_GOOD
			
		else:
			# Truly ambiguous or complex cases
			return NietzscheanMoralValue.SLAVE_BAD  # Default skeptical position

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

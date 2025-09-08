#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

from .moral_context import MoralContext, DutyType, AgentType, RelationshipImpact, TimeHorizon
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
		net_value: int = context.consequences.effective_utility()
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

		# Long-term negative consequences might indicate vice even if short-term looks good
		if (context.consequences.net_flourishing > 0 and
			context.consequences.time_horizon == TimeHorizon.SHORT and
			context.consequences.effective_utility() < 0):
			return AristotelianMoralValue.INCONTINENT	# Short-sighted action

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
		"""
		Ross's intuitionist pluralism: Duties are prima facie obligations
		that must be weighed against each other in specific contexts.
		"""
		# Context-sensitive duty weights
		duty_weights = self._calculate_contextual_weights(context)

		# Sum the stringency of upheld vs. violated duties
		weight_upheld = sum(duty_weights[d] for d in context.duty_assessment.duties_upheld)
		weight_violated = sum(duty_weights[d] for d in context.duty_assessment.duties_violated)

		# Add margin for Ross's "moral uncertainty"
		if abs(weight_upheld - weight_violated) < self._get_uncertainty_threshold(context):
			return RossianMoralValue.CONFLICTING
		elif weight_upheld > weight_violated:
			return RossianMoralValue.PERMISSIBLE
		else:
			return RossianMoralValue.IMPERMISSIBLE

	def _calculate_contextual_weights(self, context: MoralContext) -> dict[DutyType, int]:
		"""
		Ross's duty weighting considers:
		1. Basic stringency of duty types
		2. Contextual factors that modify duty strength
		3. Special obligations based on relationships
		"""
		weights = {
			DutyType.NON_MALEFICENCE: 12,	# Most stringent (do no harm)
			DutyType.JUSTICE: 10,			# Fairness and distribution
			DutyType.FIDELITY: 9,			# Promise-keeping and honesty
			DutyType.REPARATION: 8,			# Correcting past wrongs
			DutyType.GRATITUDE: 7,			# Repaying benefits received
			DutyType.BENEFICENCE: 6,		# Helping others
			DutyType.SELF_IMPROVEMENT: 5,	# Improving oneself
		}
		self._apply_contextual_modifiers(weights, context)
		return weights

	def _apply_contextual_modifiers(self, weights: dict, context: MoralContext):
		"""Apply Ross's contextual considerations to duty weights"""
		
		# Time horizon affects all duties (future consequences matter)
		time_modifier = {
			TimeHorizon.SHORT: 0.8,   # Short-term consequences discounted
			TimeHorizon.MEDIUM: 1.0,   # Standard weighting
			TimeHorizon.LONG: 1.2	  # Long-term consequences emphasized
		}[context.consequences.time_horizon]
		
		for duty in weights:
			weights[duty] = int(weights[duty] * time_modifier)
		
		# Relationship-based modifiers (Ross emphasized special obligations)
		if context.agent.agent_type in [AgentType.FRIEND, AgentType.FAMILY_MEMBER]:
			weights[DutyType.FIDELITY] += 3   # Stronger fidelity to close relations
			weights[DutyType.GRATITUDE] += 2  # Stronger gratitude to intimates
		
		# Harm severity amplifies non-maleficence
		if context.consequences.net_utility < -10:
			weights[DutyType.NON_MALEFICENCE] += 4
		
		# Significant injustice amplifies justice duty
		if context.cooperative_outcome.societal_trust_change < -5:
			weights[DutyType.JUSTICE] += 3

	def _get_uncertainty_threshold(self, context: MoralContext) -> int:
		"""
		Ross acknowledged moral decisions often involve uncertain weighing
		of competing duties. This threshold reflects that uncertainty.
		"""
		# More complex situations have higher uncertainty
		complexity_factor = (len(context.duty_assessment.duties_upheld) + 
						   len(context.duty_assessment.duties_violated))
		
		# Conflicting relationships increase uncertainty
		relationship_complexity = len(context.trust_impact.relationships_affected)
		
		return 2 + complexity_factor + relationship_complexity

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

	def display_results(self, action: str, context: MoralContext, results: dict):
		"""Display the results with context information for better understanding."""
		print(f"\n{'='*80}")
		print(f"MORAL ANALYSIS: {action.upper()}")
		print(f"{'='*80}")
		
		# Display context information first
		print(f"\nCONTEXT:")
		print(f"  Action: {context.action_description}")
		print(f"  Universalization: Self-collapse={context.universalized_result.self_collapse}, "
			  f"Contradiction={context.universalized_result.contradiction_in_will}")
		print(f"  Consequences: Net flourishing={context.consequences.net_flourishing}, "
			  f"Net utility={context.consequences.net_utility}")
		print(f"  Time horizon: {context.consequences.time_horizon.name}")
		print(f"  Power expression: {context.consequences.power_expression}")
		print(f"  Cooperative outcome: Stable={context.cooperative_outcome.stable}, "
			  f"Trust change={context.cooperative_outcome.societal_trust_change}")
		print(f"  Trust impact: Breach={context.trust_impact.breach}, "
			  f"Relationships affected={context.trust_impact.relationships_affected}")
		print(f"  Agent: Type={context.agent.agent_type.name}, "
			  f"Virtues={[v.name for v in context.agent.virtues]}, "
			  f"Vices={[v.name for v in context.agent.vices]}")
		print(f"  Duties: Upheld={[d.name for d in context.duty_assessment.duties_upheld]}, "
			  f"Violated={[d.name for d in context.duty_assessment.duties_violated]}")
		
		# Individual impacts (if any)
		if context.consequences.individual_impact:
			print(f"  Individual impacts:")
			for entity, impact in context.consequences.individual_impact.items():
				print(f"	{entity}: {impact:+d}")
		
		# Group by core moral value ENUM for quick overview
		core_groups: dict[MoralValue, list] = {
			MoralValue.GOOD: [],
			MoralValue.BAD: [],
			MoralValue.NEUTRAL: []
		}
		
		for philosopher, data in results.items():
			core_value = data['core']
			core_groups[core_value].append(f"  {philosopher:.<25}: {data['value_str']}")
		
		print(f"\n{'─'*80}")
		print("QUICK CONSENSUS:")
		print(f"{'─'*80}")
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
		
		print(f"\n{'─'*80}")
		print("DETAILED ANALYSIS:")
		print(f"{'─'*80}")
		
		for philosopher, data in results.items():
			print(f"\n{philosopher}:")
			print(f"  Verdict: {data['value_str']}")
			print(f"  Meaning: {data['quality']}")
			print(f"  Core: {data['core'].name}")
		
		# Optional: Show the core moral value mapping
		print(f"\n{'─'*80}")
		print("CORE MORAL VALUE MAPPING:")
		print(f"{'─'*80}")
		core_summary: dict = {}
		for philosopher, data in results.items():
			core_value = data['core']
			if core_value not in core_summary:
				core_summary[core_value] = []
			core_summary[core_value].append(philosopher)
		
		for core_value, philosophers in core_summary.items():
			print(f"{core_value.name}: {', '.join(philosophers)}")

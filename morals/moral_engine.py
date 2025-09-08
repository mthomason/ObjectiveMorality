#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

from .moral_context import MoralContext
from .moral_value import PhilosophicalMoralValue, AristotelianMoralValue, UtilitarianMoralValue

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
# Moral Engine Runner
# ------------------------------

class MoralEngineRunner:
	def run_engines(self, action: str, context: MoralContext):
		engines = {
			"Kantian": KantianEngine(),
			"Utilitarian": UtilitarianEngine(),
			"Aristotelian": AristotelianEngine(),
			"Contractualist": ContractualistEngine(),
		}
	
		results = {}
		for name, engine in engines.items():
			results[name] = str(engine.evaluate(action, context))
		return results

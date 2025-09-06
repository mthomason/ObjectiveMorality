#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

from .moral_context import MoralContext

# ------------------------------
# Base Class for Moral Engines
# ------------------------------

class MoralEngine:
	def evaluate(self, action: str, context: MoralContext):
		raise NotImplementedError("Each moral engine must implement evaluate()")

# ------------------------------
# Kantian Engine (Deontological)
# ------------------------------

class KantianEngine(MoralEngine):
	def evaluate(self, action, context):
		"""
		Action is wrong if universalizing it causes contradiction.
		"""
		if context.universalized_result.self_collapse:
			return "Impermissible"
		return "Permissible"

# ------------------------------
# Utilitarian Engine (Consequentialist)
# ------------------------------

class UtilitarianEngine(MoralEngine):
	def evaluate(self, action, context):
		"""
		Action is right if net flourishing > 0
		"""
		if context.consequences.net_flourishing > 0:
			return "Permissible"
		elif context.consequences.net_flourishing < 0:
			return "Impermissible"
		else:
			return "Neutral"

# ------------------------------
# Aristotelian Engine (Virtue Ethics)
# ------------------------------

class AristotelianEngine(MoralEngine):
	def evaluate(self, action, context):
		"""
		Action is virtuous if it aligns with flourishing life & stable character.
		Uses consequences + trust + social stability as proxies.
		"""
		if context.consequences.net_flourishing > 0 and context.cooperative_outcome.stable:
			return "Virtuous"
		elif context.consequences.net_flourishing < 0:
			return "Vicious"
		else:
			return "Contingent"

# ------------------------------
# Contractualist Engine
# ------------------------------

class ContractualistEngine(MoralEngine):
	def evaluate(self, action, context):
		"""
		Action is wrong if reasonable persons behind a veil of ignorance
		would reject the rule permitting it.
		"""
		if context.trust_impact.breach:
			return "Impermissible"
		return "Permissible"

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
			results[name] = engine.evaluate(action, context)
		return results

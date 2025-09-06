#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

class UniversalizedResult:
	def __init__(self, self_collapse: bool):
		self.self_collapse: bool = self_collapse

class Consequences:
	def __init__(self, net_flourishing: int):
		self.net_flourishing: int = net_flourishing

class CooperativeOutcome:
	def __init__(self, stable: bool):
		self.stable: bool = stable

class TrustImpact:
	def __init__(self, breach: bool):
		self.breach: bool = breach

class MoralContext:
	def __init__(
			self,
			universalized_result: UniversalizedResult,
			consequences: Consequences,
			cooperative_outcome: CooperativeOutcome,
			trust_impact: TrustImpact):
		self.universalized_result: UniversalizedResult = universalized_result
		self.consequences: Consequences = consequences
		self.cooperative_outcome: CooperativeOutcome = cooperative_outcome
		self.trust_impact: TrustImpact = trust_impact

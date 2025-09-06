#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .moral_engine import MoralEngineRunner
from .moral_context import MoralContext, TrustImpact, CooperativeOutcome, Consequences, UniversalizedResult
from pprint import pprint

def main():

	engine = MoralEngineRunner()

	# ------------------------------
	# Moral Case: Adultery
	# ------------------------------

	context_adultery = MoralContext(
		UniversalizedResult(self_collapse=True),
		Consequences(net_flourishing=-10),
		CooperativeOutcome(stable=False),
		TrustImpact(breach=True)
	)

	result_adultery = engine.run_engines("adultery", context_adultery)

	# ------------------------------
	# Moral Case: Pork Modern
	# ------------------------------

	context_pork_modern = MoralContext(
		UniversalizedResult(self_collapse=False),
		Consequences(net_flourishing=+5),
		CooperativeOutcome(stable=True),
		TrustImpact(breach=False)
	)

	result_pork_modern = engine.run_engines("pork_modern", context_pork_modern)

	# ------------------------------
	# Moral Case: Pork Premodern
	# ------------------------------

	context_pork_premodern = MoralContext(
		UniversalizedResult(self_collapse=False),
		Consequences(net_flourishing=-5),
		CooperativeOutcome(stable=True),
		TrustImpact(breach=False)
	)

	result_pork_premodern = engine.run_engines("pork_premodern", context_pork_premodern)

	print("Adultery")
	pprint(result_adultery)
	print("")

	print("Pork Modern")
	pprint(result_pork_modern)
	print("")


	print("Pork Premodern")
	pprint(result_pork_premodern)
	print("")

if __name__ == "__main__":
	main()

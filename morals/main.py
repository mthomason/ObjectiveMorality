#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .moral_engine import MoralEngineRunner
from pprint import pprint

def main():

	# ------------------------------
	# Moral Case: Adultery
	# ------------------------------

	context_adultery = {
		"universalized_result": {"self_collapse": True},
		"consequences": {"net_flourishing": -10},
		"cooperative_outcome": {"stable": False},
		"trust_impact": {"breach": True},
	}

	result_adultery = MoralEngineRunner.run_engines("adultery", context_adultery)

	# ------------------------------
	# Moral Case: Pork Modern
	# ------------------------------

	context_pork_modern = {
		"universalized_result": {"self_collapse": False},
		"consequences": {"net_flourishing": +5},			# healthy, nutritious
		"cooperative_outcome": {"stable": True},
		"trust_impact": {"breach": False},
	}

	result_pork_modern = MoralEngineRunner.run_engines("pork_modern", context_pork_modern)

	# ------------------------------
	# Moral Case: Pork Premodern
	# ------------------------------

	context_pork_premodern = {
		"universalized_result": {"self_collapse": False},  
		"consequences": {"net_flourishing": -5},			# illness, parasites
		"cooperative_outcome": {"stable": True},
		"trust_impact": {"breach": False},
	}

	result_pork_premodern = MoralEngineRunner.run_engines("pork_premodern", context_pork_premodern)

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

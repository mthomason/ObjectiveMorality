#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .moral_engine import MoralEngineRunner
from .moral_context import *
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

	# ------------------------------
	# Moral Case: Tell a Lie
	# ------------------------------

	context_lie = MoralContext(
		action_description="Lied to an inquiring official about a friend's whereabouts.",
	
		universalized_result=UniversalizedResult(
			self_collapse=True,
			contradiction_in_will=True
		),
		
		consequences=Consequences(
			net_flourishing=10,
			net_utility=15,
			individual_impact={"friend": 100, "society": -85},
			power_expression=-5
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=True, 
			societal_trust_change=-1
		),
		
		trust_impact=TrustImpact(
			breach=True,
			relationships_affected=["societal_trust"],
			impact_type=[RelationshipImpact.BREACHES_TRUST]
		),
		
		agent=Agent(
			agent_type=AgentType.FRIEND,
			virtues=[Virtue.LOYALTY, Virtue.COMPASSION],
			vices=[Vice.DISHONESTY]
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[DutyType.BENEFICENCE, DutyType.FIDELITY],
			duties_violated=[DutyType.NON_MALEFICENCE]
		)
	)

	result_tell_a_lie = engine.run_engines("tell_a_lie", context_lie)

	print("Adultery")
	pprint(result_adultery)
	print("")

	print("Pork Modern")
	pprint(result_pork_modern)
	print("")

	print("Pork Premodern")
	pprint(result_pork_premodern)
	print("")

	print("Tell a Lie")
	pprint(result_tell_a_lie)
	print("")

if __name__ == "__main__":
	main()

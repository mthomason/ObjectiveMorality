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
		action_description="Engaged in sexual relations with someone else's spouse.",
		universalized_result=UniversalizedResult(self_collapse=True, contradiction_in_will=True),
		consequences=Consequences(
			net_flourishing=-15,
			net_utility=-20,
			individual_impact={
				"betrayed_spouse": -50, 
				"community_trust": -30,
				"children": -40,
				"adulterer": +10 # short-term pleasure but long-term harm
			},
			power_expression=-5
		),
		cooperative_outcome=CooperativeOutcome(stable=False, societal_trust_change=-3),
		trust_impact=TrustImpact(
			breach=True,
			relationships_affected=["marriage", "family", "community_trust"],
			impact_type=[RelationshipImpact.BREACHES_TRUST, RelationshipImpact.WEAKENS]
		),
		agent=Agent(
			agent_type=AgentType.STRANGER,
			virtues=[],
			vices=[Vice.DISHONESTY, Vice.BETRAYAL, Vice.INDULGENCE]
		),
		duty_assessment=DutyAssessment(
			duties_upheld=[],
			duties_violated=[DutyType.FIDELITY, DutyType.NON_MALEFICENCE]
		)
	)

	result_adultery = engine.run_engines("adultery", context_adultery)

	# ------------------------------
	# Moral Case: Pork Modern
	# ------------------------------

	context_pork_modern = MoralContext(
		action_description="Ate properly cooked pork from a regulated source.",
		
		universalized_result=UniversalizedResult(
			self_collapse=False,
			contradiction_in_will=False
		),
		
		consequences=Consequences(
			net_flourishing=+8,
			net_utility=+10,
			individual_impact={
				"eater": +15,  # nutrition and pleasure
				"farmer": +5,   # economic benefit
				"society": 0	# no significant impact
			},
			power_expression=+2  # exercising personal choice
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=True,
			societal_trust_change=0
		),
		
		trust_impact=TrustImpact(
			breach=False,
			relationships_affected=[],
			impact_type=[]
		),
		
		agent=Agent(
			agent_type=AgentType.STRANGER,
			virtues=[Virtue.TEMPERANCE],  # eating in moderation
			vices=[]
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[DutyType.SELF_IMPROVEMENT],  # maintaining health
			duties_violated=[]
		)
	)

	result_pork_modern = engine.run_engines("pork_modern", context_pork_modern)

	# ------------------------------
	# Moral Case: Pork Premodern
	# ------------------------------

	context_pork_premodern = MoralContext(
		action_description="Ate undercooked pork from an unregulated source in a context with known parasites.",
		
		universalized_result=UniversalizedResult(
			self_collapse=False,
			contradiction_in_will=False
		),
		
		consequences=Consequences(
			net_flourishing=-12,
			net_utility=-15,
			individual_impact={
				"eater": -20,  # illness and suffering
				"family": -10,  # burden of care
				"community": -5 # potential spread of illness
			},
			power_expression=-3  # poor judgment leading to harm
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=True,  # the social contract itself isn't threatened
			societal_trust_change=0
		),
		
		trust_impact=TrustImpact(
			breach=False,
			relationships_affected=[],
			impact_type=[]
		),
		
		agent=Agent(
			agent_type=AgentType.STRANGER,
			virtues=[],
			vices=[Vice.FOOLISHNESS]  # poor judgment about food safety
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[],
			duties_violated=[DutyType.SELF_IMPROVEMENT]  # failing to maintain health
		)
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

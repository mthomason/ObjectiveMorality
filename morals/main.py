#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .moral_engine import MoralEngineRunner
from .moral_context import *
from pprint import pprint

def main():

	engine_runner = MoralEngineRunner()

	# ------------------------------
	# Moral Case: Adultery
	# ------------------------------

	context_adultery = MoralContext(
		action_description="Engaged in sexual relations with someone else's spouse.",
		universalized_result=UniversalizedResult(self_collapse=True, contradiction_in_will=True),
		consequences=Consequences(
			net_flourishing=-15,
			net_utility=-20,
			time_horizon=TimeHorizon.LONG,
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

	result_adultery = engine_runner.run_engines("adultery", context_adultery)

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
			time_horizon=TimeHorizon.MEDIUM,
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

	result_pork_modern = engine_runner.run_engines("pork_modern", context_pork_modern)

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
			time_horizon=TimeHorizon.MEDIUM,
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

	result_pork_premodern = engine_runner.run_engines("pork_premodern", context_pork_premodern)

	# ------------------------------
	# Moral Case: Tell a Lie
	# ------------------------------

	context_lie = MoralContext(
		action_description="Lied to an inquiring official about a friend's whereabouts to protect them from potential harm.",
		
		universalized_result=UniversalizedResult(
			self_collapse=True,
			contradiction_in_will=True
		),
		
		consequences=Consequences(
			net_flourishing=10,
			net_utility=15,
			individual_impact={
				"friend": 100,		# protected from potential harm
				"society": -15,		# minor erosion of trust (not -85, too severe for a single lie)
				"official": -5,		# wasted time/resources
				"oneself": +5		# maintained friendship integrity, but with moral discomfort
			},
			power_expression=-2	 # slightly negative - deception isn't typically power-affirming
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=True, 
			societal_trust_change=-1  # small negative impact on general trust
		),
		
		trust_impact=TrustImpact(
			breach=True,
			relationships_affected=["societal_trust", "friendship", "official_citizen_trust"],
			impact_type=[
				RelationshipImpact.BREACHES_TRUST,		# to society/official
				RelationshipImpact.STRENGTHENS,			# to friend
				RelationshipImpact.NURTURES				# the friendship
			]
		),
		
		agent=Agent(
			agent_type=AgentType.FRIEND,
			virtues=[Virtue.LOYALTY, Virtue.COMPASSION, Virtue.COURAGE],  # added courage
			vices=[Vice.DISHONESTY]
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[
				DutyType.BENEFICENCE,
				DutyType.FIDELITY,
			],
			duties_violated=[
				DutyType.FIDELITY,
				DutyType.NON_MALEFICENCE
			]
		)
	)

	result_tell_a_lie = engine_runner.run_engines("tell_a_lie", context_lie)

	# ------------------------------
	# Moral Case: Charity
	# ------------------------------

	context_charity = MoralContext(
		action_description="Donated a significant portion of income to effective charities helping the global poor.",
		
		universalized_result=UniversalizedResult(
			self_collapse=False,		# World where everyone donates would be better
			contradiction_in_will=False	# Rational beings would will this
		),
		
		consequences=Consequences(
			net_flourishing=+25,
			net_utility=+30,
			time_horizon=TimeHorizon.LONG,
			individual_impact={
				"recipients": +80,		# life-changing benefits
				"donor": -10,			# personal sacrifice
				"society": +5			# positive externalities
			},
			power_expression=+3			# exercising virtue and generosity
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=True,
			societal_trust_change=+2	# strengthens social fabric
		),
		
		trust_impact=TrustImpact(
			breach=False,
			relationships_affected=["global_community", "donor_recipient"],
			impact_type=[
				RelationshipImpact.BUILDS_TRUST,
				RelationshipImpact.NURTURES,
				RelationshipImpact.STRENGTHENS
			]
		),
		
		agent=Agent(
			agent_type=AgentType.STRANGER,		# helping distant others
			virtues=[Virtue.COMPASSION, Virtue.JUSTICE, Virtue.TEMPERANCE],
			vices=[]							# no vices in charitable giving
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[
				DutyType.BENEFICENCE,
				DutyType.JUSTICE,
				DutyType.GRATITUDE  # if one feels grateful for their position
			],
			duties_violated=[]  # no duties violated
		)
	)
	result_charity = engine_runner.run_engines("charitable_donation", context_charity)

	# ------------------------------
	# Moral Case: Mass Surveillance
	# ------------------------------

	context_mass_surveillance = MoralContext(
		action_description="Implemented mass surveillance program collecting data on all citizens without individualized warrants, justified by national security claims.",
		
		universalized_result=UniversalizedResult(
			self_collapse=True,				# If everyone spied on everyone, society collapses
			contradiction_in_will=True		# No rational being would will a world without privacy
		),
		
		consequences=Consequences(
			net_flourishing=-15,			# Chilling effect on free expression, self-censorship
			net_utility=-5,					# Mixed: some security benefits vs massive privacy costs
			time_horizon=TimeHorizon.LONG,
			individual_impact={
				"citizens": -30,			# Loss of privacy, autonomy, trust
				"government": +10,			# Increased perceived security, power
				"dissidents": -50,			# Targeted repression, fear
				"criminals": -5				# Some prevention, but many evade
			},
			power_expression=+8				# Massive state power increase
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=False,				 # Erodes social trust, creates paranoid society
			societal_trust_change=-20	 # Severe damage to citizen-government trust
		),
		
		trust_impact=TrustImpact(
			breach=True,
			relationships_affected=["citizen_state", "social_fabric", "international_trust"],
			impact_type=[
				RelationshipImpact.BREACHES_TRUST,
				RelationshipImpact.EXPLOITS,
				RelationshipImpact.WEAKENS
			]
		),
		
		agent=Agent(
			agent_type=AgentType.STATE_OFFICIAL,
			virtues=[Virtue.JUSTICE],								# Claimed intention to protect
			vices=[Vice.DISHONESTY, Vice.UNFAIRNESS, Vice.CRUELTY]	# Deception, inequality, potential repression
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[
				DutyType.BENEFICENCE,		# Claimed protection of public safety
				DutyType.JUSTICE			# Claimed protection of social order
			],
			duties_violated=[
				DutyType.FIDELITY,			# Breach of social contract
				DutyType.NON_MALEFICENCE,	# Harms privacy, autonomy, trust
				DutyType.JUSTICE			# Violates due process, equal protection
			]
		)
	)
	result_mass_surveillance = engine_runner.run_engines("mass_surveillance", context_mass_surveillance)

	engine_runner.display_results("adultery", result_adultery)
	engine_runner.display_results("pork_modern", result_pork_modern)
	engine_runner.display_results("pork_premodern", result_pork_premodern)
	engine_runner.display_results("tell_a_lie", result_tell_a_lie)
	engine_runner.display_results("charitable_donation", result_charity)
	engine_runner.display_results("mass_surveillance", result_mass_surveillance)
	print("")

if __name__ == "__main__":
	main()

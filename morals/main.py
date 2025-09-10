#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Michael Thomason <mthomason@gmail.com>
# Copyright (C) 2025 Michael Thomason, All rights reserved.
# With hope and prayer I release this into the public domain.
# I claim copyright, only to ensure its release into the public domain.

# -----------------------------------------------------------------------------
# Included moral cases: Adultery, Pork (modern and historical), lying, charity
#	mass surveillance, and two trolley problems (switch and fat man).
# -----------------------------------------------------------------------------

from .moral_engine import MoralEngineRunner
from .moral_context import *
from .moral_json import MoralContextManager
from pprint import pprint

def main():

	engine_runner = MoralEngineRunner()
	context_manager = MoralContextManager()

	# ------------------------------
	# Moral Case: Adultery
	# This example shows how to create the moral context in code, but it's
	#	also saved and loaded from a JSON file.  This can be done for all
	#	examples.  But, I'm leaving the existing context in code, to
	#	demonstrate how it's done, and because the comments are useful.
	# ------------------------------

	if not context_manager.context_exists("adultery"):
		context_adultery = MoralContext(
			action_description="Engaged in sexual relations with someone else's spouse.",
			universalized_result=UniversalizedResult(self_collapse=True, contradiction_in_will=True),
			consequences=Consequences(
				net_flourishing=-15,
				net_utility=-20,
				time_horizon=TimeHorizon.LONG,
				individual_impact={
					ImpactSubject.BETRAYED_SPOUSE: -50, 
					ImpactSubject.COMMUNITY: -30,
					ImpactSubject.CHILD: -40,
					ImpactSubject.AGENT: +10 # short-term pleasure but long-term harm
				},
				power_expression=-5
			),
			cooperative_outcome=CooperativeOutcome(stable=False, societal_trust_change=-3),
			trust_impact=TrustImpact(
				breach=True,
				relationships_affected=[RelationshipType.SPOUSE_SPOUSE, RelationshipType.FAMILY_MEMBER, RelationshipType.CITIZEN_STATE],
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
		context_manager.save_context(context_adultery, "adultery") # This is how to write to JSON
	
	context_adultery = context_manager.load_context("adultery")	# This is the only example read from JSON
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
				ImpactSubject.EATER: +15,	# nutrition and pleasure
				ImpactSubject.FARMER: +5,	# economic benefit
				ImpactSubject.SOCIETY: 0	# no significant impact
			},
			power_expression=+2	# exercising personal choice
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
			virtues=[Virtue.TEMPERANCE],				# eating in moderation
			vices=[]
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[DutyType.SELF_IMPROVEMENT],	# maintaining health
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
				ImpactSubject.EATER: -20,  # illness and suffering
				ImpactSubject.FAMILY_MEMBER: -10,  # burden of care
				ImpactSubject.COMMUNITY: -5 # potential spread of illness
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
				ImpactSubject.FRIEND: 100,		# protected from potential harm
				ImpactSubject.SOCIETY: -15,		# minor erosion of trust (not -85, too severe for a single lie)
				ImpactSubject.OFFICIAL: -5,		# wasted time/resources
				ImpactSubject.AGENT: +5			# maintained friendship integrity, but with moral discomfort
			},
			power_expression=-2	 # slightly negative - deception isn't typically power-affirming
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=True, 
			societal_trust_change=-1  # small negative impact on general trust
		),
		
		trust_impact=TrustImpact(
			breach=True,
			relationships_affected=[RelationshipType.CITIZEN_STATE, RelationshipType.FRIEND_FRIEND, RelationshipType.CITIZEN_STATE],
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
				ImpactSubject.RECIPIENT: +80,		# life-changing benefits
				ImpactSubject.DONOR: -10,			# personal sacrifice
				ImpactSubject.SOCIETY: +5			# positive externalities
			},
			power_expression=+3			# exercising virtue and generosity
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=True,
			societal_trust_change=+2	# strengthens social fabric
		),
		
		trust_impact=TrustImpact(
			breach=False,
			relationships_affected=[RelationshipType.HUMAN_HUMAN, RelationshipType.CAREGIVER_RECEIVER],
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
				ImpactSubject.CITIZENS: -30,	# Loss of privacy, autonomy, trust
				ImpactSubject.GOVERNMENT: +10,	# Increased perceived security, power
				ImpactSubject.DISSIDENT: -50,	# Targeted repression, fear
				ImpactSubject.CRIMINAL: -5		# Some prevention, but many evade
			},
			power_expression=+8				# Massive state power increase
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=False,				 # Erodes social trust, creates paranoid society
			societal_trust_change=-20	 # Severe damage to citizen-government trust
		),
		
		trust_impact=TrustImpact(
			breach=True,
			relationships_affected=[RelationshipType.CITIZEN_STATE, RelationshipType.COMMUNITY_MEMBER, RelationshipType.HUMAN_HUMAN],
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

	# ------------------------------
	# Moral Case: Trolley Problem - Switch Variant
	# ------------------------------

	context_trolley_switch = MoralContext(
		action_description="Pulled a lever to divert a runaway trolley onto a side track, resulting in one death but saving five people.",
		
		universalized_result=UniversalizedResult(
			self_collapse=False,			# Universalizing minimizing harm doesn't cause contradiction
			contradiction_in_will=False
		),
		
		consequences=Consequences(
			net_flourishing=+4,				# 5 lives saved - 1 life lost = +4
			net_utility=+4,
			time_horizon=TimeHorizon.LONG,
			individual_impact={
				ImpactSubject.SAVED_PEOPLE: +5,
				ImpactSubject.STRANGER: -1,
				ImpactSubject.AGENT: -2		# Emotional burden
			},
			power_expression=+3				# Taking control of situation
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=True,
			societal_trust_change=0			# No direct impact on social trust
		),
		
		trust_impact=TrustImpact(
			breach=False,
			relationships_affected=[],
			impact_type=[]
		),
		
		agent=Agent(
			agent_type=AgentType.STRANGER,
			virtues=[Virtue.COURAGE, Virtue.JUSTICE],
			vices=[]
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[
				DutyType.BENEFICENCE,		# Saving lives
				DutyType.JUSTICE			# Minimizing overall harm
			],
			duties_violated=[
				DutyType.NON_MALEFICENCE	# Causing one death
			]
		)
	)

	result_trolley_switch = engine_runner.run_engines("trolley_switch", context_trolley_switch)

	# ------------------------------
	# Moral Case: Trolley Problem - Fat Man Variant
	# ------------------------------

	context_trolley_fat_man = MoralContext(
		action_description="Pushed a large person off a bridge to stop a runaway trolley, resulting in their death but saving five people.",
		
		universalized_result=UniversalizedResult(
			self_collapse=True,				# Universalizing killing innocent people causes contradiction
			contradiction_in_will=True		# No rational being would will this
		),
		
		consequences=Consequences(
			net_flourishing=+4,				# Same net utility as switch variant
			net_utility=+4,
			time_horizon=TimeHorizon.LONG,
			individual_impact={
				ImpactSubject.SAVED_PEOPLE: +5,
				ImpactSubject.STRANGER: -1,
				ImpactSubject.AGENT: -5		# Greater emotional burden (more direct involvement)
			},
			power_expression=-2				# Using someone as mere means
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=False,
			societal_trust_change=-3		# Erodes trust in public safety
		),
		
		trust_impact=TrustImpact(
			breach=True,
			relationships_affected=[RelationshipType.COMMUNITY_MEMBER],
			impact_type=[RelationshipImpact.BREACHES_TRUST, RelationshipImpact.WEAKENS]
		),
		
		agent=Agent(
			agent_type=AgentType.STRANGER,
			virtues=[Virtue.JUSTICE],		# Trying to minimize harm
			vices=[Vice.CRUELTY]			# Directly causing harm
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[
				DutyType.BENEFICENCE		# Saving lives
			],
			duties_violated=[
				DutyType.NON_MALEFICENCE,	# Directly killing someone
				DutyType.JUSTICE			# Using someone as mere means
			]
		)
	)

	result_trolley_fat_man = engine_runner.run_engines("trolley_fat_man", context_trolley_fat_man)

	# ------------------------------
	# Moral Case: Suicide
	# ------------------------------

	context_suicide = MoralContext(
		action_description="A person intentionally ends their own life to escape unbearable suffering.",
		
		universalized_result=UniversalizedResult(
			self_collapse=True,          # Universal suicide would lead to human extinction
			contradiction_in_will=True   # Rational beings wouldn't will their own non-existence
		),
		
		consequences=Consequences(
			net_flourishing=-20,
			net_utility=-15,
			time_horizon=TimeHorizon.LONG,
			individual_impact={
				ImpactSubject.AGENT: -100,           # Complete loss of flourishing
				ImpactSubject.FAMILY_MEMBER: -40,    # Profound grief and trauma
				ImpactSubject.FRIEND: -30,           # Loss and emotional pain
				ImpactSubject.COMMUNITY: -10,        # Social fabric weakened
				ImpactSubject.SOCIETY: -5            # Loss of potential contribution
			},
			power_expression=-8          # Ultimate loss of agency and self-mastery
		),
		
		cooperative_outcome=CooperativeOutcome(
			stable=False,
			societal_trust_change=-2     # Undermines social commitment to life preservation
		),
		
		trust_impact=TrustImpact(
			breach=True,
			relationships_affected=[
				RelationshipType.FAMILY_MEMBER,
				RelationshipType.FRIEND_FRIEND,
				RelationshipType.COMMUNITY_MEMBER,
				RelationshipType.HUMAN_HUMAN
			],
			impact_type=[
				RelationshipImpact.BREACHES_TRUST,  # Breach of implicit social contract
				RelationshipImpact.WEAKENS,         # Weakens family and community bonds
				RelationshipImpact.EXPLOITS         # Exploits relationships by transferring pain
			]
		),
		
		agent=Agent(
			agent_type=AgentType.STRANGER,
			virtues=[Virtue.COURAGE],    # Some might see courage in facing death
			vices=[
				Vice.DESPAIR,            # Overwhelming hopelessness
				Vice.SELFISHNESS,        # Putting own suffering above others' needs
				Vice.COWARDICE           # Fleeing from life's challenges (from some perspectives)
			]
		),
		
		duty_assessment=DutyAssessment(
			duties_upheld=[
				# Some might argue it upholds self-determination
			],
			duties_violated=[
				DutyType.NON_MALEFICENCE,    # Harm to self
				DutyType.BENEFICENCE,        # Failure to continue potential good works
				DutyType.FIDELITY,           # Breaking implicit promises to loved ones
				DutyType.GRATITUDE,          # Failing to appreciate gift of life
				DutyType.SELF_IMPROVEMENT    # Ending rather than improving self
			]
		)
	)

	result_suicide = engine_runner.run_engines("suicide", context_suicide)

	engine_runner.display_results("adultery", context_adultery, result_adultery)
	engine_runner.display_results("pork_modern", context_pork_modern, result_pork_modern)
	engine_runner.display_results("pork_premodern", context_pork_premodern, result_pork_premodern)
	engine_runner.display_results("tell_a_lie", context_lie, result_tell_a_lie)
	engine_runner.display_results("charitable_donation", context_charity, result_charity)
	engine_runner.display_results("mass_surveillance", context_mass_surveillance, result_mass_surveillance)
	engine_runner.display_results("trolley_switch", context_trolley_switch, result_trolley_switch)
	engine_runner.display_results("trolley_fat_man", context_trolley_fat_man, result_trolley_fat_man)
	engine_runner.display_results("suicide", context_suicide, result_suicide)
	engine_runner.display_consistency_report()

if __name__ == "__main__":
	main()

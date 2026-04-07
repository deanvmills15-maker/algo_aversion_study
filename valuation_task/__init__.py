from otree.api import *

doc = """
Valuation task: participants state their maximum willingness-to-pay for
professional investment advice (Human Wealth Manager or AI Advisor) across
5 rounds. Switch point is elicited via a multiple price list (prices $1-$10).
"""


class C(BaseConstants):
    NAME_IN_URL = 'valuation_task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5

    PRICES = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Alternate advisor type by round number
    ADVISOR_BY_ROUND = {
        1: 'Human Wealth Manager',
        2: 'AI Advisor',
        3: 'Human Wealth Manager',
        4: 'AI Advisor',
        5: 'Human Wealth Manager',
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    switch_point = models.IntegerField(
        label='',
        min=1,
        max=10,
    )


class Valuation(Page):
    form_model = 'player'
    form_fields = ['switch_point']

    @staticmethod
    def vars_for_template(player: Player):
        advisor_type = C.ADVISOR_BY_ROUND[player.round_number]
        return dict(
            prices=C.PRICES,
            advisor_type=advisor_type,
        )


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        advisor_type = C.ADVISOR_BY_ROUND[player.round_number]
        return dict(advisor_type=advisor_type)


page_sequence = [Valuation, Results]

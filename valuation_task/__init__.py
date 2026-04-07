from otree.api import *

doc = """
Valuation task: participants state their maximum willingness-to-pay for
professional investment advice (Human Wealth Manager or AI Advisor) across
5 rounds. Switch point is elicited via a multiple price list (prices $1-$10).
Portfolio construction screen collects 5-asset allocation (shown in round 1 only).
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
        min=0,   # 0 = unwilling to pay even $1 for advice
        max=10,
    )

    # 5-asset portfolio allocation (integers, must sum to 100)
    alloc_tbills  = models.IntegerField(initial=20, min=0, max=100, label='T-Bills')
    alloc_index   = models.IntegerField(initial=20, min=0, max=100, label='Index Fund')
    alloc_reits   = models.IntegerField(initial=20, min=0, max=100, label='REITs')
    alloc_stocks  = models.IntegerField(initial=20, min=0, max=100, label='Individual Stocks')
    alloc_crypto  = models.IntegerField(initial=20, min=0, max=100, label='Cryptocurrency')


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


class PortfolioConstruction(Page):
    form_model = 'player'
    form_fields = ['alloc_tbills', 'alloc_index', 'alloc_reits', 'alloc_stocks', 'alloc_crypto']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        fields = ['alloc_tbills', 'alloc_index', 'alloc_reits', 'alloc_stocks', 'alloc_crypto']
        total = sum(values[f] for f in fields)
        print(
            f"[PortfolioConstruction] submitted sum={total} | "
            + " | ".join(f"{f}={values[f]}" for f in fields)
        )
        if total != 100:
            return f'Your allocations sum to {total}%. Please adjust the sliders so they total exactly 100%.'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        advisor_type = C.ADVISOR_BY_ROUND[player.round_number]
        return dict(advisor_type=advisor_type)


page_sequence = [PortfolioConstruction, Valuation, Results]

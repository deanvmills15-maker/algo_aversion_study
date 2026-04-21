import random
from otree.api import *

doc = """
Valuation task: participants state their maximum willingness-to-pay for
professional investment advice (Human Wealth Manager or AI Advisor) across
2 rounds (one per advisor type). Switch point is elicited via a multiple
price list (prices $1-$10). Portfolio construction screen collects 5-asset
allocation (shown in round 1 only). Belief elicitation collects 20-token
histogram beliefs over 7 return bins for both advisors (timing controlled
by timing_group).
"""


class C(BaseConstants):
    NAME_IN_URL = 'valuation_task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    PRICES = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    TOTAL_TOKENS = 20

    BIN_LABELS = [
        '< −25%',
        '−25% to −15%',
        '−15% to −5%',
        '−5% to +5%',
        '+5% to +15%',
        '+15% to +25%',
        '> +25%',
    ]


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    for player in subsession.get_players():
        if 'timing_group' not in player.participant.vars:
            player.participant.vars['timing_group'] = random.choice(['before', 'after'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    switch_point_human = models.IntegerField(label='', min=0, max=10)
    switch_point_ai    = models.IntegerField(label='', min=0, max=10)

    # Portfolio allocation (sums to 100)
    alloc_tbills  = models.IntegerField(initial=20, min=0, max=100, label='T-Bills')
    alloc_index   = models.IntegerField(initial=20, min=0, max=100, label='Index Fund')
    alloc_reits   = models.IntegerField(initial=20, min=0, max=100, label='REITs')
    alloc_stocks  = models.IntegerField(initial=20, min=0, max=100, label='Individual Stocks')
    alloc_crypto  = models.IntegerField(initial=20, min=0, max=100, label='Cryptocurrency')

    # Belief elicitation — Human Wealth Manager (7 bins, each 0–20, sum = 20)
    h_bin1 = models.IntegerField(initial=0, min=0, max=20, label='Human Bin 1')
    h_bin2 = models.IntegerField(initial=0, min=0, max=20, label='Human Bin 2')
    h_bin3 = models.IntegerField(initial=0, min=0, max=20, label='Human Bin 3')
    h_bin4 = models.IntegerField(initial=0, min=0, max=20, label='Human Bin 4')
    h_bin5 = models.IntegerField(initial=0, min=0, max=20, label='Human Bin 5')
    h_bin6 = models.IntegerField(initial=0, min=0, max=20, label='Human Bin 6')
    h_bin7 = models.IntegerField(initial=0, min=0, max=20, label='Human Bin 7')

    # Belief elicitation — AI Advisor (7 bins, each 0–20, sum = 20)
    a_bin1 = models.IntegerField(initial=0, min=0, max=20, label='AI Bin 1')
    a_bin2 = models.IntegerField(initial=0, min=0, max=20, label='AI Bin 2')
    a_bin3 = models.IntegerField(initial=0, min=0, max=20, label='AI Bin 3')
    a_bin4 = models.IntegerField(initial=0, min=0, max=20, label='AI Bin 4')
    a_bin5 = models.IntegerField(initial=0, min=0, max=20, label='AI Bin 5')
    a_bin6 = models.IntegerField(initial=0, min=0, max=20, label='AI Bin 6')
    a_bin7 = models.IntegerField(initial=0, min=0, max=20, label='AI Bin 7')


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
        if total != 100:
            return f'Allocations sum to {total}%. Please adjust sliders to total exactly 100%.'


class BeliefElicitation(Page):
    form_model = 'player'
    form_fields = [
        'h_bin1', 'h_bin2', 'h_bin3', 'h_bin4', 'h_bin5', 'h_bin6', 'h_bin7',
        'a_bin1', 'a_bin2', 'a_bin3', 'a_bin4', 'a_bin5', 'a_bin6', 'a_bin7',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars.get('timing_group') == 'after'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            bin_labels=C.BIN_LABELS,
            total_tokens=C.TOTAL_TOKENS,
        )

    @staticmethod
    def error_message(player: Player, values):
        h_total = sum(values[f'h_bin{i}'] for i in range(1, 8))
        a_total = sum(values[f'a_bin{i}'] for i in range(1, 8))
        if h_total != 20:
            return f'Human Wealth Manager tokens sum to {h_total}. Please use all 20 tokens.'
        if a_total != 20:
            return f'AI Advisor tokens sum to {a_total}. Please use all 20 tokens.'


class ValuationHuman(Page):
    template_name = 'valuation_task/Valuation.html'
    form_model = 'player'
    form_fields = ['switch_point_human']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(prices=C.PRICES, advisor_type='Human Wealth Manager',
                    field_name='switch_point_human', advisor_num=1)


class ValuationAI(Page):
    template_name = 'valuation_task/Valuation.html'
    form_model = 'player'
    form_fields = ['switch_point_ai']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(prices=C.PRICES, advisor_type='AI Advisor',
                    field_name='switch_point_ai', advisor_num=2)


page_sequence = [PortfolioConstruction, ValuationHuman, ValuationAI, BeliefElicitation]

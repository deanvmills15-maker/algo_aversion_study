from otree.api import *

doc = """
Valuation task: participants state their maximum willingness-to-pay for
professional investment advice (Human Wealth Manager or AI Advisor) across
5 rounds. Switch point is elicited via a multiple price list (prices $1-$10).
Portfolio construction screen collects 5-asset allocation (shown in round 1 only).
Belief elicitation collects 20-token histogram beliefs over 7 return bins for
both Human Wealth Manager and AI Advisor (shown in round 1 only).
"""


class C(BaseConstants):
    NAME_IN_URL = 'valuation_task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5

    PRICES = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    ADVISOR_BY_ROUND = {
        1: 'Human Wealth Manager',
        2: 'AI Advisor',
        3: 'Human Wealth Manager',
        4: 'AI Advisor',
        5: 'Human Wealth Manager',
    }

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


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    switch_point = models.IntegerField(label='', min=0, max=10)

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
        print(
            f"[PortfolioConstruction] sum={total} | "
            + " | ".join(f"{f}={values[f]}" for f in fields)
        )
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
        return player.round_number == 1

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
        print(f"[BeliefElicitation] h_total={h_total}, a_total={a_total}")
        if h_total != 20:
            return f'Human Wealth Manager tokens sum to {h_total}. Please use all 20 tokens.'
        if a_total != 20:
            return f'AI Advisor tokens sum to {a_total}. Please use all 20 tokens.'


class Valuation(Page):
    form_model = 'player'
    form_fields = ['switch_point']

    @staticmethod
    def vars_for_template(player: Player):
        advisor_type = C.ADVISOR_BY_ROUND[player.round_number]
        return dict(prices=C.PRICES, advisor_type=advisor_type)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        advisor_type = C.ADVISOR_BY_ROUND[player.round_number]
        return dict(advisor_type=advisor_type)


page_sequence = [PortfolioConstruction, BeliefElicitation, Valuation, Results]

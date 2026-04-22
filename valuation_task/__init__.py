import math
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
        if 'beliefs_before' not in player.participant.vars:
            player.participant.vars['beliefs_before'] = random.choice([True, False])


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
        return player.participant.vars.get('beliefs_before') is False

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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['beliefs_timing'] = 'after'
        for i in range(1, 8):
            player.participant.vars[f'h_bin{i}'] = getattr(player, f'h_bin{i}')
            player.participant.vars[f'a_bin{i}'] = getattr(player, f'a_bin{i}')


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


_ACTUAL_DISTS = {
    'human': [0.03, 0.07, 0.15, 0.22, 0.28, 0.18, 0.07],
    'ai':    [0.05, 0.08, 0.12, 0.18, 0.25, 0.20, 0.12],
}
_BIN_RANGES = [(-50,-25), (-25,-15), (-15,-5), (-5,5), (5,15), (15,25), (25,60)]
_GAMBLE_MAX = 42   # max raw gamble outcome (option 5A = $42)
_NOTIONAL   = 50000
_SCALE      = 10000  # $10,000 notional = $1 real


class Payout(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if 'payout_data' in player.participant.vars:
            return player.participant.vars['payout_data']

        # ── Component 1: Gamble 50/50 draw ──
        gamble_choice = player.participant.vars.get('gamble_choice', 1)
        gamble_a      = player.participant.vars.get('gamble_a', 10)
        gamble_b      = player.participant.vars.get('gamble_b', 10)
        gamble_result = random.choice(['A', 'B'])
        gamble_raw    = gamble_a if gamble_result == 'A' else gamble_b
        gamble_payout = round(gamble_raw * 5 / _GAMBLE_MAX, 2)

        # ── Component 2: Portfolio performance ──
        selected_advisor = random.choice(['human', 'ai'])
        selected_fee     = random.randint(1, 10)
        sw           = player.switch_point_human if selected_advisor == 'human' else player.switch_point_ai
        advisor_label = 'Human Wealth Manager' if selected_advisor == 'human' else 'AI Advisor'
        uses_advisor  = (selected_fee <= sw)
        actual_dist   = _ACTUAL_DISTS[selected_advisor]

        if uses_advisor:
            bin_idx = random.choices(range(7), weights=actual_dist)[0]
            lo, hi  = _BIN_RANGES[bin_idx]
            simulated_return = round(random.uniform(lo, hi), 1)
        else:
            mus   = [4,  8,  7, 12, 15]
            sigs  = [2, 12, 18, 28, 55]
            allocs = [player.alloc_tbills, player.alloc_index, player.alloc_reits,
                      player.alloc_stocks, player.alloc_crypto]
            mu  = sum(a/100 * m for a, m in zip(allocs, mus))
            sig = math.sqrt(sum((a/100)**2 * s**2 for a, s in zip(allocs, sigs)))
            simulated_return = round(random.gauss(mu, sig), 1)

        notional_gain    = _NOTIONAL * simulated_return / 100
        portfolio_base   = notional_gain / _SCALE        # 5 * return/100, max $5
        portfolio_payout = round(portfolio_base - (selected_fee if uses_advisor else 0), 2)

        # ── Component 3: Belief scoring (quadratic) ──
        h_bins = [player.participant.vars.get(f'h_bin{i}', getattr(player, f'h_bin{i}', 0))
                  for i in range(1, 8)]
        a_bins = [player.participant.vars.get(f'a_bin{i}', getattr(player, f'a_bin{i}', 0))
                  for i in range(1, 8)]
        participant_bins = h_bins if selected_advisor == 'human' else a_bins
        total_tokens     = sum(participant_bins) or 1
        participant_probs = [b / total_tokens for b in participant_bins]

        belief_score  = max(0.0, 1.0 - sum(
            (actual_dist[i] - participant_probs[i])**2 for i in range(7)))
        belief_payout = round(belief_score * 5, 2)

        # ── Total ──
        variable_raw      = gamble_payout + portfolio_payout + belief_payout
        performance_payout = round(max(0.0, variable_raw), 2)
        total_payout       = round(5.00 + performance_payout, 2)

        # Pre-format display strings (handles negatives cleanly)
        def fmt(v):
            return f'+${v:.2f}' if v >= 0 else f'−${abs(v):.2f}'

        data = dict(
            # Component 1
            gamble_choice=gamble_choice,
            gamble_a=gamble_a,
            gamble_b=gamble_b,
            gamble_a_display=f'${gamble_a}' if gamble_a >= 0 else f'−${abs(gamble_a)}',
            gamble_b_display=f'${gamble_b}' if gamble_b >= 0 else f'−${abs(gamble_b)}',
            gamble_result=gamble_result,
            gamble_raw=gamble_raw,
            gamble_payout=gamble_payout,
            gamble_payout_display=fmt(gamble_payout),
            # Component 2
            selected_advisor=selected_advisor,
            advisor_label=advisor_label,
            selected_fee=selected_fee,
            switch_point=sw,
            uses_advisor=uses_advisor,
            simulated_return=simulated_return,
            portfolio_payout=portfolio_payout,
            portfolio_payout_display=fmt(portfolio_payout),
            notional_gain=round(notional_gain),
            # Component 3
            actual_dist=actual_dist,
            participant_probs=[round(p, 4) for p in participant_probs],
            beliefs_timing=player.participant.vars.get('beliefs_timing', 'unknown'),
            belief_score=round(belief_score, 3),
            belief_payout=belief_payout,
            # Total
            variable_raw=round(variable_raw, 2),
            variable_raw_display=fmt(round(variable_raw, 2)),
            performance_payout=performance_payout,
            total_payout=total_payout,
        )

        player.participant.vars['payout_data'] = data
        return data


page_sequence = [PortfolioConstruction, ValuationHuman, ValuationAI, BeliefElicitation, Payout]

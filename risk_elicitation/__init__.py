import random
import string
from datetime import datetime
from otree.api import *

doc = """
Eckel-Grossman risk elicitation. Participants choose one of 5 investment options
with 50/50 payoffs. Choice stored as gamble_choice (1-5).
"""


class C(BaseConstants):
    NAME_IN_URL = 'risk_elicitation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    GAMBLES = [
        {'num': 1, 'a': 10, 'b': 10},
        {'num': 2, 'a': 18, 'b': 6},
        {'num': 3, 'a': 26, 'b': 2},
        {'num': 4, 'a': 34, 'b': -2},
        {'num': 5, 'a': 42, 'b': -6},
    ]

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
    gamble_choice = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        label='',
    )

    # Belief elicitation — Human Wealth Manager
    h_bin1 = models.IntegerField(initial=0)
    h_bin2 = models.IntegerField(initial=0)
    h_bin3 = models.IntegerField(initial=0)
    h_bin4 = models.IntegerField(initial=0)
    h_bin5 = models.IntegerField(initial=0)
    h_bin6 = models.IntegerField(initial=0)
    h_bin7 = models.IntegerField(initial=0)

    # Belief elicitation — AI Advisor
    a_bin1 = models.IntegerField(initial=0)
    a_bin2 = models.IntegerField(initial=0)
    a_bin3 = models.IntegerField(initial=0)
    a_bin4 = models.IntegerField(initial=0)
    a_bin5 = models.IntegerField(initial=0)
    a_bin6 = models.IntegerField(initial=0)
    a_bin7 = models.IntegerField(initial=0)


def generate_participant_id():
    timestamp = datetime.now().strftime('%Y%m%d')
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'{timestamp}-{suffix}'


def set_payoffs(player: Player):
    gamble = next(g for g in C.GAMBLES if g['num'] == player.gamble_choice)
    player.payoff = cu(random.choice([gamble['a'], gamble['b']]))


class Instructions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if not player.participant.vars.get('participant_id_custom'):
            player.participant.vars['participant_id_custom'] = generate_participant_id()
        return dict(
            pid=player.participant.vars.get('participant_id_custom'),
            now=datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
        )


class GambleChoice(Page):
    form_model = 'player'
    form_fields = ['gamble_choice']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(gambles=C.GAMBLES)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoffs(player)
        mapping = {1: 'Very Conservative', 2: 'Conservative', 3: 'Moderate', 4: 'Aggressive', 5: 'Very Aggressive'}
        player.participant.vars['risk_profile'] = mapping.get(player.gamble_choice)


def _belief_vars(player):
    return dict(bin_labels=C.BIN_LABELS, total_tokens=C.TOTAL_TOKENS)


def _belief_error(player, values):
    h_total = sum(values[f'h_bin{i}'] for i in range(1, 8))
    a_total = sum(values[f'a_bin{i}'] for i in range(1, 8))
    if h_total != 20:
        return f'Human Wealth Manager tokens sum to {h_total}. Please use all 20 tokens.'
    if a_total != 20:
        return f'AI Advisor tokens sum to {a_total}. Please use all 20 tokens.'


_BELIEF_FIELDS = [
    'h_bin1', 'h_bin2', 'h_bin3', 'h_bin4', 'h_bin5', 'h_bin6', 'h_bin7',
    'a_bin1', 'a_bin2', 'a_bin3', 'a_bin4', 'a_bin5', 'a_bin6', 'a_bin7',
]


class BeliefElicitationEarly(Page):
    """'before' group only — shown right after GambleChoice."""
    template_name = 'risk_elicitation/BeliefElicitation.html'
    form_model = 'player'
    form_fields = _BELIEF_FIELDS

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars.get('timing_group') == 'before'

    vars_for_template = staticmethod(_belief_vars)
    error_message = staticmethod(_belief_error)


page_sequence = [Instructions, GambleChoice, BeliefElicitationEarly]

from otree.api import *
import random
import string
from datetime import datetime

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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gamble_choice = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        label='',
    )


def generate_participant_id():
    timestamp = datetime.now().strftime('%Y%m%d')
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'{timestamp}-{suffix}'


def set_payoffs(player: Player):
    import random
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


class Results(Page):
    pass


page_sequence = [Instructions, GambleChoice, Results]

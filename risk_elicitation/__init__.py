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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gamble_choice = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        label='',
    )


def set_payoffs(player: Player):
    import random
    gamble = next(g for g in C.GAMBLES if g['num'] == player.gamble_choice)
    player.payoff = cu(random.choice([gamble['a'], gamble['b']]))


class GambleChoice(Page):
    form_model = 'player'
    form_fields = ['gamble_choice']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(gambles=C.GAMBLES)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoffs(player)


class Results(Page):
    pass


page_sequence = [GambleChoice, Results]

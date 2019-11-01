# -*- coding: utf-8 -*-


import random
from typing import List

from flask import request

from koikoi.card import Card
from koikoi.field import Field
from koikoi.players.player import Player


class HumanFlask(Player):
    """
    Player class for humans in Flask application.

    Parameters
    ----------
    name : ``str``, optional (default = 'Human')
        Player name.
    display_hand : ``bool``, optional (default = True)
        Determines whether to display hands.
    """
    def __init__(
        self,
        name: str = 'Human',
        display_hand: bool = True,
    ) -> None:
        super().__init__(name, display_hand)

    def select_from_hand(self, field: Field, other: Player) -> Card:
        return Card.from_string(request.form['selected'])

    def select_from_field(
        self,
        choices: List[Card],
        field: Field,
        other,
    ) -> Card:

        return random.choice(choices)

    def koikoi(self, field: Field, other: Player) -> bool:
        return (random.random() < 0.5)

# -*- coding: utf-8 -*-


import random
from typing import List

from koikoi.card import Card
from koikoi.field import Field
from koikoi.players.player import Player


class RandomCPU(Player):
    """
    Player class for CPU that select cards randomly.

    Parameters
    ----------
    name : ``str``, optional (default = 'RandomCPU')
        Player name.
    display_hand : ``bool``, optional (default = False)
        Determines whether to display hands.
    """
    def __init__(
        self,
        name: str = 'RandomCPU',
        display_hand: bool = False,
    ) -> None:
        super().__init__(name, display_hand)

    def select_card_randomly(self, choices: List[Card]) -> Card:
        return random.choice(choices)

    def select_from_hand(self, field: Field, other: Player) -> Card:
        return self.select_card_randomly(self.hand)

    def select_from_field(
        self,
        choices: List[Card],
        field: Field,
        other: Player,
    ) -> Card:

        return self.select_card_randomly(choices)

    def koikoi(self, field: Field, other: Player) -> bool:
        return (random.random() < 0.5)

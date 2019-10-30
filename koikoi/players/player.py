# -*- coding: utf-8 -*-


from typing import List

from koikoi.card import Card, ShareCards
from koikoi.field import Field
from koikoi.point_calculator import PointCalculator


class Player(object):
    """
    An abstract class for players.

    Parameters
    ----------
    cards : ``List[Card]``
    name : ``str``, optional (default = 'Player')
    """
    def __init__(
        self,
        cards: List[Card],
        name: str = 'Player',
    ) -> None:

        self.name = name
        self.hand = cards
        self.share = ShareCards()
        self.point_data = {
            yaku: 0 for yaku in PointCalculator.YAKU2POINT.keys()
        }

    def select_from_hand(self, field: Field, other) -> Card:
        """
        Selects card from hand in this player's turn.

        Paramteres
        ----------
        field : ``Field``
        other : ``Player``

        Return
        ------
        card : ``Card``
        """
        raise NotImplementedError()

    def select_from_field(
        self,
        choices: List[Card],
        field: Field,
        other,
    ) -> Card:
        """
        Selects card from field when two cards are the same month
        as the player put on the field.

        Paramteres
        ----------
        choices : ``List[Card]``
        field : ``Field``
        other : ``Player``

        Return
        ------
        card : ``Card``
        """
        raise NotImplementedError()

    def koikoi(self, field: Field, other) -> bool:
        """
        Determines whether to koikoi or not.

        Paramteres
        ----------
        field : ``Field``
        other : ``Player``

        Return
        ------
        is_koikoi : ``bool``
        """
        raise NotImplementedError()

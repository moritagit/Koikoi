# -*- coding: utf-8 -*-


from typing import List

from koikoi.card import Card
from koikoi.field import Field
from koikoi.players import Player


class Formatter(object):
    """
    An abstract class for formatters.
    Formatter outputs cards in field and player hands.
    """
    def __call__(self, message: str) -> None:
        pass

    def format_hand(self, player: Player) -> None:
        pass

    def format_share(self, player: Player) -> None:
        pass

    def format_field(self, field: Field) -> None:
        pass

    def format_yaku_update(self, updated_yaku: List[str]) -> None:
        pass

    def format_yaku(self, point_data: List[str]) -> None:
        pass

    def format_turn(self, player: Player) -> None:
        pass

    def format_card_selection(self, card: Card) -> None:
        pass

    def format_draw(self, card: Card) -> None:
        pass

    def format_get_cards(self, cards: List[Card]) -> None:
        pass

    def format_to_field(self, card: Card) -> None:
        pass

    def format_double_cards(self, month) -> None:
        pass

    def format_end_message(self, message: str) -> None:
        pass

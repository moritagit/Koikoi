# -*- coding: utf-8 -*-


from koikoi.card import Card
from koikoi.field import Field
from koikoi.players import Player


class Formatter(object):
    """
    An abstract class for formatters.
    Formatter outputs cards in field and player hands.
    """
    def format_field(self, field: Field):
        pass

    def format_hand(self, player: Player):
        pass

    def format_card_selection(self, card: Card):
        pass

    def format_draw(self, card: Card):
        pass

    def format_end_message(self, message: str):
        pass

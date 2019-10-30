# -*- coding: utf-8 -*-

from typing import List

from koikoi.card import Card
from koikoi.field import Field
from koikoi.players import Player
from koikoi.formatters.formatter import Formatter


class Console(Formatter):
    """Formatter for console."""
    def format_turn(self, player: Player):
        print(f'{player.name}の番です')

    def format_hand(self, player: Player):
        print(f'{player.name}の手札')
        print(player.hand)
        print()

    def format_share(self, player: Player):
        print(f'{player.name}の取り札')
        print(player.share.data)
        print()

    def format_field(self, field: Field):
        print('場')
        print(field.cards)
        print()

    def format_card_selection(self, card: Card):
        print(f'{card.name}を出しました')
        print()

    def format_draw(self, card: Card):
        print('山札から1枚引きます')
        print(f'{card.name}が引かれました')
        print()

    def format_yaku(self, updated_yaku: List[str]):
        for yaku in updated_yaku:
            print(f'{yaku}です')
        print()

    def format_end_message(self, message: str):
        print(message)

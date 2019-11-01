# -*- coding: utf-8 -*-

from typing import List

from koikoi.card import Card
from koikoi.field import Field
from koikoi.players import Player
from koikoi.formatters.formatter import Formatter


class Console(Formatter):
    """Formatter for console."""
    def __call__(self, message: str) -> None:
        print(message)

    def format_hand(self, player: Player) -> None:
        if player.display_hand:
            print(f'{player.name}の手札')
            print(player.hand)
            print()

    def format_share(self, player: Player) -> None:
        print(f'{player.name}の取り札')
        print(player.share.data)
        print()

    def format_field(self, field: Field) -> None:
        print('場')
        print(field.cards)
        print()

    def format_yaku_update(self, updated_yaku: List[str]) -> None:
        for yaku in updated_yaku:
            print(f'{yaku}です')
        print()

    def format_yaku(self, point_data: List[str]) -> None:
        print('役')
        for yaku, point in point_data.items():
            if point > 0:
                print(f'{yaku:<4}：{point:>2}文')
        print()

    def format_turn(self, player: Player) -> None:
        print('\n')
        print(f'{player.name}の番です')
        print()

    def format_card_selection(self, card: Card) -> None:
        print(f'{card.name}を選びました')

    def format_draw(self, card: Card):
        print('山札から1枚引きます')
        print(f'{card.name}が引かれました')

    def format_get_cards(self, cards: List[Card]) -> None:
        cards_str = ', '.join([card.name for card in cards])
        print(f'取り札に{cards_str}が加わりました')

    def format_to_field(self, card: Card) -> None:
        print(f'{card.name}が場に出されました')

    def format_double_cards(self, month) -> None:
        print(f'{month}月の札が場に2枚あります')

    def format_end_message(self, message: str) -> None:
        print(message)
        print('\n')

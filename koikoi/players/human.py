# -*- coding: utf-8 -*-


import io
import sys
from typing import List

from koikoi.card import Card, UnknownCardNameError
from koikoi.field import Field
from koikoi.players.player import Player


sys.stdin = io.TextIOWrapper(
    sys.stdin.buffer, encoding='utf-8', errors='replace',
)


class Human(Player):
    """
    Player class for humans.

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

    def select_card_from_name(
        self,
        choices: List[Card],
        namespace: str,
    ) -> Card:

        input_name = input('札の名前を入力してください：')

        # check if the input is valid name
        try:
            selected_card = Card.from_string(input_name)
        except UnknownCardNameError:
            print(f'「{input_name}」という名前の札はありません。')
            selected_card = self.select_card_from_name(choices, namespace)

        # check if the card is in the field
        if selected_card not in choices:
            print(f'「{input_name}」は{namespace}にありません。')
            selected_card = self.select_card_from_name(choices, namespace)

        return selected_card

    def select_from_hand(self, field: Field, other: Player) -> Card:
        return self.select_card_from_name(self.hand, '手札')

    def select_from_field(
        self,
        choices: List[Card],
        field: Field,
        other,
    ) -> Card:

        return self.select_card_from_name(choices, '場')

    def koikoi(self, field: Field, other: Player) -> bool:
        input_decision = input('こいこいしますか？上がりますか？：')
        if input_decision in ['こいこい', 'koikoi']:
            is_koikoi = True
        elif input_decision in ['上がり', 'agari']:
            is_koikoi = False
        else:
            print('「こいこい」もしくは「上がり」と入力してください。')
            is_koikoi = self.koikoi(field, other)
        return is_koikoi

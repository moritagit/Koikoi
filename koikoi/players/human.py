# -*- coding: utf-8 -*-


from typing import List

from koikoi.card import Card, UnknownCardNameError
from koikoi.field import Field
from koikoi.players.player import Player


class Human(Player):
    """
    Player class for humans.

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

        super().__init__(cards, name)

    def select_card_from_name(self, field: Field):
        input_name = input('札の名前を入力してください：')

        # check if the input is valid name
        try:
            selected_card = Card.from_string(input_name)
        except UnknownCardNameError:
            print(f'「{input_name}」という名前の札はありません。')
            selected_card = self.select_card_from_name(field)

        # check if the card is in the field
        if selected_card not in field:
            print(f'「{input_name}」は場にありません。')
            selected_card = self.select_card_from_name(field)

        return selected_card

    def select_from_hand(self, field: Field, other: Player) -> Card:
        return self.select_card_from_name(field)

    def select_from_field(self, field: Field, other: Player) -> Card:
        return self.select_card_from_name(field)

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

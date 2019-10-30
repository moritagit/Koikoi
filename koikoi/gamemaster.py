# -*- coding: utf-8 -*-


from typing import List, Tuple

from koikoi.card import Card, Deck
from koikoi.field import Field, AllSameMonthCardAppearanceError
from koikoi.players import Player, Human, RandomCPU


class GameMaster(object):
    """Game master for Koikoi."""
    def __init__(self) -> None:
        self.deck, self.field, self.player1, self.player2 = self.build()

    def build(self) -> Tuple[Deck, Field, Player, Player]:
        try:
            deck = Deck()
            field = Field(deck)
            player1 = Human(
                cards=[deck.pop() for _ in range(8)],
                name='Human1',
            )
            player2 = Human(
                cards=[deck.pop() for _ in range(8)],
                name='Human2',
            )
        except AllSameMonthCardAppearanceError:
            print(AllSameMonthCardAppearanceError)
            deck, field, player1, player2 = self.build()

        return deck, field, player1, player2

    def put_card_to_field(self, card: Card, player: Player, other: Player):
        same_month_cards = self.field.get_same_month_cards(card)
        n_mathced = len(same_month_cards)
        if n_mathced == 0:
            self.field.append(card)
        elif n_mathced in [1, 3]:
            self.field.remove(same_month_cards)
            player.share.extend([card] + same_month_cards)
        elif n_mathced == 2:
            selected_card = player.select_from_field(
                same_month_cards, self.field, other,
            )
            self.field.remove(selected_card)
            player.share.extend([card, selected_card])
        return

    def process_one_turn(self, player: Player, other: Player):
        # select card from hand
        selected_card = player.select_from_hand(self.field, other)
        self.put_card_to_field(selected_card, player, other)

        # draw card from deck
        drawn_card = self.deck.pop()
        self.put_card_to_field(drawn_card, player, other)

        # calc point

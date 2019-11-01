# -*- coding: utf-8 -*-


from typing import List, Union

from koikoi.card import Card, Deck


class Field(object):
    """Field for Koikoi."""
    def __init__(self) -> None:
        self.cards = []

    def __len__(self) -> int:
        return len(self.cards)

    def __contains__(self, card: Card) -> bool:
        return (card in self.cards)

    def build(self, deck: Deck) -> None:
        """
        Parameters
        ----------
        deck : ``Deck``
        """
        cards = []
        for _ in range(8):
            cards.append(deck.pop())

        months = [card.month for card in cards]
        for month in range(1, 13):
            if months.count(month) == 4:
                raise AllSameMonthCardAppearanceError(month)

        self.cards = cards

    def append(self, card: Card) -> None:
        self.cards.append(card)

    def remove(self, cards: Union[Card, List[Card]]) -> None:
        if isinstance(cards, Card):
            cards = [cards]
        deleted_cards = cards  # rename for readability

        for card in deleted_cards:
            if card not in self.cards:
                raise ValueError(f'{card}は場に出ていません。')

        new_cards = []
        for card in self.cards:
            if card not in deleted_cards:
                new_cards.append(card)
        self.cards = new_cards

    def get_same_month_cards(self, card: Card) -> List[Card]:
        """
        Searches the field and returns cards
        which belongs to the same month as the input card.

        Parameters
        ----------
        card : ``Card``

        Returns
        -------
        cards : ``List[Card]``
        """
        object_month = card.month
        cards = []
        for field_card in self.cards:
            if field_card.month == object_month:
                cards.append(field_card)
        return cards


class AllSameMonthCardAppearanceError(Exception):
    """
    Raised when all the four cards in the same month appeared in the field
    at the beggining of a game.

    Parameters
    ----------
    month : ``int``
    """
    def __init__(self, month: int) -> None:
        self.__message = f'{month}月の札が4枚場に出てしまいました。'

    def __str__(self) -> str:
        return self.__message

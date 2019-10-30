# -*- coding: utf-8 -*-


from typing import List

from koikoi.card import Card


class Hand(object):
    def __init__(self) -> None:
        self.data = {
            'light': [],
            'seed': [],
            'strip': [],
            'kasu': [],
        }

    def __len__(self) -> int:
        return sum(self.tolist())

    def tolist(self) -> List[Card]:
        return [len(lst) for lst in self.data.values()]

    def append(self, card: Card) -> None:
        self.data[card.role_class].append(card)

    def extend(self, cards: List[Card]) -> None:
        for card in cards:
            self.append(card)

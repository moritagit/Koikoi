# -*- coding: utf-8 -*-


import random
from typing import List


MONTH2CARD = {
    1: {
        'flower': '松',
        'light': ['鶴'],
        'seed': [],
        'strip': ['赤短'],
        'kasu': ['カス1', 'カス2'],
    },
    2: {
        'flower': '梅',
        'light': [],
        'seed': ['鴬'],
        'strip': ['赤短'],
        'kasu': ['カス1', 'カス2'],
    },
    3: {
        'flower': '桜',
        'light': ['幕'],
        'seed': [],
        'strip': ['赤短'],
        'kasu': ['カス1', 'カス2'],
    },
    4: {
        'flower': '藤',
        'light': [],
        'seed': ['不如帰'],
        'strip': ['短冊'],
        'kasu': ['カス1', 'カス2'],
    },
    5: {
        'flower': '菖蒲',
        'light': [],
        'seed': ['八橋'],
        'strip': ['短冊'],
        'kasu': ['カス1', 'カス2'],
    },
    6: {
        'flower': '牡丹',
        'light': [],
        'seed': ['蝶'],
        'strip': ['青短'],
        'kasu': ['カス1', 'カス2'],
    },
    7: {
        'flower': '萩',
        'light': [],
        'seed': ['猪'],
        'strip': ['短冊'],
        'kasu': ['カス1', 'カス2'],
    },
    8: {
        'flower': '芒',
        'light': ['月'],
        'seed': ['雁'],
        'strip': [],
        'kasu': ['カス1', 'カス2'],
    },
    9: {
        'flower': '菊',
        'light': [],
        'seed': ['盃'],
        'strip': ['青短'],
        'kasu': ['カス1', 'カス2'],
    },
    10: {
        'flower': '紅葉',
        'light': [],
        'seed': ['鹿'],
        'strip': ['青短'],
        'kasu': ['カス1', 'カス2'],
    },
    11: {
        'flower': '柳',
        'light': ['小野道風'],
        'seed': ['燕'],
        'strip': ['短冊'],
        'kasu': ['カス'],
    },
    12: {
        'flower': '鳳凰',
        'light': [],
        'seed': [],
        'strip': [],
        'kasu': ['カス1', 'カス2', 'カス3'],
    },
}


class Card(object):
    """
    Represents a card of hanahuda.

    Parameters
    ----------
    month : ``int``
        Month of the card.
    role_class : ``str``
        Role class of the card. Must be chosen from
        ``['light', 'seed', 'strip', 'kasu']``
    index : ``int``, optional (default = 0)
        Index
    """
    def __init__(
        self,
        month: int,
        role_class: str,
        index: int = 0,
    ) -> None:

        if (1 <= month <= 12):
            raise ValueError(
                '``month`` must be an integer between 1 and 12, '
                f'but {month} was input.'
            )
        if role_class not in ['light', 'seed', 'strip', 'kasu']:
            raise ValueError(
                f'Unknown ``role_class`` {role_class} was input. '
                '``role_class`` must be chosen from [light, seed, strip, kasu]'
            )
        if len(MONTH2CARD[month][role_class]) <= index:
            raise ValueError(
                f'Too large index for {role_class} cards of {month} month '
                f'({len(MONTH2CARD[month][role_class])} <= {index}).'
            )

        self.month = month
        self.role_class = role_class
        self.index = index

        flower = MONTH2CARD[month]['flower']
        role = MONTH2CARD[month][role_class][index]
        self.name = f'{flower}の{role}'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Card) and (self.name == other.name)

    def __ne__(self, other):
        return not (isinstance(other, Card) and (self.name == other.name))


class Deck(object):
    """Represents deck."""
    def __init__(self):
        self.cards = self.build()

    def __len__(self):
        return len(self.cards)

    def build(self) -> List[Card]:
        cards = []
        for month in range(1, 13):
            for role_class in ['light', 'seed', 'strip', 'kasu']:
                for index, role in enumerate(MONTH2CARD[month][role_class]):
                    card = Card(month, role_class, index)
                    cards.append(card)
        random.shuffle(cards)
        return cards

    def pop(self):
        return self.cards.pop(0)

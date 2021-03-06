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
        'flower': '桐',
        'light': ['鳳凰'],
        'seed': [],
        'strip': [],
        'kasu': ['カス1', 'カス2', 'カス3'],
    },
}

ROLE_CLASSES = ['light', 'seed', 'strip', 'kasu']


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

        if not (1 <= month <= 12):
            raise ValueError(
                '``month`` must be an integer between 1 and 12, '
                f'but {month} was input.'
            )
        if role_class not in ROLE_CLASSES:
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
        self.role = MONTH2CARD[month][role_class][index]
        self.name = f'{flower}の{self.role}'

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other) -> bool:
        return isinstance(other, Card) and (self.name == other.name)

    def __ne__(self, other) -> bool:
        return not (isinstance(other, Card) and (self.name == other.name))

    def __lt__(self, other):
        if self.month < other.month:
            return True
        elif self.month > other.month:
            return False
        else:
            # if is same month
            if (
                ROLE_CLASSES.index(self.role_class)
                < ROLE_CLASSES.index(other.role_class)
            ):
                return True
            elif (
                ROLE_CLASSES.index(self.role_class)
                > ROLE_CLASSES.index(other.role_class)
            ):
                return False
            else:
                # if is same month and role class (kasu only)
                return (self.index < other.index)

    def __gt__(self, other):
        if self.month > other.month:
            return True
        elif self.month < other.month:
            return False
        else:
            # if is same month
            if (
                ROLE_CLASSES.index(self.role_class)
                > ROLE_CLASSES.index(other.role_class)
            ):
                return True
            elif (
                ROLE_CLASSES.index(self.role_class)
                < ROLE_CLASSES.index(other.role_class)
            ):
                return False
            else:
                # if is same month and role class (kasu only)
                return (self.index > other.index)

    @classmethod
    def from_string(cls, name):
        """
        Makes Card object from string representation, like '芒の月'.

        Parameters
        ----------
        name : ``str``
            Card name.

        Returns
        -------
        card : ``Card``
            A card made from string.

        Raises
        ------
        ``UnknownCardNameError``
        """
        if name.count('の') != 1:
            raise UnknownCardNameError(name)

        target_flower, target_role = name.split('の')
        for month, data in MONTH2CARD.items():
            if target_flower == data['flower']:
                for role_class in ROLE_CLASSES:
                    for index, role in enumerate(data[role_class]):
                        if target_role == role:
                            card = Card(month, role_class, index)
                            return card
        raise UnknownCardNameError(name)


class UnknownCardNameError(Exception):
    """
    Raised when Card.from_string method meets unknown card name.

    Parameters
    ----------
    name : ``str``
        A (wrong) card name.
    """
    def __init__(self, name: str) -> None:
        self.__message = f'{name} does not exist.'

    def __str__(self) -> str:
        return self.__message


class Deck(object):
    """Represents deck."""
    def __init__(self) -> None:
        self.cards = self.build()

    def __len__(self) -> int:
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

    def pop(self) -> Card:
        return self.cards.pop(0)


class ShareCards(object):
    """Represents cards a player got in the game."""
    def __init__(self) -> None:
        self.data = {
            'light': [],
            'seed': [],
            'strip': [],
            'kasu': [],
        }

    def __len__(self) -> int:
        return len(self.tolist())

    def tolist(self) -> List[Card]:
        share_list = []
        for lst in self.data.values():
            share_list.extend(lst)
        return share_list

    def append(self, card: Card) -> None:
        self.data[card.role_class].append(card)

    def extend(self, cards: List[Card]) -> None:
        for card in cards:
            self.append(card)

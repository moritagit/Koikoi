# -*- coding: utf-8 -*-


import random
from typing import List, Dict

from koikoi.card import Card, Deck, ROLE_CLASSES, MONTH2CARD
from koikoi.field import Field
from koikoi.players.player import Player


def make_month2cards(cards: List[Card]) -> Dict[str, List[Card]]:
    """
    Makes a dictionary from month to a list of cards which belong to the month.

    Parameters
    ----------
    cards : ``List[Card]``

    Returns
    -------
    month2cards : ``Dict[str, List[Card]]``
    """
    month2cards = {}
    for month in range(1, 13):
        month2cards[month] = []
    for card in cards:
        month2cards[card.month].append(card)
    return month2cards


class RuleBase(Player):
    """
    Player class which select cards by rule base.

    Parameters
    ----------
    name : ``str``, optional (default = 'RuleBase')
        Player name.
    display_hand : ``bool``, optional (default = False)
        Determines whether to display hands.
    """
    def __init__(
        self,
        name: str = 'RuleBase',
        display_hand: bool = False,
    ) -> None:

        super().__init__(name, display_hand)

        self._priority_month = [
            [9],
            [3, 8],
            [1],
            [12],
            [6, 10],
            [11],
            [2, 7],
            [4, 5],
        ]
        '''
        self._priority_flower = [
            ['菊'],
            ['桜', '芒'],
            ['松'],
            ['桐'],
            ['牡丹', '紅葉'],
            ['柳'],
            ['梅', '萩'],
            ['藤', '菖蒲'],
        ]
        self._priority_role = [
            '盃',
            '幕', '月',
            '鶴',
            '鳳凰',
            '赤短', '青短',
            '小野道風',
            '鹿', '蝶', '猪',
            # '鴬', '不如帰', '八橋', '雁', '燕',  # seed
            # '短冊', 'カス1', 'カス2',  # strip and kasu
        ]
        self._month2primeroles = {
            1: ['鶴', '赤短'],
            2: ['赤短'],
            3: ['幕', '赤短'],
            4: [],
            5: [],
            6: ['蝶', '青短'],
            7: ['猪'],
            8: ['月'],
            9: ['盃', '青短'],
            10: ['鹿', '青短'],
            11: ['小野道風'],
            12: ['鳳凰'],
        }
        '''
        self._primary_cards = self._make_primary_card_list()
        self._all_cards = set(Deck().cards)

    def _make_primary_card_list(self) -> List[Card]:
        primary_cards = []
        for month_list in self._priority_month:
            for month in month_list:
                for role_class in ROLE_CLASSES:
                    for index, role in enumerate(MONTH2CARD[month][role_class]):
                        card = Card(month, role_class, index)
                        primary_cards.append(card)
        return primary_cards

    def _make_haveN_remainN(
        self,
        month2card_hand: Dict[int, List[Card]],
        month2card_remaining: Dict[int, List[Card]],
    ) -> Dict[str, List[int]]:

        haveNremainN = {
            'have4': [],
            'have3remain1': [],
            'have2remain2': [],
            'have2remain0': [],
            'have1remain1': [],
            'have1remain23': [],
        }

        for month in range(1, 13):
            if len(month2card_hand[month]) == 0:
                continue
            elif len(month2card_hand[month]) == 4:
                haveNremainN['have4'].append(month)
            elif len(month2card_hand[month]) == 3:
                haveNremainN['have3remain1'].append(month)
            elif len(month2card_hand[month]) == 2:
                if len(month2card_remaining[month]) == 2:
                    haveNremainN['have2remain2'].append(month)
                elif len(month2card_remaining[month]) == 0:
                    haveNremainN['have2remain0'].append(month)
            elif (
                (len(month2card_hand[month]) == 1)
                and (len(month2card_remaining[month]) == 1)
            ):
                haveNremainN['have1remain1'].append(month)
            else:  # that is, have1 and remain2 or remain3
                haveNremainN['have1remain23'].append(month)
        return haveNremainN

    def _make_haveN_existN(
        self,
        month2card_hand: Dict[int, List[Card]],
        month2card_field: Dict[int, List[Card]],
        month2card_remaining: Dict[int, List[Card]],
        matched_months: List[int],
    ) -> Dict[str, List[int]]:

        haveNexistN = {
            'have3exist1': [],
            'have2exist2': [],
            'have2exist1': [],
            'have1exist3': [],
            'have1exist2': [],
            'have1exist1remain2': [],
            'have1exist1remain0': [],
        }

        for month in matched_months:
            if len(month2card_hand[month]) == 3:
                haveNexistN['have3exist1'].append(month)
            elif len(month2card_hand[month]) == 2:
                if len(month2card_field[month]) == 2:
                    haveNexistN['have2exist2'].append(month)
                elif len(month2card_field[month]) == 1:
                    haveNexistN['have2exist1'].append(month)
            elif len(month2card_hand[month]) == 1:
                if len(month2card_field[month]) == 3:
                    haveNexistN['have1exist3'].append(month)
                elif len(month2card_field[month]) == 2:
                    haveNexistN['have1exist2'].append(month)
                elif len(month2card_field[month]) == 1:
                    if len(month2card_remaining[month]) == 2:
                        haveNexistN['have1exist1remain2'].append(month)
                    elif len(month2card_remaining[month]) == 0:
                        haveNexistN['have1exist1remain0'].append(month)
        return haveNexistN

    def select_card_randomly(self, choices: List[Card]) -> Card:
        return random.choice(choices)

    def select_card_sequentialy(
        cards: List[Card],
        reverse: bool = False,
    ) -> Card:

        sorted_cards = sorted(cards)
        idx = (-1 if reverse else 0)
        card = sorted_cards[idx]
        return card

    def select_from_field(
        self,
        choices: List[Card],
        field: Field,
        other: Player,
    ) -> Card:

        return self.select_card_sequentialy(choices)

    def koikoi(self, field: Field, other: Player) -> bool:
        return (random.random() < 0.5)

    def select_from_hand(self, field: Field, other: Player) -> Card:
        m2c_hand = make_month2cards(self.hand)
        m2c_field = make_month2cards(field.cards)

        remaining_cards = (
            self._all_cards
            - set(self.hand)
            - set(self.share.tolist())
            - set(field.cards)
            - set(other.share.tolist())
        )
        m2c_remaining = make_month2cards(remaining_cards)

        matched_months = []
        for month in range(1, 13):
            if m2c_hand[month] and m2c_field[month]:
                matched_months.append(month)

        chosen = None
        haveNremainN = self._make_haveN_remainN(m2c_hand, m2c_remaining)

        if len(matched_months) == 0:
            # when can not get any card from the field
            if haveNremainN['have4']:
                chosen = self.select_card_randomly(
                    m2c_hand[haveNremainN['have4'][0]]
                )
            elif haveNremainN['have2remain0']:
                chosen = self.select_card_randomly(
                    m2c_hand[haveNremainN['have2remain0'][0]]
                )
            elif haveNremainN['have3remain1']:
                # todo: improve the logic ?
                for month_list in self._priority_month[::-1]:
                    for month in month_list:
                        if month in haveNremainN['have3remain1']:
                            chosen = self.select_card_sequentialy(
                                m2c_hand[month], reverse=True,
                            )
            elif haveNremainN['have1remain23']:
                for month_list in self._priority_month[::-1]:
                    for month in month_list:
                        if month in haveNremainN['have1remain23']:
                            chosen_temp = m2c_hand[month][0]
                            if chosen_temp not in self._primary_cards:
                                chosen = chosen_temp
            elif haveNremainN['have2remain2']:
                for month_list in self._priority_month[::-1]:
                    if month in haveNremainN['have2remain2']:
                        chosen_temp = self.select_card_sequentialy(
                            m2c_hand[month], reverse=True,
                        )
                        if chosen_temp not in self._primary_cards:
                            chosen = chosen_temp
            elif haveNremainN['have1remain1']:
                for month_list in self._priority_month[::-1]:
                    if month in haveNremainN['have1remain1']:
                        chosen_temp = m2c_hand[month][0]
                        if chosen_temp not in self._primary_cards:
                            chosen = chosen_temp
            else:
                raise ValueError('Some unknown error occured.')

            if not chosen:
                for card in self._primary_cards[::-1]:
                    if card in self.hand:
                        chosen = card
            return chosen

        else:
            # when can get a card from the field

            haveNexistN = self._make_haveN_existN(
                m2c_hand, m2c_field, m2c_remaining, matched_months,
            )

            # choose from cards which are not confirmed to be taken
            cands = []
            for key in ['have2exist1', 'have1exist1remain2', 'have1exist2']:
                month_list = haveNexistN[key]
                for month in month_list:
                    cands.extend(m2c_hand[month])
                    cands.extend(m2c_field[month])

            if Card.from_string('菊の盃') in cands:
                chosen = self.select_card_sequentialy(m2c_hand[9])
            elif Card.from_string('桜の幕') in cands:
                chosen = self.select_card_sequentialy(m2c_hand[3])
            elif Card.from_string('芒の月') in cands:
                chosen = self.select_card_sequentialy(m2c_hand[8])

            if chosen:
                return chosen

            if haveNexistN['have2exist1']:
                for month in self._priority_month:
                    if month in haveNexistN['have2exist1']:
                        chosen = self.select_card_sequentialy(m2c_hand[month])
                        break
            elif haveNexistN['have1exist1remain2']:
                for month in self._priority_month:
                    if month in haveNexistN['have1exist1remain2']:
                        hand_card = m2c_hand[month]
                        field_card = m2c_field[month]
                        if (
                            set(hand_card + field_card)
                            and set(self._primary_cards)
                        ):
                            chosen = hand_card
                            break
            elif haveNexistN['have1exist2']:
                for month in self._priority_month:
                    if month in haveNexistN['have1exist2']:
                        hand_card = m2c_hand[month]
                        field_card = m2c_field[month]
                        if (
                            set(hand_card + field_card)
                            and set(self._primary_cards)
                        ):
                            chosen = hand_card
                            break

            if chosen:
                return chosen

            if haveNexistN['have2exist1']:
                chosen = self.select_card_sequentialy(
                    m2c_hand[haveNexistN['have2exist1'][0]]
                )
            elif haveNexistN['have1exist2']:
                chosen = m2c_hand[haveNexistN['have1exist2'][0]][0]
            elif haveNexistN['have1exist1remain2']:
                chosen = m2c_hand[haveNexistN['have1exist1remain2'][0]][0]

            if chosen:
                return chosen

            # select a card which is confirmed to be taken
            if haveNremainN['have4']:
                chosen = self.select_card_randomly(
                    m2c_hand[haveNremainN['have4'][0]]
                )
            elif haveNremainN['have2remain0']:
                chosen = self.select_card_randomly(
                    m2c_hand[haveNremainN['have2remain0'][0]]
                )

            if chosen:
                return chosen

            if haveNexistN['have2exist2']:
                chosen = self.select_card_sequentialy(
                    m2c_hand[haveNexistN['have2exist2'][0]], reverse=True,
                )
            elif haveNremainN['have3remain1']:
                # todo: improve the logic ?
                for month in self._priority_month:
                    if month in haveNremainN['have3remain1']:
                        chosen = self.select_card_sequentialy(
                           m2c_hand[month], reverse=True,
                        )
            elif haveNremainN['have1remain23']:
                for month in self._priority_month:
                    if month in haveNremainN['have1remain23']:
                        chosen_temp = m2c_hand[month][0]
                        if chosen_temp not in self._primary_cards:
                            chosen = chosen_temp
            elif haveNremainN['have2remain2']:
                for month in self._priority_month:
                    if month in haveNremainN['have2remain2']:
                        chosen_temp = m2c_hand[month][-1]
                        if chosen_temp not in self._primary_cards:
                            chosen = chosen_temp

            if chosen:
                return chosen

            # choose from cards which are confirmed to be taken
            if haveNexistN['have3exist1']:
                chosen = self.select_card_sequentialy(
                    m2c_hand[haveNexistN['have3exist1'][0]], reverse=True,
                )
            elif haveNexistN['have1exist3']:
                chosen = m2c_hand[haveNexistN['have1exist3'][0]][0]
            elif haveNexistN['have1exist1remain0']:
                chosen = m2c_hand[haveNexistN['have1exist1remain0'][0]][0]

        return chosen

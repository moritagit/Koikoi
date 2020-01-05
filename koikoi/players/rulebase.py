# -*- coding: utf-8 -*-


import random
from typing import List

from koikoi.card import Card
from koikoi.field import Field
from koikoi.players.player import Player


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

    def select_card_randomly(self, choices: List[Card]) -> Card:
        return random.choice(choices)

    def select_from_hand(self, field: Field, other: Player) -> Card:
        return self.select_card_randomly(self.hand)

    def select_from_field(
        self,
        choices: List[Card],
        field: Field,
        other: Player,
    ) -> Card:

        return self.select_card_randomly(choices)

    def koikoi(self, field: Field, other: Player) -> bool:
        return (random.random() < 0.5)

    def make_primecard_list():
        """
        This is a function to make a list of cards which have priority.
        """
        priority2flower_list = [["菊"], ["桜", "芒"], ["松"], ["桐"], ["牡丹", "紅葉"], ["柳"], ["梅", "萩"], ["藤", "菖蒲"]]
        priority2role_list = ["盃", "幕", "月", "鶴", "鳳凰", "赤短", "青短", "小野道風", "鹿", "蝶", "猪"]
        priority2month_list = [9, 3, 8, 1, 12, 6, 10, 11, 2, 7]

        month2primeroles = {
            1 : ["鶴", "赤短"], 2 : ["赤短"], 3 : ["幕", "赤短"], 4 : [], 5 : [], 6 : ["蝶", "青短"],
            7 : ["猪"], 8 : ["月"], 9 : ["盃", "青短"], 10 : ["鹿", "青短"], 11 : ["小野道風"], 12 : ["鳳凰"]
        }

        priority_list = []
        for flowerlist in priority2flower_list:
            for flower in flowerlist:
                month = flower2month[flower]
                for role in month2role[month]:
                    priority_list.append(Card(month, role))
        return priority_list

    def make_priority_list(self):       #要アップデート
        """
        This is a method to make a priority list of cards for cp.
        """
        hand_dict = make_month2cards(self.cp.hand)
        month2count = {}
        for month in range(1, 13):
            if hand_dict[month] is not []:
                month2count[month] = month2count.get(month, 0) + 1

        remain = self.deck
        remain += self.player.hand
        month2remain = make_month2cards(remain)

        self.month_priority = []
        months_in_hand = list(month2count.keys())
        for i in range(len(priority2flower_list)):
            for flower in priority2flower_list[i]:
                if flower2month[flower] in months_in_hand:
                    self.month_priority.append(flower2month[flower])

    def choose_from(cards, reverse=False):
        """
        This is a function to choose a card from 2 cards.
        """
        sorted_cards = sorted(cards)
        if reverse == False:
            return sorted_cards[0]
        else:
            return sorted_cards[-1]

    def choose(self):           #なんか死んでる
        """
        This is a method for cp to choose a card from his hand, to put it on the field.
        """
        hand_dict = make_month2cards(self.cp.hand)
        field_dict = make_month2cards(self.field)
        self.make_priority_list()

        remain = self.deck
        remain += self.player.hand
        month2remaining = make_month2cards(remain)

        chosen = None

        matched_month = []
        for month in range(1, 13):
            if (hand_dict[month] != []) and (field_dict[month] != []):
                matched_month.append(month)

        # frags and lists for searching cp's hand
        have4 = False
        have4month = []
        have3remain1 = False
        have3remain1month = []
        have2remain2 = False
        have2remain2month = []
        have2remain0 = False
        have2remain0month = []
        have1remain1 = False
        have1remain1month = []
        have1remain23 = False
        have1remain23month = []

        have3thereis1 = False
        have3thereis1month = []
        have2thereis2 = False
        have2thereis2month = []
        have2thereis1 = False
        have2thereis1month = []
        have1thereis3 = False
        have1thereis3month = []
        have1thereis2 = False
        have1thereis2month = []
        have1thereis1remain2 = False
        have1thereis1remain2month = []
        have1thereis1remain0 = False
        have1thereis1remain0month = []

        # recognize the circumstance
        for month in range(1, 13):
            if len(hand_dict[month]) == 0:
                continue
            elif len(hand_dict[month]) == 4:
                have4 = True
                have4month.append(month)
            elif len(hand_dict[month]) == 3:
                have3remain1 = True
                have3remain1month.append(month)
            elif len(hand_dict[month]) == 2:
                if len(month2remaining) == 2:
                    have2remain2 = True
                    have2remain2month.append(month)
                elif len(month2remaining) == 0:
                    have2remain0 = True
                    have2remain0month.append(month)
            elif (len(hand_dict[month]) == 1) and (len(month2remaining) == 1):
                have1remain1 = True
                have1remain1month.append(month)
            else:  # that is, have1remain2 or have1remain3
                have1remain23 = True
                have1remain23month.append(month)

        # when cp can take nothing from the field
        if len(matched_month) == 0:
            if have4:
                chosen = random.choice(hand_dict[have4month[0]])
            elif have2remain0:
                chosen = random.choice(hand_dict[have2remain0month])
            elif have3remain1:                                              #ここに複雑な論理を入れる？
                for flowerlist in priority2flower_list[::-1]:
                    for flower in flowerlist:
                        month = flower2month[flower]
                        if month in have3remain1month:
                            chosen = Card(month, "カス")
            elif have1remain23:
                for flowerlist in priority2flower_list[::-1]:
                    for flower in flowerlist:
                        month = flower2month[flower]
                        if month in have1remain23month:
                            chosen_temp = hand_dict[month][0]
                            if chosen_temp not in self.prime_cards:
                                chosen = chosen_temp
            elif have2remain2:
                for flowerlist in priority2flower_list[::-1]:
                    for flower in flowerlist:
                        month = flower2month[flower]
                        if month in have2remain2month:
                            chosen_temp = choose_from(hand_dict[month], reverse=True)
                            if chosen_temp not in self.prime_cards:
                                chosen = chosen_temp
            else:   #have1remain1
                for flowerlist in priority2flower_list[::-1]:
                    for flower in flowerlist:
                        month = flower2month[flower]
                        if month in have1remain1month:
                            chosen_temp = hand_dict[month][0]
                            if chosen_temp not in self.prime_cards:
                                chosen = chosen_temp

            if chosen == None:
                for card in self.prime_cards[::-1]:
                    if card in self.cp.hand:
                        chosen = card

        # when cp can take anything from the field
        else:
            # recognize the circumstance
            for month in matched_month:
                if len(hand_dict[month]) == 3:
                    have3thereis1 = True
                    have3thereis1month.append(month)
                elif len(hand_dict[month]) == 2:
                    if len(field_dict[month]) == 2:
                        have2thereis2 = True
                        have2thereis2month.append(month)
                    elif len(field_dict[month]) == 1:
                        have2thereis1 = True
                        have2thereis1month.append(month)
                elif len(hand_dict[month]) == 1:
                    if len(field_dict[month]) == 3:
                        have1thereis3 = True
                        have1thereis3month.append(month)
                    elif len(field_dict[month]) == 2:
                        have1thereis2 = True
                        have1thereis2month.append(month)
                    elif len(field_dict[month]) == 1:
                        if len(month2remaining[month]) == 2:
                            have1thereis1remain2 = True
                            have1thereis1remain2month.append(month)
                        elif len(month2remaining[month]) == 0:
                            have1thereis1remain0 = True
                            have1thereis1remain0month.append(month)

            # choose from cards which are not confirmed to be taken
            if have2thereis1 or have1thereis1remain2 or have1thereis2:
                cantake = have2thereis1month
                cantake += have1thereis1remain2month
                cantake += have1thereis2month
                if "菊の盃" in cantake:
                    chosen = choose_from(hand_dict[9])
                elif "桜の幕" in cantake:
                    chosen = choose_from(hand_dict[3])
                elif "芒の月" in cantake:
                    chosen = choose_from(hand_dict[8])

            if not chosen:
                if have2thereis1:
                    for month in priority2month_list:
                        if month in have2thereis1month:
                            chosen = choose_from(hand_dict[month])
                            break
                elif have1thereis1remain2:
                    for month in priority2month_list:
                        if month in have1thereis1remain2month:
                            chosen_temp = choose_from(hand_dict[month])
                            if chosen_temp in self.prime_cards:
                                chosen = chosen_temp
                                break
                elif have1thereis2:
                    for month in priority2month_list:
                        if month in have1thereis2month:
                            chosen_temp = choose_from(hand_dict[month])
                            if chosen_temp in self.prime_cards:
                                chosen = chosen_temp
                                break

            if not chosen:
                if have2thereis1:
                    chosen = choose_from(hand_dict[have2thereis1month[0]])
                elif have1thereis2:
                    chosen = hand_dict[have1thereis2month[0]][0]
                elif have1thereis1remain2:
                    chosen = hand_dict[have1thereis1remain2month[0]][0]

            # put a card which is confirmed to be taken
            if not chosen:
                if have4:
                    chosen = random.choice(hand_dict[have4month[0]])
                elif have2remain0:
                    chosen = random.choice(hand_dict[have2remain0month[0]])

            # 中間処理
            if not chosen:
                if have2thereis2:
                    chosen = choose_from(hand_dict[have2thereis2month[0]], reverse=True)
                elif have3remain1:  # ここに複雑な論理を入れる？
                    for flowerlist in priority2flower_list[::-1]:
                        for flower in flowerlist:
                            month = flower2month[flower]
                            if month in have3remain1month:
                                chosen = Card(month, "カス")
                elif have1remain23:
                    for flowerlist in priority2flower_list[::-1]:
                        for flower in flowerlist:
                            month = flower2month[flower]
                            if month in have1remain23month:
                                chosen_temp = hand_dict[month][0]
                                if chosen_temp not in self.prime_cards:
                                    chosen = chosen_temp
                elif have2remain2:
                    for flowerlist in priority2flower_list[::-1]:
                        for flower in flowerlist:
                            month = flower2month[flower]
                            if month in have2remain2month:
                                chosen_temp = hand_dict[month][-1]
                                if chosen_temp not in self.prime_cards:
                                    chosen = chosen_temp

            # choose from cards which are confirmed to be taken
            if not chosen:
                if have3thereis1:
                    chosen = choose_from(hand_dict[have3thereis1month[0]], reverse=True)
                elif have1thereis3:
                    chosen = hand_dict[have1thereis3month[0]][0]
                elif have1thereis1remain0:
                    chosen = hand_dict[have1thereis1remain0month[0]][0]

        print(chosen)
        self.cp.hand.remove(chosen)
        return chosen

# -*- coding: utf-8 -*-


from typing import Dict, List

from koikoi.card import Card, Deck
from koikoi.field import Field, AllSameMonthCardAppearanceError
from koikoi.point_calculator import PointCalculator
from koikoi.formatters import Formatter, Console
from koikoi.players import Player, Human, RandomCPU


class GameMaster(object):
    """Game master for Koikoi."""
    def __init__(
        self,
        player1: Player = Human(),
        player2: Player = RandomCPU(),
        formatter: Formatter = Console(),
    ) -> None:

        self.deck = None
        self.field = Field()
        self.player1 = player1()
        self.player2 = player2()
        self.point_calculator = PointCalculator()
        self.formatter = formatter

        self.finish_message = '流れです。'

    def build(self) -> None:
        def _make_deck_and_field():
            try:
                self.deck = Deck()
                self.field.build(self.deck)
            except AllSameMonthCardAppearanceError:
                print(AllSameMonthCardAppearanceError)
                _make_deck_and_field()
            return

        def _distribute_card(player):
            player.build([self.deck.pop() for _ in range(8)])

        _make_deck_and_field()
        _distribute_card(self.player1)
        _distribute_card(self.player2)

    def put_card_to_field(
        self,
        card: Card,
        player: Player,
        other: Player,
    ) -> None:

        same_month_cards = self.field.get_same_month_cards(card)
        n_mathced = len(same_month_cards)
        if n_mathced == 0:
            self.field.append(card)
        elif n_mathced in [1, 3]:
            self.field.remove(same_month_cards)
            player.share.extend([card] + same_month_cards)
        elif n_mathced == 2:
            self.formatter.format_double_cards(card.month)
            selected_card = player.select_from_field(
                same_month_cards, self.field, other,
            )
            self.field.remove(selected_card)
            player.share.extend([card, selected_card])
        return

    def check_point_update(
        self,
        point_data: Dict[str, int],
        point_data_old: Dict[str, int],
    ) -> List[str]:

        updated_yaku = []
        for key in point_data.keys():
            point = point_data[key]
            point_old = point_data_old[key]
            diff = point - point_old
            was_updated = (diff > 0)
            if was_updated:
                updated_yaku.append(key)
        return updated_yaku

    def process_one_turn(self, player: Player, other: Player) -> None:
        # show
        self.formatter.format_share(other)
        self.formatter.format_hand(other)
        self.formatter.format_field(self.field)
        self.formatter.format_hand(player)
        self.formatter.format_share(player)
        self.formatter.format_turn(player)

        # select card from hand
        selected_card = player.select_from_hand(self.field, other)
        player.hand.remove(selected_card)
        self.put_card_to_field(selected_card, player, other)
        self.formatter.format_card_selection(selected_card)

        # draw card from deck
        drawn_card = self.deck.pop()
        self.put_card_to_field(drawn_card, player, other)
        self.formatter.format_draw(drawn_card)

        # calc point
        point_data = self.point_calculator(player.share)
        point_data_old = player.point_data
        updated_yaku = self.check_point_update(point_data, point_data_old)
        player.point_data = point_data
        self.formatter.format_yaku(updated_yaku)

        # koikoi
        is_finish = False
        if updated_yaku:
            if player.hand:
                is_koikoi = player.koikoi(self.field, other)
                is_finish = (not is_koikoi)
            else:
                is_finish = True

        # if finished, output the field and hands
        if is_finish:
            point = sum([val for val in player.point_data.values()])
            self.finish_message = f'{point}文で{player.name}の勝ちです。'
            self.formatter.format_share(other)
            self.formatter.format_hand(other)
            self.formatter.format_field(self.field)
            self.formatter.format_hand(player)
            self.formatter.format_share(player)

        return is_finish

    def run(self):
        # init
        self.deck, self.field, self.player1, self.player2 = self.build()

        # run
        while self.player1.hand or self.player2.hand:
            is_finish = self.process_one_turn(self.player1, self.player2)
            if is_finish:
                break

            is_finish = self.process_one_turn(self.player2, self.player1)
            if is_finish:
                break

        self.formatter.format_end_message(self.finish_message)

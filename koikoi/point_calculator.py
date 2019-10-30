# -*- coding: utf-8 -*-


from typing import Dict

from koikoi.card import Card, ShareCards


class PointCalculator(object):
    YAKU2POINT = {
        '五光': 10, '四光': 8, '雨四光': 7, '三光': 5,
        '花見酒': 5, '月見酒': 5,
        '猪鹿蝶': 5,
        '赤短青短': 10, '赤短': 5, '青短': 5,
        'たね': 1, 'たん': 1, 'かす': 1
    }

    def __init__(self):
        __predefined_card_names = [
            '柳の小野道風',
            '菊の盃', '桜の幕', '芒の月',
            '萩の猪', '紅葉の鹿', '牡丹の蝶',
        ]
        self._name2card = {
            name: Card.from_string(name)
            for name in __predefined_card_names
        }

    def __call__(self, share: ShareCards) -> Dict[str, int]:
        # make abbriviations
        y2p = PointCalculator.YAKU2POINT
        n2c = self._name2card

        # init point data
        point_data = {yaku: 0 for yaku in y2p.keys()}

        # hikari
        if len(share.lights) == 5:
            point_data['五光'] = y2p['五光']
        elif len(share.lights) == 4:
            if n2c['柳の小野道風'] in share.lights:
                point_data['雨四光'] = y2p['雨四光']
            else:
                point_data['四光'] = y2p['四光']
        elif ((len(share.lights) == 3) and (n2c['柳の小野道風'] in share.lights)):
            point_data['三光'] = y2p['三光']

        # sake
        if n2c['菊の盃'] in share.seeds:
            if n2c['桜の幕'] in share.lights:
                point_data['花見酒'] = y2p['花見酒']
            elif n2c['芒の月'] in share.lights:
                point_data['月見酒'] = y2p['月見酒']

        # tane
        n_seeds = len(share.seeds)
        if (
            n2c['萩の猪'] in share.seeds
            and n2c['紅葉の鹿'] in share.seeds
            and n2c['牡丹の蝶'] in share.seeds
        ):
            point_data['猪鹿蝶'] = y2p['猪鹿蝶']
            point_data['たね'] = y2p['たね'] * (n_seeds - 3)
        elif n_seeds >= 5:
            point_data['たね'] = y2p['たね'] * (n_seeds - 4)

        # tanzaku
        tan_roles = [card.role for card in share.strips]
        n_tan = len(share.strips)
        is_akatan = (tan_roles.count('赤短') == 3)
        is_aotan = (tan_roles.count('青短') == 3)
        if is_akatan and is_aotan:
            point_data['赤短青短'] = y2p['赤短青短']
            point_data['たん'] = y2p['たん'] * (n_tan - 6)
        elif is_akatan:
            point_data['赤短'] = y2p['赤短']
            point_data['たん'] = y2p['たん'] * (n_tan - 3)
        elif is_aotan:
            point_data['青短'] = y2p['青短']
            point_data['たん'] = y2p['たん'] * (n_tan - 3)
        elif n_tan >= 5:
            point_data['たん'] = y2p['たん'] * (n_tan - 4)

        # kasu
        n_kasu = len(share.kasu)
        if n2c['菊の盃'] in share.seeds:
            n_kasu += 1
        if n_kasu >= 10:
            point_data['かす'] = y2p['かす'] * (n_tan - 9)

        return point_data

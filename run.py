# -*- coding: utf-8 -*-


from typing import Optional

import click

import koikoi


@click.command()
@click.option('--mode', '-m', default='console')
@click.option('--player', '-p', default='')
def cmd(mode: str, player: str):
    mode = mode.lower()
    if mode == 'console':
        run_console(player=player)
    elif mode == 'app':
        run_app()
    else:
        raise ValueError(f'Unknown mode {mode}')


def run_console(player: str = ''):
    player = player.lower()

    if player == 'rulebase':
        player_cpu = koikoi.players.RuleBase()
    else:
        player_cpu = koikoi.players.RandomCPU()

    gm = koikoi.GameMaster(
        player2=player_cpu,
        formatter=koikoi.Console(),
    )
    gm.build()
    gm.run()


def run_app():
    from app.app import app
    app.run()


def main():
    cmd()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-


from flask import Flask, render_template

import koikoi


app = Flask(__name__)

gamemaster = koikoi.GameMaster(
    player1=koikoi.players.HumanFlask(),
    player2=koikoi.players.RandomCPU(),
    formatter=koikoi.Console(),
)


@app.route('/')
def main():
    gamemaster.build()
    return render_template(
        'index.html',
        message='はじめます',
        field=gamemaster.field,
        player=gamemaster.player1,
        other=gamemaster.player2,
    )


@app.route('/select', methods=['POST'])
def select():
    if gamemaster.is_finished:
        return render_template(
            'index.html',
            message='初めからを押してください',
            field=gamemaster.field,
            player=gamemaster.player1,
            other=gamemaster.player2,
        )

    message = ''

    # human turn
    was_human_win = gamemaster.process_one_turn(
        gamemaster.player1, gamemaster.player2,
    )

    if was_human_win:
        point = sum([val for val in gamemaster.player1.point_data.values()])
        message = f'{point}文であなたの勝ちです'
    else:
        # CP turn
        was_cp_win = gamemaster.process_one_turn(
            gamemaster.player2, gamemaster.player1,
        )
        if was_cp_win:
            point = sum([val for val in gamemaster.player2.point_data.values()])
            message = f'{point}文でCPの勝ちです'

    is_draw = (not (gamemaster.player1.hand or gamemaster.player2.hand))

    if not message:
        if is_draw:
            message = '流れです'
            gamemaster.formatter.format_end_message(message)
        else:
            message = 'あなたの番です'

    return render_template(
        'index.html',
        message=message,
        field=gamemaster.field,
        player=gamemaster.player1,
        other=gamemaster.player2,
    )

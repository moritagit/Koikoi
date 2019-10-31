# -*- coding: utf-8 -*-


from flask import Flask, render_template, request

import koikoi


app = Flask(__name__)

gamemaster = koikoi.GameMaster()


@app.route('/')
def main():
    gamemaster.build()
    return render_template(
        'index.html',
        field=gamemaster.field,
        player=gamemaster.player1,
        other=gamemaster.player2,
    )


@app.route('/select', methods=['POST'])
def select():
    gamemaster.build()
    selected_card = koikoi.Card.from_string(request.form['selected'])

    return render_template(
        'index.html',
        field=gamemaster.field,
        player=gamemaster.player1,
        other=gamemaster.player2,
    )

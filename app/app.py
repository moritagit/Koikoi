# -*- coding: utf-8 -*-


from flask import Flask, render_template, request

import koikoi


app = Flask(__name__)


@app.route('/')
def main():
    gamemaster = koikoi.GameMaster()

    return render_template(
        'index.html',
        field=gamemaster.field,
        player=gamemaster.player,
        other=gamemaster.other,
    )


@app.route('/select', methods=['POST'])
def select():
    selected_card = koikoi.Card.from_string(request.form['selected'])

    gamemaster = koikoi.GameMaster()

    return render_template(
        'index.html',
        field=gamemaster.field,
        player=gamemaster.player,
        other=gamemaster.other,
    )

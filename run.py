# -*- coding: utf-8 -*-


import click


@click.command()
@click.option('--mode', '-m', default='console')
def cmd(mode: str):
    if mode.lower() == 'console':
        run_console()
    elif mode.lower() == 'app':
        run_app()
    else:
        raise ValueError(f'Unknown mode {mode}')


def run_console():
    import koikoi
    gm = koikoi.GameMaster(
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

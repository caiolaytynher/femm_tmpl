from collections.abc import Callable

from femmlib.core import FEMM


def main() -> None:
    app = FEMM(
        doc_type='magnetics',
        freq=60,
        unit='centimeters',
        depth=2,
    )

    with app.new('base.FEM'):
        circle = app.circle((0, 0), 5)

    def analyze() -> None:
        with app.open('base.FEM', delay=20):
            circle.select('arc')

    interactive_prompt(analyze)


def interactive_prompt(*commands: Callable[[], None]) -> None:
    while True:
        print(
            'Options:',
            *[
                f'\t{i + 1}. {cmd.__name__.capitalize().replace('_', ' ')}'
                for i, cmd in enumerate(commands)
            ],
            '\tQ/q. Quit',
            sep='\n',
        )
        command = input('> ')

        if command.lower() == 'q':
            break

        if not command.isdigit():
            continue

        command_index = int(command) - 1

        if command_index > len(commands) - 1 or command_index < 0:
            continue

        commands[command_index]()


if __name__ == '__main__':
    main()

from femmlib import problem
from femmlib.core import open_femm

# TODO: Não precisa especificar a pasta pra tudo, é bom definir um
# standard, até pra facilitar a limpeza dos dados com o make.


def main() -> None:
    with open_femm(delay=2):
        state, unit = (
            problem.builder().with_depth(2).with_unit('centimeters').build()
        )
        print(state, unit)
        problem.solve('femm/tmp.FEM')


if __name__ == '__main__':
    main()

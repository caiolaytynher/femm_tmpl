from dataclasses import dataclass
from typing import Literal, Self

import femm

from femmlib.unit import Name as UnitName
from femmlib.unit import Unit
from helpers.path import PathLike, parse_path

type DocType = Literal[
    'magnetics',
    'electrostatics',
    'heat flow',
    'current flow',
]
type ProblemType = Literal['planar', 'axi']
type ArcSolver = Literal['successive approximation', 'newton']


@dataclass(init=False)
class Problem:
    """
    Responsável por definir, salvar e resolver o problema. Os valores
    padrão são os mesmos do FEMM. Ao instanciar esta classe, um novo
    arquivo será aberto e as variáveis do problema serão automaticamente
    definidas.
    """

    type: ProblemType
    freq: int
    unit: Unit
    depth: int

    def __init__(
        self,
        doc_type: Literal[DocType],
    ) -> None:
        """
        Tipo de documeto.

        `'magnetics'` : magnético
        `'electrostatics'` : eletrostático
        `'heat flow'` : fluxo de calor
        `'current flow'` : fluxo de corrente.
        """
        match doc_type:
            case 'magnetics':
                self.doc_type = 0
            case 'electrostatics':
                self.doc_type = 1
            case 'heat flow':
                self.doc_type = 2
            case 'current flow':
                self.doc_type = 3

        self.freq: int = 0
        self.unit = Unit('inches')
        self.problem_type: ProblemType = 'planar'
        self.precision: float = 1e-8
        self.depth: int = 1
        self.min_angle: int = 30
        self.arc_solver: Literal[0, 1] = 0

    def with_freq(self, freq: int) -> Self:
        """Frequência."""
        self.freq = freq
        return self

    def with_unit(self, unit: UnitName) -> Self:
        """
        Unidade de medida das distâncias.

        "inches", "millimeters", "centimeters",
        "mils" e "meters".
        """
        self.unit = unit
        return self

    def with_type(self, problem_type: ProblemType) -> Self:
        """Tipo do problema. "planar" para 2D e "axi" para 3D."""
        self.problem_type = problem_type
        return self

    def with_precision(self, precision: float) -> Self:
        """Precisão."""
        self.precision = precision
        return self

    def with_depth(self, depth: int) -> Self:
        """Profundidade."""
        self.depth = depth
        return self

    def with_min_angle(self, min_angle: int) -> Self:
        """Ângulo mínimo."""
        self.min_angle = min_angle
        return self

    def with_arc_solver(self, arc_solver: ArcSolver) -> Self:
        """
        Método de resolução dos arcos. 0 para aproximação sucessiva e 1
        para Newton.
        """
        self.arc_solver = arc_solver
        return self

    def build(self) -> tuple[Problem, Unit]:
        """
        Abre um novo documento no modo definido por `Problem.doctype` e
        define as variáveis do problema.
        """
        femm.newdocument(self.doc_type)
        femm.mi_probdef(
            self.freq,
            self.unit,
            self.problem_type,
            self.precision,
            self.depth,
            self.min_angle,
            self.arc_solver,
        )

        return Problem(self.freq, self.problem_type, self.depth), Unit(
            self.unit
        )


def builder() -> Builder:
    """
    Recebe o nome do arquivo .FEM e caminho de diretório onde serão
    salvos os arquivos específicos do FEMM. Se colocar uma pasta que não
    existe antes do nome do arquivo, a pasta será criada.
    """
    return Builder()


def solve(file: PathLike) -> None:
    """
    Salva o arquivo no caminho definido por `file`, criando a pasta se
    necessário, cria a mecha, analisa o circuito e carrega a solução.
    Certifique-se que o arquivo termina em `.FEM`.
    """
    file = parse_path(file, ensure_parent=True)
    assert file.name.endswith('.FEM'), f'File {file} should end in .FEM'

    # Salva, cria a mecha e analisa a solução.
    femm.mi_saveas(str(file))
    femm.mi_createmesh()
    femm.mi_analyze()
    femm.mi_loadsolution()

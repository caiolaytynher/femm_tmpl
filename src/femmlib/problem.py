from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Self

import femm

from femmlib.unit import Unit, UnitLike

type DocType = Literal[
    'magnetics',
    'electrostatics',
    'heat flow',
    'current flow',
]
type ProblemType = Literal['planar', 'axi']
type ArcSolver = Literal['successive approximation', 'newton']


@dataclass
class Problem:
    freq: int
    unit: Unit
    type: ProblemType
    precision: float
    depth: int
    min_angle: int
    arc_solver: ArcSolver

    def update(self) -> Self:
        femm.mi_probdef(
            self.freq,
            self.unit.name,
            self.type,
            self.precision,
            self.depth,
            self.min_angle,
            0 if self.arc_solver == 'successive approximation' else 1,
        )

        return self

    @staticmethod
    def solve(file_name: str) -> None:
        """
        Salva o arquivo no caminho definido por `file`, criando a pasta se
        necessário, cria a mecha, analisa o circuito e carrega a solução.
        Certifique-se que o arquivo termina em `.FEM`.
        """
        if not file_name.endswith('.FEMM'):
            file_name += '.FEMM'

        folder = Path('femm').resolve()
        if not folder.exists():
            folder.mkdir()

        # Salva, cria a mecha e analisa a solução.
        femm.mi_saveas(str(folder / file_name))
        femm.mi_createmesh()
        femm.mi_analyze()
        femm.mi_loadsolution()

    def update_freq(self, freq: int) -> Self:
        self.freq = freq
        return self.update()


@dataclass(init=False)
class ProblemBuilder:
    """
    Responsável por definir, salvar e resolver o problema. Os valores
    padrão são os mesmos do FEMM. Ao instanciar esta classe, um novo
    arquivo será aberto e as variáveis do problema serão automaticamente
    definidas.
    """

    def __init__(
        self,
        doc_type: DocType,
    ) -> None:
        """
        Tipo de documeto.

        `'magnetics'` : magnético
        `'electrostatics'` : eletrostático
        `'heat flow'` : fluxo de calor
        `'current flow'` : fluxo de corrente
        """
        self.doc_type: DocType = doc_type
        self.freq: int = 0
        self.unit = Unit('inches')
        self.type: ProblemType = 'planar'
        self.precision: float = 1e-8
        self.depth: int = 1
        self.min_angle: int = 30
        self.arc_solver: ArcSolver = 'successive approximation'

    def with_freq(self, freq: int) -> Self:
        """Frequência."""
        self.freq = freq
        return self

    def with_unit(self, unit: UnitLike) -> Self:
        """
        Unidade de medida das distâncias.

        `'inches'` : polegadas
        `'millimeters'` : milímetros
        `'centimeters'` : centímetros
        `'mils'` : mils (milésimo de polegada)
        `'meters'` : metros
        """
        if isinstance(unit, Unit):
            self.unit = unit
        else:
            self.unit = Unit(unit)

        return self

    def with_type(self, type: ProblemType) -> Self:
        """
        Tipo do problema.

        `'planar'` : 2D
        `'axi'` : 3D
        """
        self.type = type
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
        Método de resolução dos arcos.

        `'succesive approximation'`: aproximações sucessivas
        `'newton'` : método de Newton
        """
        self.arc_solver = arc_solver
        return self

    def build(self):
        """
        Abre um novo documento no modo definido por `Problem.doctype` e
        define as variáveis do problema.
        """
        match self.doc_type:
            case 'magnetics':
                femm.newdocument(0)
            case 'electrostatics':
                femm.newdocument(1)
            case 'heat flow':
                femm.newdocument(2)
            case 'current flow':
                femm.newdocument(3)

        problem = Problem(
            self.freq,
            self.unit,
            self.type,
            self.precision,
            self.depth,
            self.min_angle,
            self.arc_solver,
        ).update()

        return problem

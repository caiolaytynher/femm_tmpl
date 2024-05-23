import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import femm

from femmlib.shape import Circle
from femmlib.state import State
from femmlib.types import ArcSolver, DocType, Group, ProbType, Unit
from mathlib.vector2 import LEFT, RIGHT, Vector2, Vector2Like

CONV_RATE: dict[Unit, float] = {
    'inches': 0.0254,
    'millimeters': 0.001,
    'centimeters': 0.01,
    'mils': 2.54e-5,
    'meters': 1,
    'micrometers': 1e-6,
}

FEMM_FOLDER = Path('femm').resolve()


@dataclass
class FEMM:
    doc_type: DocType
    freq: float = 0
    unit: Unit = 'inches'
    type: ProbType = 'planar'
    precision: float = 1e-8
    depth: float = 1
    min_angle: float = 30
    arc_solver: ArcSolver = 'successive approximations'
    groups: set[Group] = field(default_factory=set, init=False)

    def __post_init__(self) -> None:
        self.state = State(
            self.doc_type,
            self.freq,
            self.depth * CONV_RATE[self.unit],
            CONV_RATE[self.unit],
        )

    def save(self, file_name: str) -> Self:
        if not FEMM_FOLDER.exists():
            FEMM_FOLDER.mkdir()

        file = FEMM_FOLDER / (
            file_name if file_name.endswith('.FEM') else f'{file_name}.FEM'
        )

        match self.doc_type:
            case 'magnetics':
                femm.mi_saveas(str(file))
            case _:
                raise NotImplementedError(
                    f'Missing implementation for {self.doc_type}.'
                )

        return self

    def define_problem(self) -> Self:
        match self.doc_type:
            case 'magnetics':
                femm.mi_probdef(
                    self.freq,
                    self.unit,
                    self.type,
                    self.precision,
                    self.depth,
                    self.min_angle,
                    1 if self.arc_solver == 'newton' else 0,
                )
            case _:
                raise NotImplementedError(
                    f'Missing implementation for {self.doc_type}.'
                )

        return self

    @contextmanager
    def new(self, file_name: str, *, delay: float = 0) -> Iterator[None]:
        try:
            femm.openfemm()

            match self.doc_type:
                case 'magnetics':
                    femm.newdocument(0)
                case 'electrostatics':
                    femm.newdocument(1)
                case 'heat flow':
                    femm.newdocument(2)
                case 'current flow':
                    femm.newdocument(3)

            self.define_problem()
            yield
            if delay > 0:
                time.sleep(delay)
        finally:
            self.save(file_name)
            femm.closefemm()

    @contextmanager
    def open(self, file_name: str, *, delay: float = 0) -> Iterator[None]:
        assert file_name.endswith('.FEM') or file_name.endswith('.ans')

        file = Path('femm').resolve() / file_name
        if not file.exists():
            raise ReferenceError(f'File does not exists: {file}.')

        try:
            femm.openfemm()
            femm.opendocument(str(file))
            yield
            if delay > 0:
                time.sleep(delay)
        finally:
            femm.closefemm()

    def solve(self) -> Self:
        match self.doc_type:
            case 'magnetics':
                femm.mi_createmesh()
                femm.mi_analyze()
                femm.mi_loadsolution()
            case _:
                raise NotImplementedError(
                    f'Missing implementation for {self.doc_type}.'
                )

        return self

    def update_freq(self, freq: float) -> Self:
        self.freq = freq
        self.state.freq = freq
        return self.define_problem()

    def update_depth(self, depth: float) -> Self:
        self.depth = depth
        self.state.depth = depth
        return self.define_problem()

    def new_group(self) -> Group:
        group = max(self.groups) + 1 if len(self.groups) > 0 else 1
        self.groups.add(group)
        return group

    def circle(self, center: Vector2Like, radius: float) -> Circle:
        center = Vector2.parse(center)
        left = center + LEFT * radius
        right = center + RIGHT * radius
        node_group = self.new_group()
        arc_group = self.new_group()
        lower_arc = (left - center).perpendicular() + center
        upper_arc = (right - center).perpendicular() + center

        match self.doc_type:
            case 'magnetics':
                femm.mi_drawarc(*left, *right, angle=180, maxseg=1)
                femm.mi_addarc(*right, *left, angle=180, maxseg=1)

                femm.mi_selectnode(*left)
                femm.mi_selectnode(*right)
                femm.mi_setgroup(node_group)
                femm.mi_clearselected()

                femm.mi_selectarcsegment(*lower_arc)
                femm.mi_selectarcsegment(*upper_arc)
                femm.mi_setgroup(arc_group)
                femm.mi_clearselected()
            case _:
                raise NotImplementedError(
                    f'Missing implementation for {self.doc_type}.'
                )

        return Circle(
            nodes=[left, right],
            arc_group=arc_group,
            node_group=node_group,
            state=self.state,
        )

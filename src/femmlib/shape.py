from dataclasses import dataclass
from typing import Literal, Self

import femm

from femmlib.state import State
from femmlib.types import Group
from mathlib.vector2 import Vector2


@dataclass
class Circle:
    nodes: list[Vector2]
    arc_group: Group
    node_group: Group
    state: State

    def select(self, mode: Literal['arc', 'node']) -> Self:
        match self.state.doc_type:
            case 'magnetics':
                femm.mi_selectgroup(
                    self.arc_group if mode == 'arc' else self.node_group
                )
            case _:
                raise NotImplementedError(
                    f'Missing implementation for {self.state.doc_type}.'
                )

        return self

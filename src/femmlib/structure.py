from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Self

import femm
from block import Block
from electromagnetics import VACUUM_PERMEABILITY
import vec
from vec import Vec2, Vec2Like, to_vec2

type ConnectMethod = Literal["open loop", "closed loop", "circle"]


class StructureBuilder:
    def __init__(self, nodes: list[Vec2Like], material: Block) -> None:
        self.nodes = [to_vec2(node) for node in nodes]
        self.material = material
        self.connect_method: ConnectMethod = "open loop"

    def with_connect_method(self, connect_method: ConnectMethod) -> Self:
        self.connect_method = connect_method
        return self

    def build(self) -> Structure:
        """Posiciona e liga os nós da estrutura."""
        for node in self.nodes:
            femm.mi_addnode(*node)

        match self.connect_method:
            case "open loop":
                for node, next_node in zip(self.nodes, self.nodes[1:]):
                    femm.mi_addsegment(*node, *next_node)
            case "closed loop":
                for node, next_node in zip(self.nodes, self.nodes[1:]):
                    femm.mi_addsegment(*node, *next_node)

                femm.mi_addsegment(*self.nodes[0], *self.nodes[-1])
            case "circle":
                assert (
                    len(self.nodes) == 2
                ), "To create a circle, there must only be 2 nodes."

                # Liga os nós nos dois sentidos.
                femm.mi_addarc(*self.nodes[0], *self.nodes[1], angle=180, maxseg=1)
                femm.mi_addarc(*self.nodes[1], *self.nodes[0], angle=180, maxseg=1)
            case _:
                raise ValueError("Connect method does not exist.")

        return Structure(self.nodes, self.material, self.connect_method)


@dataclass
class Structure:
    """
    Assume que as coordenadas providas estão na ordem em que os nós serão
    ligados.

    - `nodes`: Lista de coordenadas dos nós que compôem a estrutura;
    - `material`: Material que representa a estrutura.
    - `connect_method`: Método de conectar os nós. Valores: "open loop", "closed
    loop", "circle". Valor padrão: "open loop".
    """

    nodes: list[Vec2]
    material: Block
    connect_method: ConnectMethod

    @staticmethod
    def builder(nodes: list[Vec2Like], material: Block) -> StructureBuilder:
        return StructureBuilder(nodes, material)

    def select(self) -> None:
        first = self.nodes[0]
        last = self.nodes[-1]

        match self.connect_method:
            case "open loop":
                for node, next_node in zip(self.nodes, self.nodes[1:]):
                    femm.mi_selectsegment(*vec.midpoint(node, next_node))
            case "closed loop":
                for node, next_node in zip(self.nodes, self.nodes[1:]):
                    femm.mi_selectsegment(*vec.midpoint(node, next_node))

                femm.mi_selectsegment(*vec.midpoint(first, last))
            case "circle":
                radius = vec.distance(first, last) / 2
                center = vec.midpoint(first, last)

                if first.y == last.y:
                    first_arc = center + vec.UP * radius
                    second_arc = center + vec.DOWN * radius
                else:
                    first_arc = center + vec.LEFT * radius
                    second_arc = center + vec.RIGHT * radius

                femm.mi_selectarcsegment(*first_arc)
                femm.mi_selectarcsegment(*second_arc)

    def set_turns(self, turns: int) -> None:
        self.material.turns = turns
        self.material.update_props()

    def invert_winding_polarity(self) -> None:
        self.material.turns *= -1
        self.material.update_props()

    def permeability(self) -> Vec2:
        """
        Retorna a permeabilidade do material.

        A permeabilidade no FEMM tem direção x e y, portanto a função retorna um
        vetor. Funciona apenas na fase de pós processamento, i.e. após chamar
        `Problem.solve()`.
        """
        return Vec2(*femm.mo_getmu(*self.material.position)) * VACUUM_PERMEABILITY

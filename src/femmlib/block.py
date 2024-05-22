from dataclasses import dataclass
from typing import Literal, Self

import femm

from mathlib.vector2 import Vector2, Vector2Like

type MaterialName = Literal[
    'Air', 'Pure Iron', '18 AWG', '1010 Steel', 'M-45 Steel'
]


@dataclass
class Block:
    """
    Propriedades do material.
    """

    name: MaterialName
    position: Vector2
    auto_mesh: bool
    mesh_size: float
    circuit_name: str
    magnetization_direction: float
    group: int
    turns: int

    def update(self) -> None:
        """
        Seleciona um rótulo existente na posição `Block.position` e atualiza as
        propriedades nele.
        """
        femm.mi_selectlabel(*self.position)

        # Define as propriedades do material. Assume que as propriedades estão
        # na ordem que `mi_setblockprop()` necessita.
        femm.mi_setblockprop(
            self.name,
            int(self.auto_mesh),
            self.mesh_size,
            self.circuit_name,
            self.magnetization_direction,
            self.group,
            self.turns,
        )
        femm.mi_clearselected()


class BlockBuilder:
    def __init__(self, name: MaterialName, position: Vector2Like):
        self.name: MaterialName = name
        self.position = Vector2.parse(position)
        self.auto_mesh: bool = True
        self.mesh_size: float = 0
        self.circuit_name: str = ''
        self.magnetization_direction: float = 0
        self.group: int = 0
        self.turns: int = 1

    def with_position(self, x: float, y: float) -> Self:
        self.position = Vector2(x, y)
        return self

    def with_mesh_size(self, mesh_size: float) -> Self:
        """Tamanho da mecha. Valor padrão: 0."""
        self.mesh_size = mesh_size
        self.auto_mesh = False
        return self

    # TODO: Ver se não vale a pena receber um circuito inteiro.
    def with_circuit_name(self, circuit_name: str) -> Self:
        """Nome do circuito o qual o bloco faz parte."""
        self.circuit_name = circuit_name
        return self

    def with_magnetization_direction(
        self, magnetization_direction: float
    ) -> Self:
        """Direção do ângulo de magnetização em graus. Valor padrão: 0."""
        self.magnetization_direction = magnetization_direction
        return self

    def with_group(self, group: int) -> Self:
        """Número do grupo o qual o bloco faz parte. Valor padrão: 0."""
        self.group = group
        return self

    def with_turns(self, turns: int) -> Self:
        """Número de voltas da bobina. Valor padrão: 1."""
        self.turns = turns
        return self

    def build(self) -> Block:
        femm.mi_getmaterial(self.name)
        femm.mi_addblocklabel(*self.position)

        block = Block(
            self.name,
            self.position,
            self.auto_mesh,
            self.mesh_size,
            self.circuit_name,
            self.magnetization_direction,
            self.group,
            self.turns,
        )
        block.update()

        return block

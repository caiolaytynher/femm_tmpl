from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Self

import femm
import vec
from vec import Vec2, Vec2Like, to_vec2
from problem import Unit

type Direction = Literal["horizontal", "vertical"]


class AirGapBuilder:
    def __init__(
        self,
        upper_left: Vec2Like,
        upper_right: Vec2Like,
        lower_left: Vec2Like,
        lower_right: Vec2Like,
    ) -> None:
        self.upper_right = to_vec2(upper_right)
        self.upper_left = to_vec2(upper_left)
        self.lower_right = to_vec2(lower_right)
        self.lower_left = to_vec2(lower_left)
        self.direction: Direction = "vertical"

    def with_direction(self, direction: Direction) -> Self:
        self.direction = direction
        return self

    def build(self) -> AirGap:
        return AirGap(
            self.upper_left,
            self.upper_right,
            self.lower_left,
            self.lower_right,
            self.direction,
        )


@dataclass
class AirGap:
    """
    Representa o entreferro.

    Responsável por calcular o tamanho, a área da secção transversal, o ponto
    central e por alterar o tamanho. Todos os argumentos são passados como
    similares a vetores, mas são convertidos para vetores quando o objeto é
    construído.

    Entreferros geralmente consistem de 4 nós, mas eles podem ser verticais ou
    horizontais. Por isso, existe uma variável de estado para especificar qual a
    direção. Isso alterará a forma com que certas funções são executadas.

    - `upper_right`: Nó superior direito;
    - `upper_left`: Nó superior esquerdo;
    - `lower_right`: Nó inferior direito;
    - `lower_left`: Nó inferior esquerdo;
    - `direction`: Direção que o entreferro cresce. "horizontal" para horizontal
    e "vertical" para vertical.
    """

    upper_left: Vec2
    upper_right: Vec2
    lower_left: Vec2
    lower_right: Vec2
    direction: Direction

    @staticmethod
    def builder(
        *,
        upper_left: Vec2Like,
        upper_right: Vec2Like,
        lower_left: Vec2Like,
        lower_right: Vec2Like,
    ) -> AirGapBuilder:
        return AirGapBuilder(upper_left, upper_right, lower_left, lower_right)

    def length(self) -> float:
        """Computa e retorna o tamanho do entreferro."""
        # Se o entreferro for horizontal, calcule a distância entre os pontos
        # superior direito e esquerdo. Caso contrário dos pontos superior
        # e inferior esquerdo. Naturalmente, os pontos simétricos também
        # poderiam ter sido utilizados.
        if self.direction == "horizontal":
            return vec.distance(self.upper_right, self.upper_left)

        return vec.distance(self.upper_left, self.lower_left)

    def thickness(self) -> float:
        """Computa e retorna a grossura do entreferro."""
        if self.direction == "horizontal":
            return vec.distance(self.upper_left, self.lower_left)

        return vec.distance(self.upper_right, self.upper_left)

    def center(self) -> Vec2:
        """
        Computa e retorna um vetor contendo as coordenadas do cenro do
        entreferro.
        """
        # Coordenada x do ponto médio entre canto superior esquerdo e direito e
        # y do canto superior esquerdo e inferior esquerdo.
        return Vec2(
            vec.midpoint(self.upper_left, self.upper_right).x,
            vec.midpoint(self.upper_left, self.lower_left).y,
        )

    def cross_sectional_area(self, depth: float, units: Unit) -> float:
        """
        Computa e retorna o valor da área da secção transversal do entreferro.
        """
        # Calcula a grossura em metros dependendo da direção do entreferro.
        if self.direction == "horizontal":
            thickness = units.to_meters(vec.distance(self.upper_left, self.lower_left))
        else:
            thickness = units.to_meters(vec.distance(self.upper_left, self.upper_right))

        # Profundidade em metros
        depth = units.to_meters(depth)

        return depth * thickness

    def increment(self, amount: float) -> None:
        """
        Muda o tamanho do entreferro deslocando os pontos na direção
        especificada por uma quantidade definida por `amount`. Se `amount` for
        positivo, o entreferro cresce, se for negativo, diminui.
        """
        if self.direction == "horizontal":
            for x, y in (self.upper_right, self.lower_right):
                femm.mi_selectnode(x, y)
            amount_vec = vec.RIGHT * amount / 2
            femm.mi_movetranslate(*amount_vec)
            femm.mi_clearselected()

            for x, y in (self.upper_left, self.lower_left):
                femm.mi_selectnode(x, y)
            femm.mi_movetranslate(*(vec.LEFT * amount / 2))
            femm.mi_clearselected()
        else:
            for x, y in (self.upper_right, self.upper_left):
                femm.mi_selectnode(x, y)
            femm.mi_movetranslate(*(vec.UP * amount / 2))
            femm.mi_clearselected()

            for x, y in (self.lower_right, self.lower_left):
                femm.mi_selectnode(x, y)
            femm.mi_movetranslate(*(vec.DOWN * amount / 2))
            femm.mi_clearselected()

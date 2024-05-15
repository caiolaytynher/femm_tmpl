import math
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Literal, Self

type Vector2Like = Vector2 | Sequence[float]


@dataclass(slots=True)
class Vector2:
    """
    Representa um vetor 2D em coordenadas cartesianas no formato (x, y).
    """

    x: float
    y: float

    def __iter__(self) -> Iterator[float]:
        """Define o vetor como uma classe iterável."""
        yield self.x
        yield self.y

    def __len__(self) -> Literal[2]:
        """Define o tamanho de um objeto de classe vetor."""
        return 2

    @classmethod
    def parse(cls, vec: Vector2Like) -> Self:
        """
        Converte um objeto similar a um vetor no próprio vetor.

        Condições:
        - Ser uma sequência de `float`s;
        - Possuir tamanho 2.
        """
        if isinstance(vec, Sequence):
            assert len(vec) == 2, 'O tamanho precisa ser 2.'

        return cls(*vec)

    def __add__(self, other: Vector2Like) -> Self:
        """Define a soma de um vetor com um similar. Retorna um vetor."""
        other = self.parse(other)

        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2Like) -> Self:
        """Define a subtração de um `Vector2` com um similar."""
        other = self.parse(other)

        return self.__class__(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Self:
        """Define o negativo de um `Vector2`."""
        return self.__class__(-self.x, -self.y)

    def __mul__(self, other: float) -> Self:
        """Define a multiplicação de um `Vector2` por um escalar."""
        return self.__class__(self.x * other, self.y * other)

    def __truediv__(self, other: float) -> Self:
        """Define a divisão de um `Vector2` por um escalar."""
        return self.__class__(self.x / other, self.y / other)

    def magnitude(self) -> float:
        """Retorna a magnitude do vetor."""
        return math.sqrt(self.x**2 + self.y**2)

    def direction(self) -> Self:
        """Retorna um versor que aponta na mesma direção que o vetor."""
        return self / self.magnitude()

    def perpendicular(
        self,
        direction: Literal['clockwise', 'counterclockwise'] = 'clockwise',
    ) -> Self:
        """
        Retorna o vetor girado na perpendicular na direção especificada.

        `direction` : `'clockwise'` ou `'counterclockwise'`
            Especifica a direção que o vetor deve girar. (Padrão:
            `'clockwise'`)
        """
        x, y = self
        match direction:
            case 'clockwise':
                return self.__class__(-y, x)
            case 'counterclockwise':
                return self.__class__(y, -x)

    @classmethod
    def dot(cls, vec: Vector2Like, other: Vector2Like) -> float:
        """Retorna o produto escalar entre dois vetores."""
        vec = cls.parse(vec)
        other = cls.parse(other)

        return vec.x * other.x + vec.y * other.y

    @classmethod
    def distance(cls, vec: Vector2Like, other: Vector2Like) -> float:
        """Retorna a distância entre dois vetores."""
        vec = cls.parse(vec)
        other = cls.parse(other)

        return (vec - other).magnitude()

    @classmethod
    def midpoint(cls, vec: Vector2Like, other: Vector2Like) -> Self:
        """Retorna o ponto médio entre dois vetores."""
        vec = cls.parse(vec)
        other = cls.parse(other)

        return cls.parse((other + vec) / 2)


UP = Vector2(0, 1)
DOWN = Vector2(0, -1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
ZERO = Vector2(0, 0)

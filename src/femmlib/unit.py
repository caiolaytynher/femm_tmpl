from dataclasses import dataclass
from typing import Literal

type Name = Literal[
    'inches',
    'millimeters',
    'centimeters',
    'mils',
    'meters',
]

CONVERSION_RATE: dict[Name, float] = {
    'centimeters': 0.01,
    'inches': 0.0254,
    'meters': 1,
    'millimeters': 0.001,
    'mils': 2.54e-5,
}


@dataclass
class Unit:
    name: Name

    def to_meters(self, value: float) -> float:
        """
        Converte para metros o valor do argumento `value` baseado na
        definição de `unit` do problema. Feito para ser utilizado com
        medidas retiradas do FEMM.
        """

        return value * CONVERSION_RATE[self.name]

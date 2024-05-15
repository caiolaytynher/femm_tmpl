from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Iterator, Self

import femm

type CircuitType = Literal[0, 1]


@dataclass
class CircuitProps:
    """
    Propriedades do circuito.

    Resultado da função `mo_getcircuitproperties()` com adicionais que ajudam a
    obter mais informações acerca do circuito.

    - `current`: Corrente;
    - `voltage`: Tensão;
    - `flux_linkage`: Fluxo concatenado.
    """

    current: float
    voltage: float
    flux_linkage: float

    def __iter__(self) -> Iterator[float]:
        """
        Permite utilizar um objeto da classe `CircuitProps` como um iterador.
        """
        yield self.current
        yield self.voltage
        yield self.flux_linkage

    def __len__(self) -> int:
        """Define o tamanho do objeto."""
        return 3

    def with_extension(self, turns: int, area: float) -> CircuitPropsExtended:
        return CircuitPropsExtended(
            self.current,
            self.voltage,
            self.flux_linkage,
            flux=(flux := self.flux_linkage / turns),
            mmf=(mmf := turns * self.current),
            reluctance=mmf / flux,
            flux_density=flux / area,  # Valor aproximado devido à área.
            inductance=self.flux_linkage / self.current,
        )


@dataclass
class CircuitPropsExtended:
    current: float
    voltage: float
    flux_linkage: float
    flux: float
    mmf: float
    reluctance: float
    flux_density: float
    inductance: float

    def __iter__(self) -> Iterator[float]:
        yield self.current
        yield self.voltage
        yield self.flux_linkage
        yield self.flux
        yield self.mmf
        yield self.reluctance
        yield self.flux_density
        yield self.inductance

    def __len__(self) -> int:
        return 8


class CircuitBuilder:
    def __init__(self, name: str, current: float) -> None:
        self.name = name
        self.current = current
        self.type: CircuitType = 1

    def with_name(self, name: str) -> Self:
        self.name = name
        return self

    def with_parallel(self) -> Self:
        self.type = 0
        return self

    def with_series(self) -> Self:
        self.type = 1
        return self

    def build(self) -> Circuit:
        femm.mi_addcircprop(self.name, self.current, self.type)
        return Circuit(self.name, self.current, self.type)


@dataclass
class Circuit:
    """
    Características do circuito.

    - `pname`: Nome do circuito;
    - `ic`: Corrente do circuito;
    - `ptype`: Tipo do circuito. 0 para paralelo e 1 para série.
    """

    name: str
    current: float
    type: CircuitType

    @staticmethod
    def builder(name: str, current: float) -> CircuitBuilder:
        return CircuitBuilder(name, current)

    def set_current(self, current: float) -> None:
        femm.mi_setcurrent(self.name, current)

        self.current = current

    def props(self) -> CircuitProps:
        """
        Retorna um objeto do tipo `CircuitProps`. Pode ser desempacotado em
        corrente, tensão e fluxo concatenado.
        """
        props: tuple[float, ...] = femm.mo_getcircuitproperties(self.name)  # type: ignore
        return CircuitProps(*props)

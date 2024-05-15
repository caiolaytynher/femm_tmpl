from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Self

import femm
from vec import Vec2Like
from structure import Structure

type BoundaryFormat = Literal[0, 1, 2, 3, 4, 5, 6, 7]


class BoundaryBuilder:
    def __init__(self, name: str, structure: Structure) -> None:
        self.name = name
        self.structure = structure

        # Propriedades de fronteira.
        self.mag_vec_potential = (0.0, 0.0, 0.0)
        self.flux = 0.0
        self.permeability = 0.0
        self.conductivity = 0.0
        self.normal_component = 0.0
        self.tangential_component = 0.0
        self.boundary_format: BoundaryFormat = 0
        self.inner_angle = 0.0
        self.outer_angle = 0.0

        # Propriedades de segmento de reta/arco.
        self.max_segment_deg = 1.0
        self.element_size = 0.0
        self.auto_mesh: bool = True
        self.hide: bool = False
        self.group: int = 0

    def with_prescribed_mag_vec_potential(
        self, mag_vec_potential: tuple[float, float, float], flux: float
    ) -> Self:
        self.mag_vec_potential = mag_vec_potential
        self.flux = flux
        return self

    def with_small_skin_depth(self, permeability: float, conductivity: float) -> Self:
        """
        - `permeability`: Permeabilidade magnética;
        - `conductivity`: Condutividade magnética em MS/m.
        """
        self.permeability = permeability
        self.conductivity = conductivity
        self.boundary_format = 1
        return self

    def with_mixed_boundary_conditions(
        self, normal_component: float, tangential_component: float
    ) -> Self:
        self.normal_component = normal_component
        self.tangential_component = tangential_component
        self.boundary_format = 2
        return self

    def with_strategic_dual_image(self) -> Self:
        self.boundary_format = 3
        return self

    def with_periodic(self) -> Self:
        self.boundary_format = 4
        return self

    def with_anti_periodic(self) -> Self:
        self.boundary_format = 5
        return self

    def with_periodic_air_gap(self, inner_angle: float, outer_angle: float) -> Self:
        """
        - `inner_angle`: Ângulo interno da borda em graus;
        - `outer_angle`: Ângulo externo da borda em graus.
        """
        self.inner_angle = inner_angle
        self.outer_angle = outer_angle
        self.boundary_format = 6
        return self

    def with_anti_periodic_air_gap(
        self, inner_angle: float, outer_angle: float
    ) -> Self:
        """
        - `inner_angle`: Ângulo interno da borda em graus;
        - `outer_angle`: Ângulo externo da borda em graus.
        """
        self.inner_angle = inner_angle
        self.outer_angle = outer_angle
        self.boundary_format = 7
        return self

    def with_arc_segment_props(
        self,
        max_segment_deg: float = 1.0,
        hide: bool = False,
        group: int = 0,
    ) -> Self:
        self.max_segment_deg = max_segment_deg
        self.hide = hide
        self.group = group
        return self

    def with_segment_props(
        self,
        element_size: float = 0.0,
        hide: bool = False,
        group: int = 0,
    ) -> Self:
        self.hide = hide
        self.group = group
        if element_size != self.element_size:
            self.auto_mesh = False
            self.element_size = element_size
        return self

    def build(self) -> Boundary:
        femm.mi_addboundprop(
            self.name,
            self.mag_vec_potential[0],
            self.mag_vec_potential[1],
            self.mag_vec_potential[2],
            self.flux,
            self.permeability,
            self.conductivity,
            self.normal_component,
            self.tangential_component,
            self.inner_angle,
            self.outer_angle,
        )

        self.structure.select()
        if self.structure.connect_method == "circle":
            femm.mi_setarcsegmentprop(
                self.max_segment_deg,
                self.name,
                int(self.hide),
                self.group,
            )
        else:
            femm.mi_setsegmentprop(
                self.name,
                self.element_size,
                self.auto_mesh,
                self.hide,
                self.group,
            )
        femm.mi_clearselected()

        return Boundary(
            self.name,
            BoundaryProps(
                self.mag_vec_potential,
                self.flux,
                self.permeability,
                self.conductivity,
                self.normal_component,
                self.tangential_component,
                self.boundary_format,
                self.inner_angle,
                self.outer_angle,
            ),
        )


@dataclass
class BoundaryProps:
    mag_vec_potential: tuple[float, float, float]
    flux: float
    permeability: float
    conductivity: float
    normal_component: float
    tangential_component: float
    boundary_format: float
    inner_angle: float
    outer_angle: float


@dataclass
class Boundary:
    """
    Propriedades da fronteira.

    O valor das outras propriedades fora `Boundary.propname` são irrelevantes
    por enquanto. Recomenda-se manter o valor padrão.
    """

    name: str
    props: BoundaryProps

    @staticmethod
    def builder(name: str, structure: Structure) -> BoundaryBuilder:
        return BoundaryBuilder(name, structure)

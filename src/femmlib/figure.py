from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Self

import femm
from helpers import PathLike, to_path

type VectorPlotType = Literal[0, 1, 2, 3, 4, 5, 6]
type DensityPlotType = Literal[
    "bmag",
    "breal",
    "bimag",
    "logb",
    "hmag",
    "hreal",
    "himag",
    "jmag",
    "jreal",
    "jimag",
]


class FigureBuilder:
    def __init__(self) -> None:
        self.density_plot_type: DensityPlotType = "bmag"
        self.legend: bool = False
        self.gray_scale: bool = False
        self.density_upper_bound = 1.0
        self.density_lower_bound = 0.0
        self.vector_plot_type: VectorPlotType = 0
        self.arrow_scale_factor = 1.0

    def with_density_plot_type(self, plot_type: DensityPlotType) -> Self:
        """
        - `plot_type`: O tipo de plotagem de densidade. Valor padrão: "bmag".
                - `"bmag"`: Magnitude da densidade de fluxo;
                - `"breal"`: Componente real da densidade de fluxo;
                - `"bimag"`: Componente imaginária da densidade de fluxo;
                - `"logb"`: Magnitude logarítmica da densidade de fluxo;
                - `"hmag"`: Magnitude do campo magnético;
                - `"hreal"`: Componente real da campo magnético;
                - `"himag"`: Componente imaginária da campo magnético;
                - `"jmag"`: Magnitude da densidade de corrente;
                - `"jreal"`: Componente real da densidade de corrente;
                - `"jimag"`: Componente imaginária da densidade de corrente.
        """
        self.density_plot_type = plot_type
        return self

    def with_legend(self) -> Self:
        """Legenda da plotagem. Valor padrão: Falso."""
        self.legend = True
        return self

    def with_gray_scale(self) -> Self:
        """
        Muda a escala de cor da plotagem para preto e branco. Por padrão é
        colorido.
        """
        self.gray_scale = True
        return self

    def with_density_display_bounds(self, lower: float, upper: float) -> Self:
        """
        - `lower`: Menor valor a ser mostrado na plotagem de densidade. Valor
        padrão: 0.0;
        - `upper`: Maior valor a ser mostrado na plotagem de densidade. Valor
        padrão: 1.0.
        """
        self.density_upper_bound = upper
        self.density_lower_bound = lower
        return self

    def with_vector_plot_type(self, plot_type: VectorPlotType) -> Self:
        """
        - `plot_type`: Tipo do plot de vetor. Valor padrão: 0;
                - 0: Sem plot de vetor;
                - 1: Parte real da densidade de fluxo;
                - 2: Parte real do campo magnético;
                - 3: Parte imaginária da densidade de fluxo;
                - 4: Parte imaginária do campo magnético;
                - 5: Ambas as partes real e imaginária da densidade de fluxo;
                - 6: Ambas as partes real e imaginária do campo magnético.
        """
        self.vector_plot_type = plot_type
        return self

    def with_arrow_scale_factor(self, scale_factor: float) -> Self:
        """
        - `scale_factor`: Fator de escala dos vetores. Valor padrão: 1.0.
        """
        self.arrow_scale_factor = scale_factor
        return self

    def build(self) -> Figure:
        return Figure(
            self.density_plot_type,
            self.legend,
            self.gray_scale,
            self.density_upper_bound,
            self.density_lower_bound,
            self.vector_plot_type,
            self.arrow_scale_factor,
        )


@dataclass
class Figure:
    density_plot_type: DensityPlotType
    legend: bool
    gray_scale: bool
    density_upper_bound: float
    density_lower_bound: float
    vector_plot_type: VectorPlotType
    arrow_scale_factor: float

    @staticmethod
    def builder() -> FigureBuilder:
        return FigureBuilder()

    def save(self, file: PathLike) -> None:
        """
        - `file`: Nome ou caminho do arquivo .png. Se o caminho possuir uma
        pasta não existente antes do nome do arquivo, a pasta será criada.
        """
        file = to_path(file)

        femm.mi_zoomnatural()
        femm.mo_showvectorplot(self.vector_plot_type, self.arrow_scale_factor)
        femm.mo_showdensityplot(
            int(self.legend),
            int(self.gray_scale),
            self.density_upper_bound,
            self.density_lower_bound,
            self.density_plot_type,
        )
        femm.mo_savebitmap(str(file))

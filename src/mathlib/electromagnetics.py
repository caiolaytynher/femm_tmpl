import math
from dataclasses import dataclass

VACUUM_PERMEABILITY = 4e-7 * math.pi


@dataclass
class EMProps:
    reluctance: float
    mmf: float
    flux: float
    flux_density: float
    flux_linkage: float
    inductance: float


def props(
    area: float,
    turns: int,
    current: float,
    gap_length: float,
    core_length: float,
    core_permeability: float,
) -> EMProps:
    core_reluctance = core_length / (area * core_permeability)
    gap_reluctance = gap_length / (area * VACUUM_PERMEABILITY)

    return EMProps(
        reluctance=(reluctance := core_reluctance + gap_reluctance),
        mmf=(mmf := turns * current),
        flux=(flux := mmf / reluctance),
        flux_density=flux / area,
        flux_linkage=(flux_linkage := flux * turns),
        inductance=flux_linkage / current,
    )

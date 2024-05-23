from typing import Literal

type Unit = Literal[
    'inches',
    'millimeters',
    'centimeters',
    'mils',
    'meters',
    'micrometers',
]

type DocType = Literal[
    'magnetics',
    'electrostatics',
    'heat flow',
    'current flow',
]
type ProbType = Literal['planar', 'axi']
type ArcSolver = Literal['successive approximations', 'newton']
type Group = int

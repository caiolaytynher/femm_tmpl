from dataclasses import dataclass

from femmlib.types import DocType


@dataclass
class State:
    doc_type: DocType
    freq: float
    depth: float
    conv_rate: float

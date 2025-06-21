from dataclasses import dataclass
from ..layer import QCLayer, StandardGateLayer, MeasurementLayer, BarrierLayer, MeasurementBranch

class Chunk:
    layers: list[QCLayer]

@dataclass
class StandardGateChunk(Chunk):
    layers: list[StandardGateLayer]

@dataclass
class MeasurementChunk(Chunk):
    layers: list[MeasurementLayer]

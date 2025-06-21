from .base import Chunk, BarrierLayer, StandardGateChunk

class CircuitBackend:

    def __init__(self, chunks: list[Chunk|BarrierLayer], num_qubits: int):
        self.chunks = chunks
        self.num_qubits = num_qubits
        self.label_to_idx = self._build_label_index()

    def _build_label_index(self) -> dict[str, int]:
        label_map = {}
        for i, chunk in enumerate(self.chunks):
            if isinstance(chunk, BarrierLayer) and chunk.label is not None:
                if chunk.label in label_map:
                    raise ValueError(f"Duplicate barrier label: {chunk.label}")
                label_map[chunk.label] = i
        return label_map
    
    def _resolve_barrier(self, label: str | None) -> int:
        if label is None or label == 'None':
            raise ValueError("Cannot resolve a barrier with label=None")
        for idx, chunk in enumerate(self.chunks):
            if isinstance(chunk, BarrierLayer) and chunk.label == label:
                return idx
        raise KeyError(f"Barrier with label '{label}' not found")
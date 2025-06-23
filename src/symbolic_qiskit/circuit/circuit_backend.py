import sympy as sp

from .base import Chunk, BarrierLayer, StandardGateChunk, MeasurementChunk

class CircuitBackend:

    def __init__(self, 
        chunks: list[Chunk|BarrierLayer],
        num_qubits: int,
        simplify_on_build: bool,
        global_phase: float|sp.Expr
    ):
        self.chunks = chunks
        self.num_qubits = num_qubits
        self.label_to_idx: dict[str, int] = self._build_label_index()
        self.chunk_matrices: list[sp.Matrix | None] = [
            chunk.get_matrix(num_qubits) if isinstance(chunk, StandardGateChunk) else None
            for chunk in chunks]
        
        self.simplify_on_build = simplify_on_build
        self.global_phase = global_phase

    def _build_label_index(self) -> dict[str, int]:
        label_map = {}
        for i, chunk in enumerate(self.chunks):
            if isinstance(chunk, BarrierLayer) and chunk.label is not None:
                if chunk.label in label_map:
                    raise ValueError(f"Duplicate barrier label: {chunk.label}")
                label_map[chunk.label] = i
        return label_map
    
    @property
    def barrier_labels(self) -> list[str]:
        return list(self.label_to_idx.keys())
    
    def _resolve_barrier(self, label: str | None) -> int:
        if label is None or label == 'None':
            raise ValueError("Cannot resolve a barrier with label=None")
        if label not in self.label_to_idx:
            raise KeyError(
                f"Barrier label '{label}' not found. Available labels: {self.barrier_labels}"
            )
        return self.label_to_idx[label]
    
    def unitary(self, start: str | None, end: str | None, simplify: bool) -> sp.Matrix:
        if start is None:
            start_idx = 0
        else:
            start_idx = self._resolve_barrier(start) + 1

        if end is None:
            end_idx = len(self.chunks)
        else:
            end_idx = self._resolve_barrier(end)
        
        for i in range(start_idx, end_idx):
            if isinstance(self.chunks[i], MeasurementChunk):
                raise ValueError(f"Cannot compute unitary: measurement found: {self.chunks[i]}")

        U: sp.Matrix = sp.eye(2 ** self.num_qubits)
        for matrix in self.chunk_matrices[start_idx:end_idx]:
            if matrix is not None:
                U = matrix @ U

        return U.applyfunc(sp.simplify) if simplify else U

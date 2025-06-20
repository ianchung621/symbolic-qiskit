from typing import List

import sympy as sp

from .base import MeasurementBranch, MeasurementLayer
from .utils import state_vector_projection

def branch_on_measurement(
    branch: MeasurementBranch,
    qubit_index: int,
    clbit_index: int
) -> List[MeasurementBranch]:
    """Split a MeasurementBranch into branches conditioned on measuring qubit_index.

    If projection probability is zero, that branch is discarded.
    """
    
    new_branches = []

    for measured_value in (0, 1):
        prob, psi = state_vector_projection(branch.state, qubit_index, measured_value)

        if prob == 0:
            continue

        new_branch = MeasurementBranch(
            measured_bits=branch.measured_bits + (measured_value,),
            prob=branch.prob * prob,
            state=psi,
            clbit_results={**branch.clbit_results, clbit_index: measured_value}
        )
        new_branches.append(new_branch)

    return new_branches

def apply_measurement_layer(
    current_branches: List[MeasurementBranch],
    measurement_layer: MeasurementLayer
) -> List[MeasurementBranch]:
    """
    Apply a MeasurementLayer to current branches, returning all result branches
    after symbolic measurement branching.
    """
    for meas in measurement_layer.ops:
        assert len(meas.q_idxs) == 1 and len(meas.c_idxs) == 1, "Each measurement op must have exactly one qubit and one clbit index"

        q_idx = meas.q_idxs[0]
        c_idx = meas.c_idxs[0]

        new_branches = []
        
        for branch in current_branches:
            children = branch_on_measurement(branch, q_idx, c_idx)
            new_branches.extend(children)

        current_branches = new_branches

    return current_branches
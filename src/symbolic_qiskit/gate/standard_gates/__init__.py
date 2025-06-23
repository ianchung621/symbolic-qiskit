from .i import IGate
from .x import XGate, CXGate
from .y import YGate, CYGate
from .z import ZGate, CZGate
from .h import HGate, CHGate
from .sx import SXGate, SXdgGate, CSXGate, CSXdgGate
from .s import SGate, SdgGate, CSGate, CSdgGate
from .t import TGate, TdgGate, CTGate, CTdgGate
from .swap import SwapGate
from .iswap import iSwapGate
from .dcx import DCXGate
from .ecr import ECRGate
from .u import UGate, CUGate, U1Gate, CU1Gate, U2Gate, CU2Gate, U3Gate, CU3Gate
from .rx import RXGate, CRXGate
from .ry import RYGate, CRYGate
from .rz import RZGate, CRZGate
from .p import PhaseGate, CPhaseGate
from .r import RGate, CRGate
from .rxx import RXXGate
from .ryy import RYYGate
from .rzz import RZZGate


GATE_REGISTRY = {
    'id': IGate,
    'x': XGate,
    'cx': CXGate,
    'y': YGate,
    'cy': CYGate,
    'z': ZGate,
    'cz': CZGate,
    'h': HGate,
    'ch': CHGate,
    'sx': SXGate,
    'sxdg': SXdgGate,
    'csx': CSXGate,
    'csxdg': CSXdgGate,
    's': SGate,
    'sdg': SdgGate,
    'cs': CSGate,
    'csdg': CSdgGate,
    't': TGate,
    'tdg': TdgGate,
    'ct': CTGate,
    'ctdg': CTdgGate,
    'swap': SwapGate,
    'iswap': iSwapGate,
    'dcx': DCXGate,
    'ecr': ECRGate,
    'u': UGate,
    'cu': CUGate,
    'u1': U1Gate,
    'cu1': CU1Gate,
    'u2': U2Gate,
    'cu2': CU2Gate,
    'u3': U3Gate,
    'cu3': CU3Gate,
    'rx': RXGate,
    'crx': CRXGate,
    'ry': RYGate,
    'cry': CRYGate,
    'rz': RZGate,
    'crz': CRZGate,
    'p': PhaseGate,
    'cp': CPhaseGate,
    'r': RGate,
    'cr': CRGate,
    'rxx': RXXGate,
    'ryy': RYYGate,
    'rzz': RZZGate,
}

BASIS_GATES = set(GATE_REGISTRY.keys())
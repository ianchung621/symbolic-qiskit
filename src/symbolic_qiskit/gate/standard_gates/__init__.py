from .i import IGate
from .x import XGate, CXGate, CCXGate
from .y import YGate, CYGate
from .z import ZGate, CZGate, CCZGate
from .h import HGate, CHGate
from .sx import SXGate, SXdgGate, CSXGate, CSXdgGate
from .s import SGate, SdgGate, CSGate, CSdgGate
from .t import TGate, TdgGate, CTGate, CTdgGate
from .swap import SwapGate, CSWAPGate
from .iswap import iSwapGate
from .dcx import DCXGate
from .ecr import ECRGate
from .u import UGate, CUGate
from .u1 import U1Gate, CU1Gate
from .u2 import U2Gate, CU2Gate
from .u3 import U3Gate, CU3Gate
from .rx import RXGate, CRXGate
from .ry import RYGate, CRYGate
from .rz import RZGate, CRZGate
from .p import PhaseGate, CPhaseGate
from .r import RGate, CRGate
from .rxx import RXXGate
from .ryy import RYYGate
from .rzz import RZZGate
from .rzx import RZXGate


GATE_REGISTRY = {
    'id': IGate,
    'x': XGate,
    'cx': CXGate,
    'ccx': CCXGate,
    'y': YGate,
    'cy': CYGate,
    'z': ZGate,
    'cz': CZGate,
    'ccz': CCZGate,
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
    'cswap': CSWAPGate,
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
    'rzx': RZXGate
}

BASIS_GATES = set(GATE_REGISTRY.keys())
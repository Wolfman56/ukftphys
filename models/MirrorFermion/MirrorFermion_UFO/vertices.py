# -*- python -*-
from object_library import all_vertices, Vertex
import particles as P
import lorentz as L
import couplings as C

# Higgs portal
V_1 = Vertex(
    name = 'V_1',
    particles = [ P.H, P.H, P.xm__tilde__, P.xm ],
    color = [ '1' ],
    lorentz = [ L.SSSS ],
    couplings = { (0,0): C.GC_HiggsPortal }
)

# Gauge couplings + mirror reflection
V_2 = Vertex(
    name = 'V_2',
    particles = [ P.G, P.xm__tilde__, P.xm ],
    color = [ 'T(1,3,2)' ],
    lorentz = [ L.FFV1 ],
    couplings = { (0,0): C.GC_QCD }
)
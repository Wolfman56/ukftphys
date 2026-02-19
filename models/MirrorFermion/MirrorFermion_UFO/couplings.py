# -*- python -*-
from object_library import all_couplings, Coupling
import parameters as Param

GC_HiggsPortal = Coupling(
    name = 'GC_HiggsPortal',
    value = 'lambdaH',
    order = {'QED':1}
)

GC_QCD = Coupling(
    name = 'GC_QCD',
    value = '1',
    order = {'QCD':1}
)
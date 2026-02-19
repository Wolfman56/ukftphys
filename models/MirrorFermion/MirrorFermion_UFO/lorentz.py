# -*- python -*-
from object_library import all_lorentz, Lorentz

SSSS = Lorentz(
    name = 'SSSS',
    spins = [ 1, 1, 2, 2 ],
    structure = '1'
)

FFV1 = Lorentz(
    name = 'FFV1',
    spins = [ 2, 2, 3 ],
    structure = 'Gamma(3,2,1)'
)
# -*- python -*-
from object_library import all_particles, Particle
import parameters as Param

xm = Particle(
    pid = 6000001,
    name = 'xm',
    antiname = 'xm~',
    spin = 2,
    color = 3,
    mass = Param.MXm,
    width = Param.WXm,
    texname = '\\Psi_m',
    antitexname = '\\bar{\\Psi}_m',
    charge = 2/3,
    pdg_code = 6000001
)

xm__tilde__ = xm.anti()

xmInv = Particle(
    pid = 6000002,
    name = 'xmInv',
    antiname = 'xmInv',
    spin = 1,
    color = 1,
    mass = Param.MXmInv,
    width = Param.WXmInv,
    texname = 'x_m^{inv}',
    antitexname = 'x_m^{inv}',
    charge = 0,
    pdg_code = 6000002
)
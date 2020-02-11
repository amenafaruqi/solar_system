# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 22:03:53 2019

@author: amena
"""
import astropy.constants as const
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------- CONSTANTS ---------------------------------

G = const.G.value                  # Gravitational constant [m3/(kg s2)]
atm = const.atm.value              # Earth's atmospheric pressure [Pa]
c = const.c.value                  # Speed of light [m/s] 
g0 = const.g0.value                # Graviational acceleration on Earth [m/s2]
L_sun = const.L_sun.value          # Solar luminosity [W]
au = const.au.value                # 1 AU [m]
pc = const.pc.value                # 1 pc [m]
sigma_sb = const.sigma_sb.value    # Stefan-Boltzmann constant [W/K4 m2]

M_sun = const.M_sun.value          # Mass of the Sun [kg]
M_venus = 0.815*M_earth            # Mass of Venus [kg]
M_earth = const.M_earth.value      # Mass of Earth [kg]
M_mars = 0.107*M_earth             # Mass of Mars [kg]
M_jupiter = const.M_jup.value      # Mass of Jupiter [kg]
M_saturn = 95.16*M_earth           # Mass of Saturn [kg]
M_uranus = 14.54*M_earth           # Mass of Uranus [kg]
M_neptune = 17.15*M_earth          # Mass of Neptune [kg]

R_sun = const.R_sun.value          # Radius of Sun [m]
R_venus = 6051800                  # Radius of Venus [m]
R_earth = const.R_earth.value      # Radius of Earth [m]
R_mars = 3389500                   # Radius of Mars [m]
R_jupiter = 69911000               # Radius of Jupiter [m]
R_saturn = 58232000                # Radius of Saturn [m]
R_uranus = 25262000                # Radius of Uranus [m]
R_neptune = 246220000              # Radius of Neptune [m]

#----------------------------------------------------------------------------
class SSO:
    def __init__(self, radius, mass):
        self.radius = radius
        self.mass = mass
    
    def density(self):
        volume = (4*np.pi/3)*self.radius**3
        return self.mass/volume
    

class Planet(SSO):
    def __init__(self, radius, mass, d_orb, period, albedo, parent_luminosity, atmosphere=False):
        SSO.__init__(self, radius, mass)
        self.d_orb = d_orb
        self.period = period
        self.albedo = albedo
        self.parent_luminosity = parent_luminosity
        self.atmosphere = atmosphere
    
    def temperature(self):
        if not self.atmosphere:
            T_eff = (self.parent_luminosity*(1-self.albedo)/(16*sigma_sb*np.pi*self.d_orb**2))**0.25
        else:
            T_eff = None
        return T_eff
    
    
    def radial_velocity(self):
        return (2*np.pi*self.d_orb)/self.period
        
class Star(SSO):
    def __init__(self, radius, mass, luminosity):
        SSO.__init__(self, radius, mass)
        self.luminosity = luminosity
    
    def temperature(self):
        T_eff = (self.luminosity/(4*np.pi*sigma_sb*self.radius**2))**0.25
        return T_eff

class Moon(SSO):
    def __init__(self, radius, mass, d_orb, period, albedo):
        SSO.__init__(self, radius, mass)
        self.d_orb = d_orb
        self.period = period
        self.albedo = albedo

    def radial_velocity(self):
        return (2*np.pi*self.d_orb)/self.period
    

def make_solar_system():
    pass
    
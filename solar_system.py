import astropy.constants as const
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import cm

# ================================================================================================
# ----------------------------------------- CONSTANTS --------------------------------------------
# ================================================================================================

G = const.G.value                  # Gravitational constant [m3/(kg s2)]
atm = const.atm.value              # Earth's atmospheric pressure [Pa]
c = const.c.value                  # Speed of light [m/s] 
g0 = const.g0.value                # Graviational acceleration on Earth [m/s2]
L_sun = const.L_sun.value          # Solar luminosity [W]
au = const.au.value                # 1 AU [m]
pc = const.pc.value                # 1 pc [m]
sigma_sb = const.sigma_sb.value    # Stefan-Boltzmann constant [W/K4 m2]

M_sun = const.M_sun.value          # Mass of the Sun [kg]
M_earth = const.M_earth.value      # Mass of Earth [kg]
M_mercury = 0.055*M_earth          # Mass of Mercury [kg]
M_venus = 0.815*M_earth            # Mass of Venus [kg]
M_mars = 0.107*M_earth             # Mass of Mars [kg]
M_jupiter = const.M_jup.value      # Mass of Jupiter [kg]
M_saturn = 95.16*M_earth           # Mass of Saturn [kg]
M_uranus = 14.54*M_earth           # Mass of Uranus [kg]
M_neptune = 17.15*M_earth          # Mass of Neptune [kg]

R_sun = const.R_sun.value          # Radius of Sun [m]
R_mercury = 2439700                # Radius of Mercury [m]
R_venus = 6051800                  # Radius of Venus [m]
R_earth = const.R_earth.value      # Radius of Earth [m]
R_mars = 3389500                   # Radius of Mars [m]
R_jupiter = 69911000               # Radius of Jupiter [m]
R_saturn = 58232000                # Radius of Saturn [m]
R_uranus = 25262000                # Radius of Uranus [m]
R_neptune = 24622000               # Radius of Neptune [m]

a_mercury = 0.12                   # Albedo of Mercury
a_venus = 0.59                     # Albedo of Venus
a_earth = 0.31                     # Albedo of Earth
a_mars = 0.15                      # Albedo of Mars
a_jupiter = 0.44                   # Albedo of Jupiter
a_saturn = 0.46                    # Albedo of Saturn
a_uranus = 0.56                    # Albedo of Uranus
a_neptune = 0.51                   # Albedo of Neptune

d_mercury = 0.38*au                # Orbital radius of Mercury [m]
d_venus = 0.72*au                  # Orbital radius of Venus [m]
d_earth = au                       # Orbital radius of Earth [m]
d_mars = 1.52*au                   # Orbital radius of Mars [m]
d_jupiter = 5.2*au                 # Orbital radius of Jupiter [m]
d_saturn = 9.58*au                 # Orbital radius of Saturn [m]
d_uranus = 19.14*au                # Orbital radius of Uranus [m]
d_neptune = 30.2*au                # Orbital radius of Neptune [m]


# ================================================================================================
# --------------------------------------- ASSUMPTIONS --------------------------------------------
# ================================================================================================

# 1) Perfectly circular, constant velocity orbits
# 2) Uniform density spheres
# 3) No planetary atmospheres

# ================================================================================================
# ---------------------------------------- SSO CLASSES -------------------------------------------
# ================================================================================================


class SSO:
    def __init__(self, name, radius, mass):
        self.name = name
        self.radius = radius
        self.mass = mass
        self.volume = (4*np.pi/3)*self.radius**3
        self.density = self.mass/self.volume
    
    def orbit(self):
        pass               # CODE FOR MATHMETICAL ORBITAL TRAJECTORY HERE

class Planet(SSO):
    def __init__(self, name, radius, mass, d_orb, parent, albedo, atmosphere=False):
        SSO.__init__(self, name, radius, mass)
        self.d_orb = d_orb
        self.parent = parent
        self.albedo = albedo
        self.atmosphere = atmosphere
        self.period = (((4*np.pi**2)/(G*self.parent.mass))*self.d_orb**3)**0.5
        self.radial_velocity = (2*np.pi*self.d_orb)/self.period  
        self.temperature = None
        if not self.atmosphere:
            self.temperature = (self.parent.luminosity*(1-self.albedo)/(16*sigma_sb*np.pi*self.d_orb**2))**0.25
       
        # CALCULATE ATMOPSHERE TRUE/FALSE BASED ONE ESCAPE VELOCITY??
        # GET MORE ACCURATE TEMPS AND COLOUR CODE BASED ON THOSE??
        # ATMOSPHERIC PRESSURE CALCULATION?? 
      
class Star(SSO):
    def __init__(self, name, radius, mass, luminosity):
        SSO.__init__(self, name, radius, mass)
        self.luminosity = luminosity
        self.temperature = (self.luminosity/(4*np.pi*sigma_sb*self.radius**2))**0.25


class Moon(SSO):
    def __init__(self, name, radius, mass, d_orb, parent, albedo):
        SSO.__init__(self, name, radius, mass)
        self.d_orb = d_orb
        self.parent = parent
        self.albedo = albedo
        self.period = (((4*np.pi**2)/(G*self.parent.mass))*self.d_orb**3)**0.5
        self.radial_velocity = (2*np.pi*self.d_orb)/self.period
    
    
# ================================================================================================
# --------------------------------- GENERATE A SOLAR SYSTEM --------------------------------------
# ================================================================================================
        
sun = Star('Sun', R_sun, M_sun, L_sun)
mercury = Planet('Mercury', R_mercury, M_mercury, d_mercury, sun, a_mercury)
venus  = Planet('Venus', R_venus, M_venus, d_venus, sun, a_venus)
earth = Planet('Earth', R_earth, M_earth, d_earth, sun, a_earth)
mars = Planet('Mars', R_mars, M_mars, d_mars, sun, a_mars)
jupiter = Planet('Jupiter', R_jupiter, M_jupiter, d_jupiter, sun, a_jupiter)
saturn = Planet('Saturn', R_saturn, M_saturn, d_saturn, sun, a_saturn)
uranus = Planet('Uranus', R_uranus, M_uranus, d_uranus, sun, a_uranus)
neptune = Planet('Neptune', R_neptune, M_neptune, d_neptune, sun, a_neptune)

SSOs = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


def make_static_plot(SSOs):
    ax = plt.subplot(111)
    ax.set_ylim(-15,15)
    colours = cm.rainbow(np.linspace(0, 1, len(SSOs)))
    
    for i in range(len(SSOs)):
        radius = np.log10(SSOs[i].radius/1e6)
        y = 0
        if isinstance(SSOs[i], Planet):
            x = SSOs[i].d_orb/(0.1*au)
        else:
            x = 0
        obj_plot = Circle((x,y), radius, label = SSOs[i].name, color=colours[i])
        ax.add_patch(obj_plot)
    
    plt.legend(bbox_to_anchor=(1.1,1))
    ax.set_facecolor('black')
    ax.set_xlabel('Distance from Sun (10 AU)')
    plt.title('The Solar System (2D, static)')
    ax.set_yticklabels([])
    fig = plt.gcf()
    fig.set_size_inches(25,3)
    plt.autoscale(axis='x')
    plt.show()
        
    

    
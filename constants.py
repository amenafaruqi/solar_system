import astropy.constants as const

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

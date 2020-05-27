import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import cm
import matplotlib.animation as anim
from mpl_toolkits.mplot3d import Axes3D
import constants as c

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
    def __init__(self, name, radius, mass, d_orb, obj_type):
        self.name = name
        self.radius = radius
        self.mass = mass
        self.obj_type = obj_type
        self.position = np.array((0, d_orb), dtype=float)

    def volume(self):
        return (4*np.pi/3)*self.radius**3

    def density(self):
        return self.mass/self.volume


class Planet(SSO):
    def __init__(self, name, radius, mass, d_orb, parent, albedo, atmosphere=False):
        SSO.__init__(self, name, radius, mass, d_orb, obj_type='planet')
        self.d_orb = d_orb
        self.parent = parent
        self.albedo = albedo
        self.atmosphere = atmosphere
        self.temperature = None
        self.position = np.array((d_orb, 0), dtype=float)
        self.v_angular = (2*np.pi)/self.period()
        self.velocity = self.v_angular*self.position

    def temperature(self):
        if not self.atmosphere:
            return (self.parent.luminosity*(1-self.albedo)/(16*c.sigma_sb*np.pi*self.d_orb**2))**0.25

    def update_velocity(self, t=0):
        x_velocity = -self.d_orb*self.v_angular*np.sin(self.v_angular*t)
        y_velocity = self.d_orb*self.v_angular*np.cos(self.v_angular*t)
        self.velocity = np.array((x_velocity, y_velocity), dtype=float)

    def period(self):
        return (((4*np.pi**2)/(c.G*self.parent.mass))*self.d_orb**3)**0.5

    def update_position(self, t=0):
        x = self.d_orb*np.cos(self.v_angular*t)
        y = self.d_orb*np.sin(self.v_angular*t)
        self.position = np.array((x, y), dtype=float)

    def move_in_orbit(self, t=0):
        self.update_position(t)
        self.update_velocity(t)


class Star(SSO):
    def __init__(self, name, radius, mass, luminosity, d_orb=0):
        SSO.__init__(self, name, radius, mass, d_orb, obj_type='star')
        self.luminosity = luminosity
        self.temperature = (self.luminosity/(4*np.pi*c.sigma_sb*self.radius**2))**0.25
        self.position = np.array((0, 0), dtype=float)
        self.velocity = np.array((0, 0), dtype=float)


# ================================================================================================
# --------------------------------- GENERATE A SOLAR SYSTEM --------------------------------------
# ================================================================================================

sun = Star('Sun', c.R_sun, c.M_sun, c.L_sun)
mercury = Planet('Mercury', c.R_mercury, c.M_mercury, c.d_mercury, sun, c.a_mercury)
venus = Planet('Venus', c.R_venus, c.M_venus, c.d_venus, sun, c.a_venus)
earth = Planet('Earth', c.R_earth, c.M_earth, c.d_earth, sun, c.a_earth)
mars = Planet('Mars', c.R_mars, c.M_mars, c.d_mars, sun, c.a_mars)
jupiter = Planet('Jupiter', c.R_jupiter, c.M_jupiter, c.d_jupiter, sun, c.a_jupiter)
saturn = Planet('Saturn', c.R_saturn, c.M_saturn, c.d_saturn, sun, c.a_saturn)
uranus = Planet('Uranus', c.R_uranus, c.M_uranus, c.d_uranus, sun, c.a_uranus)
neptune = Planet('Neptune', c.R_neptune, c.M_neptune, c.d_neptune, sun, c.a_neptune)


# ================================================================================================
# --------------------------------------- MAKE PLOTS ---------------------------------------------
# ================================================================================================


class SSOVisualisation:
    def __init__(self, SSOs=[], dimensions=2):
        self.SSOs = SSOs
        self.dimensions = dimensions
        self.__text0 = None

    def make_2D_solar_system(self, n):
        t = n * 3600 * 24 * 29.5   # Each frame is a month

        solar_system = plt.Circle((0, 0), 350, fill=True, fc='black', ls='solid')
        ax.add_artist(solar_system)
        ax.axes.set_aspect('equal')
        self.__text0 = ax.text(-340, 320, "Month={:4d}".format(n, fontsize=24))
        patches = [self.__text0]
        colours = cm.rainbow(np.linspace(0, 1, len(self.SSOs)))[::-1]

        for i, obj in enumerate(self.SSOs):
            radius = np.log10(obj.radius/1e6)
            if obj.obj_type == 'planet':
                obj.move_in_orbit(t)
            obj_plot = Circle(obj.position/(0.1*c.au), radius, label=obj.name, color=colours[i])
            ax.add_patch(obj_plot)
            patches.append(obj_plot)

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.2, 1))

        return patches

    def add_third_dimension(self, obj):
        if len(obj.position) < 3:
            obj.position = np.append(obj.position, 0)
            obj.velocity = np.append(obj.velocity, 0)

    def make_3D_solar_system(self, n):
        t = n * 3600 * 24 * 29.5   # Each frame is a month

        ax.axes.set_aspect('equal')
        self.__text0 = ax.text2D(0.05, 0.95, "Month={:4d}".format(n, fontsize=24),
                                 transform=ax.transAxes)
        patches = [self.__text0]
        colours = cm.rainbow(np.linspace(0, 1, len(SSOs)))[::-1]

        for i, obj in enumerate(self.SSOs):
            size = ((np.log10(obj.radius/1e6))**2)*10
            if obj.obj_type == 'planet':
                obj.move_in_orbit(t)
            self.add_third_dimension(obj)
            x, y, z = obj.position/(0.1*c.au)
            patches.append(ax.scatter(x, y, z, marker='.', s=size, color=colours[i],
                                      label=obj.name, depthshade=True))

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.5, 1))
        return patches

    def make_static_plot(self):
        ax = plt.subplot(111)
        ax.set_ylim(-15, 15)
        solar_system = Circle((0, 0), 350, fill=True, fc='black', ls='solid')
        ax.add_patch(solar_system)
        ax.axes.set_aspect('equal')
        colours = cm.rainbow(np.linspace(0, 1, len(SSOs)))[::-1]

        for i, obj in enumerate(SSOs):
            radius = np.log10(obj.radius/1e6)
            y = 0
            if obj.obj_type == 'planet':
                x = obj.d_orb/(0.1*c.au)
            else:
                x = 0
            obj_plot = Circle((x, y), radius, label=obj.name, color=colours[i])
            ax.add_patch(obj_plot)

        plt.legend(bbox_to_anchor=(1.1, 1.5))
        ax.set_xlabel('Distance from Sun (0.1 AU)')
        plt.title('The Solar System (2D, static)')
        ax.set_yticklabels([])
        fig = plt.gcf()
        fig.set_size_inches(25, 3)
        plt.autoscale(axis='x')
        plt.show()


if __name__ == "__main__":

    SSOs = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    solar_system = SSOVisualisation(SSOs)

    solar_system.make_static_plot()

    fig = plt.figure()
    ax = plt.axes(xlim=(-350, 350), ylim=(-350, 350))
    ax.set_facecolor('white')

    animation = anim.FuncAnimation(fig,
                                   solar_system.make_2D_solar_system,
                                   frames=2000,
                                   interval=50,
                                   blit=True)

    ax.set_xlabel('Distance from Sun (0.1 AU)')
    plt.title('The Solar System (2D, animated)')
    plt.show()

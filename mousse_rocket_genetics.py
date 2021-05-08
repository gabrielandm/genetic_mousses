'''
 Angle
 Thrust limit
 Engine flow rate (between 100% and 70% or stuck at 0%)

 Fitness -> Height and Speed

 Rule:
 Fuel limit
'''

from math import sqrt, pi, atan, sin, cos
from random import random
from collections import namedtuple

Rocket = namedtuple('Rocket', ['m', 'vy', 'vx', 'h'])
# m -> Rocket's mass
# vy -> Rocket's Vertical velocity
# vx -> Rocket's orbital velocity
# h -> Orbital height

cd = 0.4
mo = 1.3*10^4 # Initial rocket mass [kg] # UwU
D = 1.2 # Rocket diameter [meters]
Mf = 1.25*10^4 # Fuel mass [kg]
dmdt = 650 # Engine fuel flow rate [kg]
dt = 0.1 # Iteration time [s]
gimble_limit = 7 # Gimble limit [degree]
orbital_height = 10^6 # Final height [meters]
G = 6.67*10^-11
M = 5.97223*10^24
R = 6.3781*10^6
thrust = 2.25*10^5 # Max thrust [NEWtown]

def newton_gravity(h):
    global G
    global M
    global R

    return (G * M) / (R + h)^2

def atm_pressure(h, g):
    Po = 1
    a = 1 / 25
    To = 298
    M = 29
    R = 0.082
    # in atm
    return Po * ((a * h + To) / To) ^ (-M * g / a * R)

def air_density(P, h):
    M = 29
    R = 0.082
    T = 298

    if h > 8.5*10^6:
        return 0
    else:
        return (P * M) / (R * T)

def s_big_calculator(): # cross_sectional_area
    global D

    return (pi * D ^ 2) / 4

def air_drag(V, h):
    air_density = air_density(atm_pressure(h, newton_gravity(h)), h)
    
    global cd

    S = s_big_calculator()

    F = (S * V^2 * cd) * 0.5

    return F

def orbital_velocity():
    global orbital_height
    global G
    global M
    global R

    return sqrt(G * M / (R + orbital_height))

def rocket_weight(g, m):
    return (m * g)

def rocket_aceleration(F, m):
    #     |  ax  |  ay   |
    return F / m

def rocket_velocity_variation(a):
    global dt
    #     | dvdt |
    return dt * a

def rocket_mass_variation(throtle):
    global dt
    global dmdt

    return -dmdt * dt * throtle

def things_calculator(rocket_stuff):
    global thrust

    # getting current rocket info
    m = rocket_stuff.m
    vy = rocket_stuff.vy
    vx = rocket_stuff.vx
    h = rocket_stuff.h

    # escolher o angulo
    gimble = random() * 14 - 7

    # força do motor
    throtle = random() * 0.3 + 0.7

    # calcular massa do foguete
    mf = m + rocket_mass_variation()
    
    téta = atan(vy / vx)
    
    # Força do engine
    Fmx = thrust * throtle * cos(téta + gimble)
    Fmy = thrust * throtle * sin(téta + gimble)

    Fx = Fmx - air_drag(vx, h)
    Fy = Fmy - air_drag(vy, h) - rocket_weight(newton_gravity(h), mf)

    afx = rocket_aceleration(Fx, mf)
    afy = rocket_aceleration(Fy, mf)

    vfx = vx + rocket_velocity_variation(afx)
    vfy = vy + rocket_velocity_variation(afy)

    # atitude
    hf = h + vfy * dt

    return mf, afx, afy, vfx, vfy, hf

''' Limits 
 things_calculator() until:
  m <= mo - Mf
  h >= orbital_height
  vx > orbital_velocity
  vx == orbital_velocity && vy != 0
'''

''' Fitness
 vx == orbital_velocity
 h == orbital_height
 vy == 0
'''
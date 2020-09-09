from barycorrpy import get_BC_vel
from barycorrpy.utils import get_stellar_data
import numpy as np
import os, sys
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import cm

try:
    ScriptDirectory = os.path.dirname(os.path.abspath(__file__))
except:
    ScriptDirectory = r"/home/shbhuk/PSU_SCD/src" # On the cluster
    ScriptDirectory = r"C:\Users\shbhu\Documents\Git\PSU_SCD\src" # Local to SK's computer


# Folder where Data is stored
DataDirectory = r"/mnt_scratch/SCD/turboseti/hit_lists" # On the cluster
DataDirectory = os.path.join(os.path.dirname(ScriptDirectory), 'OtherData')# Local to SK's computer


TargetNames = np.loadtxt(os.path.join(DataDirectory, 'TargetNames.txt'), dtype=str)
TargetMJDs = np.loadtxt(os.path.join(DataDirectory, 'TargetMJDs.txt'))
TargetJDUTC = Time(TargetMJDs, format='mjd').jd
TargetDF = pd.read_csv(os.path.join(DataDirectory, 'TargetTable.csv'))

GBTCoordinates = EarthLocation.of_site("GBT").geodetic

TimeBufferForBCPy = [-1, 1] # Search +- 1 hour to search for barycentric velocity
                            # and measure slope, i.e. acceleration
TimeRange = np.arange(TimeBufferForBCPy[0]/24, TimeBufferForBCPy[1]/24, 5*60/86400) # Steps of 5 minutes each

BarycentricVelocities = np.zeros((len(TargetNames), len(TimeRange)))
TargetBarycentricAcceleration = np.zeros((len(TargetNames), len(TimeRange)-1))
TargetJDUTCRange = np.zeros((len(TargetNames), len(TimeRange)))

"""
for i in range(len(TargetNames)):
    if i == 51:
        continue
    name = TargetNames[i]
    print(i, name)
    Mask = TargetDF.Planet_Name == name
    if not np.any(Mask):
        result = get_stellar_data(name)[0]
        ra = result['ra']
        dec = result['dec']
        pmra = result['pmra']
        pmdec =result['pmdec']
        px = result['px']
        rv = result['rv']
    else:
        result = TargetDF[Mask]
        ra = result['ra'].values
        dec = result['dec'].values
        pmra = result['gaia_pmra'].values
        pmdec =result['gaia_pmdec'].values
        px = result['gaia_plx'].values
        rv = result['st_radv'].values
        if np.isnan(rv):
            rv = 0


    TargetJDUTCRange[i] = (TargetJDUTC[i] + TimeRange)
    BarycentricVelocities[i] = np.hstack(get_BC_vel(JDUTC=TargetJDUTCRange[i], ra=ra, dec=dec, obsname="GBT",
                pmra=pmra, pmdec=pmdec, px=px, rv=rv, leap_update=False)[0])
    TargetBarycentricAcceleration[i] = (np.diff(BarycentricVelocities[i]*u.m/u.s) / (np.diff(TargetJDUTCRange[i]*u.d))).to(u.m/u.s/u.s) # Convert from per day to per second

np.savetxt(os.path.join("BarycorrpyResults_JDUTC.txt"), TargetJDUTCRange)
np.savetxt(os.path.join("BarycorrpyResults_BCVelocity.txt"), BarycentricVelocities)
np.savetxt(os.path.join("BarycorrpyResults_BCAcceleration.txt"), TargetBarycentricAcceleration)

plt.figure()
# Define colour scheme
cmap = matplotlib.cm.Spectral
# Establish colour range based on variable
norm = matplotlib.colors.Normalize(vmin=0, vmax=len(TargetNames))


for i in range(len(TargetNames)):
    if i == 51:
        continue
    name = TargetNames[i]
    colour = cmap(norm(i))
    plt.plot(TargetJDUTCRange[i], BarycentricVelocities[i] - BarycentricVelocities[i][0], label=name+'_'+str(i), color=colour)
plt.legend()
plt.xlabel("JD")
plt.ylabel("Change in barycentric velocity m/s")
plt.show(block=False)



plt.figure()
# Define colour scheme
cmap = matplotlib.cm.Spectral
# Establish colour range based on variable
norm = matplotlib.colors.Normalize(vmin=0, vmax=len(TargetNames))


for i in range(len(TargetNames)):
    if i == 51:
        continue
    name = TargetNames[i]
    colour = cmap(norm(i))
    plt.plot(TargetJDUTCRange[i][1:], TargetBarycentricAcceleration[i], label=name+'_'+str(i), color=colour)
plt.legend()
plt.xlabel("JD")
plt.ylabel("Bary acc. m/s2")
plt.show(block=False)
"""
AccelerationAtExposure = TargetBarycentricAcceleration[:,12]
np.savetxt(os.path.join("BarycorrpyResults_AccelerationAtExposure.txt"), AccelerationAtExposure)

# ORIGINAL FILE BY ROBERTO IKER SÁNCHEZ ORTIZ
# MODIFICATIONS DONE TO SUIT airfoilFoam.
# For the moment only using Umag, chord, rho, mu, pressure
#########################################################################
# Select AOA_LIST or STEP
#
PROGRAM = "STEP"

# ---------- STEP OPTION ---------------------------------------------- #
# Introduce max, min and step

MaxAOA = 24
MinAOA = 12

step = 2

# ---------- AOA_LIST OPTION ----------------------------------------------- #
# Introduce every AOA to simulation

AOA_LIST = [12]

# ---------- Simulations options -------------------------------------- #

# INPUT FOR VELOCITY AT INLET
# Select type of input: "Reynolds", "Mach" or "Vinf" for Velocity at infinity
# Units: SI

CASE_INPUT = "Reynolds"

Umag = 1
Reynolds = 10e6
Mach = 0

chord = 1
rho = 1
mu = 9.671e-8
pressure = 0
#Temperature only needed for specification by Mach
Temperature = 288.15

# ---------- Suction-Blowing Options ---------------------------------- #
Activate_suc_blow = True
Cq = -0.016

# ---------- Turbulence Options --------------------------------------- #
#CHANGE BOUNDARY CONDITIONS FOR TURBULENT VARIABLES
#Note rho, mu and pressure will also be changed
Turb_BC_change =True

#Turbulence Model
# SST, LM, SST_and_LM or LM_from_SST
# LM_and_SST will run both models in the order: SST, then LM.
# LM_from_SST will run LM from a SST converged solution:
#     ( - Restart option must be activated)
#     ( - Only gamma and ReThetat files will be copied from default folder)
model = "SST"

# Restart
# Caution: solution angles must correspond to the angles in this script
restart = False

#Turbulence Intensity (percentage %)
Tu = 0.2

#First cell height (this is not the value used by auto mode mesh generation)
desired_yPlus = 30

#Farfield length (between L/10 and L)
L = 100

#########################################################################
# VERBOSE                                                               #
# Print every change in every file                                      #
verbose = True
#                                                                       #
# NUMBER OF CORES                                                       # 
#
CORES = 4
#                                                                       #
# ----------------------- END OF SET-UP ------------------------------- #
#########################################################################

import cantera as ct
import numpy as np
import matplotlib.pyplot as plt


#import the gas
gas=ct.Solution("gri30.yaml")
#equivalence ratio range
phi_min=0.3
phi_max=3.5
npoints=50
#set the gas composition
T=300.0
P=101325.0
#find fuel, nitrogen and oxygen indices
fuel_species="CH4"
ifuel=gas.species_index(fuel_species)
io2=gas.species_index("O2")
in2=gas.species_index("N2")
#air composition
air_N2_O2_ratio=3.76
stoich_O2=gas.n_atoms(fuel_species,"C")+0.25*gas.n_atoms(fuel_species,"H")
#some arrays to hold the data
phi=np.zeros(npoints)
tad=np.zeros(npoints)
xeq=np.zeros((gas.n_species,npoints))
#solution
for i in range(npoints):
    phi[i]=phi_min+(phi_max-phi_min)*i/(npoints-1)
    X=np.zeros(gas.n_species)
    X[ifuel]=phi[i]
    X[io2]=stoich_O2
    X[in2]=stoich_O2*air_N2_O2_ratio
    #set the gas state
    gas.TPX=T,P,X
    #equilibrate the mixture adiabatically at constant P
    gas.equilibrate("HP")
    tad[i]=gas.T
    xeq[:,i]=gas.X
    print("At phi= ","%10.4f"%(phi[i])+" Tad = ","%10.4f"%(tad[i]))
#results
#mass fractions of selected species
for i, cas in enumerate(gas.species_names):
    if cas in ["O2","CO2","CO"]:
        plt.plot(phi,xeq[i,:],label=cas)
    plt.xlabel("Equivalence ratio")
    plt.ylabel("Mass fractions")
    plt.legend(loc="best")
plt.show()
#adiabatic flame temperature
plt.plot(phi,tad)
plt.xlabel("Equivalence ratio")
plt.ylabel("Adiabatic flame temperature [K]")
plt.show()
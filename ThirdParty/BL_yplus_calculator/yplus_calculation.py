from math import log10, sqrt
#This script calculates first layer height with the flat plate boundary layer estimation method
# File by Roberto Iker Sánchez Ortiz
#Comments and integration with the rest of the airfoilFoam tool by Sócrates Fernández Fernández
def main( yplus = 1.0, rho = 1.225, u_inf = 120, L_ref = 1.0, mu = 1.8E-5, print_boolean = False):
    
    Re = rho * u_inf * L_ref / mu
    
    Cf = ( 2*log10(Re) - 0.65 ) ** (-2.3)
    
    tau_w = Cf * 1/2 * rho * u_inf**2
    
    u_friction = sqrt( tau_w / rho )
    
    y = yplus * mu / ( rho * u_friction )
    
    if print_boolean:
        print("INPUTS: ")
        print('yplus = %d \n rho   = %f \n u_inf = %f \n L_ref = %f \n mu    = %e' % (yplus, rho, u_inf, L_ref, mu))
        print("First Layer Height = ", y)
    return y

if __name__ == "__main__":
    main(print_boolean = True)

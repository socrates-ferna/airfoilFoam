
def main(L = 100, y1 = 1E-6, n = 1000, RT = 1.2, n_min = 1, n_max = 10000, error = 1E-12, times = 10000, yplus_cal = False, mode_for = "n_w_similar_RT" ):
    
    if (yplus_cal):
        import yplus_calculation as yp
        y1 = yp.main( u_inf = 0.7 * 340 )
    
    if   mode_for == "RT":
        printer("Solution for RT from y1 and n")
        RT_new = solve_for_RT(RT, y1, n, times, error, L )
        printer("RT guess = " + str(RT))
        printer("L  = " + str(fun_RT(RT_new, y1, n )))
        printer("RT = " + str(RT_new))
        printer("y1 = " + str(y1))
        printer("yn = " + str(y1*RT_new**(n-1)))
        return RT_new
        
    elif mode_for == "y1":
        printer("Solution for y1 from n and RT")
        y1_new = solve_for_y(RT, n, L)
        printer("L  = " + str( fun_y(RT, y1_new, n) ) )
        printer("RT = " + str(RT))
        printer("y1 = " + str(y1_new))
        printer("yn = " + str(y1_new*RT**(n-1)))
        return y1_new
    
    elif mode_for == "L":
        printer("Solution for L from n, y1 and RT")
        L_new = str( fun_y(RT, y1, n) )
        printer("L  = " + L_new )
        printer("RT = " + str(RT))
        printer("y1 = " + str(y1))
        printer("yn = " + str(y1*RT**(n-1)))
        return L_new
        
    elif mode_for == "aprox_n":
        printer("Aproximate Solution for n")
        n_new = solve_for_n_aprox(RT, y1, n, times, L )
        printer("n guess = " + str(n))
        printer("y1 desired = " + str(y1))
        printer("L  = " + str(fun_n(RT, y1, n_new)))
        printer("RT = " + str(RT))
        n = n_new
        y1_new = solve_for_y(RT, n, L)
        printer("y1 = " + str(y1_new))
        printer("n  = " + str(n_new))
        printer("yn = " + str(y1_new*RT**(n_new-1)))
        return n_new
        
    elif mode_for == "n_w_similar_RT":
        printer("Solution for n from y1 with a similar RT")
        [n_new, RT_new] = solve_for_n(RT, y1, n, times, error, L )
        printer("RT desired = " + str(RT))
        printer("L  = " + str(fun_RT(RT_new, y1, n_new)))
        printer("RT = " + str(RT_new))
        printer("y1 = " + str(y1))
        printer("n  = " + str(n_new))
        printer("yn = " + str(y1*RT**(n_new-1)))
        return n_new, RT_new

def fun_RT(RT, y1, n):
    y = [ y1*RT**i for i in range(n) ]
    return sum(y)

def der_RT(RT, y1, n):
    dy = [ i*y1*RT**(i-1) for i in range(n) ]
    return sum(dy)

def solve_for_RT( RT, y1, n, times,error, L ):
    printer("Iterations",end='')
    for i in range(times):
        RT_new = (L - fun_RT(RT, y1, n) + der_RT(RT, y1, n)*RT) / der_RT(RT, y1, n)
        printer(".",end='')
        if abs(RT_new -RT)/RT < error:
            printer(" = " + str(i))
            break
        else:
            RT = RT_new
    return RT_new

def fun_y(RT, y1, n):
    y = [ y1*RT**i for i in range(n) ]
    return sum(y)

def solve_for_y(RT, n, L):
    y1_new = L / sum([ RT**i for i in range(n) ])
    return y1_new

def fun_n(RT, y1, n):
    y = [ y1*RT**i for i in range(n) ]
    return sum(y)

def der_n(RT, y1, n):
    der = (fun_n(RT, y1, n+1) - fun_n(RT, y1, n-1)) / 2
    return der

def solve_for_n_aprox(RT, y1, n, times, L):
    from math import floor, ceil

    for i in range(times):
        n_new = int(ceil((L - fun_n(RT, y1, n) + der_n(RT, y1,n)*n) / der_n(RT, y1,n)))
        if abs(n_new - n) < 1:
            printer("Iterations = " + str(i))
            break
        else:
            n = n_new
    return n_new

def solve_for_n(RT, y1, n, times, error, L):
    n_new = solve_for_n_aprox(RT, y1, n, times, L)
    RT_new = solve_for_RT(RT, y1, n_new, times, error, L)
    return n_new, RT_new

def printer(*arg, end="\n"):
    if yes:
        print(*arg, end=end)
    else: 
        pass

yes = False

if __name__ == "__main__":
    yes = True
    L = 100
    y1 = 1E-6
    n = 40
    RT = 1.3
    n_min = 1
    n_max = 10000
    error = 1E-12
    times = 10000
    yplus_cal = False
    mode_for = "L"
    main(L,y1,n,RT,n_min,n_max,error,times,yplus_cal,mode_for)


import numpy as np
cimport numpy as np
#np.float64_t = np.float64_t
#from scipy.signal import butter, lfilter
#import matplotlib.pyplot as plt

def Response_Spectra(np.ndarray[np.float64_t, ndim=1] acc, double dt, double xi, np.ndarray[np.float64_t, ndim=1] period):
    #cdef double m, c, k
    #cdef double SD, PSV, PSA, SV, SA
    cdef int Np, Nt
    Np = acc.size
    Nt = period.size
    
    cdef int i_T, i_s
    cdef double gamma = 0.5
    cdef double beta = 0.25
    cdef double m = 1.0
    cdef np.ndarray[np.float64_t, ndim=1] w = 2.0*3.1415926/period
    cdef np.ndarray[np.float64_t, ndim=1] c = 2.0*xi*m*w
    cdef np.ndarray[np.float64_t, ndim=1] k = m*w**2
    cdef np.ndarray[np.float64_t, ndim=1] k1 = k + gamma*c/beta/dt + m/beta/dt/dt
    cdef np.ndarray[np.float64_t, ndim=1] a = m/beta/dt + gamma*c/beta
    cdef np.ndarray[np.float64_t, ndim=1] b = 0.5*m/beta + dt*(gamma*0.5/beta - 1)*c
    
    cdef np.ndarray[np.float64_t, ndim=1] p = np.zeros(Np, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] dp = np.zeros(Np-1, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] SD = np.zeros(Nt, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] PSV = np.zeros(Nt, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] PSA = np.zeros(Nt, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] SV = np.zeros(Nt, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] SA = np.zeros(Nt, dtype=float)

    cdef np.ndarray[np.float64_t, ndim=1] dp1 = np.zeros(Np-1, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] u = np.zeros(Np, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] du = np.zeros(Np-1, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] du1 = np.zeros(Np-1, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] du2 = np.zeros(Np-1, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] u1 = np.zeros(Np, dtype=float)
    cdef np.ndarray[np.float64_t, ndim=1] u2 = np.zeros(Np, dtype=float)
 
    for i_T in range(Nt):
        p = -m*acc
        dp = np.diff(p)
        
        for i_s in range(Np-1):
            dp1[i_s] = dp[i_s] + a[i_T]*u1[i_s] + b[i_T]*u2[i_s]
            du[i_s] = dp1[i_s]/k1[i_T]
            du1[i_s] = gamma*du[i_s]/beta/dt - gamma*u1[i_s]/beta + dt*(1.0-0.5*gamma/beta)*u2[i_s]
            du2[i_s] = du[i_s]/beta/dt/dt - u1[i_s]/beta/dt - 0.5*u2[i_s]/beta
            u[i_s+1] = u[i_s] + du[i_s]
            u1[i_s+1] = u1[i_s] + du1[i_s]
            u2[i_s+1] = u2[i_s] + du2[i_s]
        
        SD[i_T] = np.max(np.abs(u))
        PSV[i_T] = SD[i_T]*w[i_T]
        PSA[i_T] = PSV[i_T]*w[i_T]
        SV[i_T] = np.max(np.abs(u1))
        SA[i_T] = np.max(np.abs(u2+acc))

    return SD, PSV, PSA, SV, SA


import numpy as np
from scipy.signal import butter, lfilter
#import matplotlib.pyplot as plt

def read_nga(filename): # Read nga format strong motion data and return time and acceleration
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()
    header = lines[0:4]
    data = lines[4:]
    N_samples = int(header[3].split()[0])
    dt = np.float32(header[3].split()[1])
    #time = dt*np.linspace(0,N_samples-1, N_samples).round(decimals=8)
    acc = ()
    for line in data:
        acc=np.append(acc, np.array(line.split(), dtype=float))
    
    return dt, acc

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    #z, p, k = butter(order, [low, high], btype='band', output='zpk')
    return b, a
    #return z, p, k

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    # This can be unstable
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    #y = filtfilt(b, a, data)
    return y

def Response_Spectra(acc, dt, xi, period):
    gamma = 0.5
    beta = 0.25
    
    m = 1.0
    w = 2.0*np.pi/period
    c = 2.0*xi*m*w
    k = m*w**2
    k1 = k + gamma*c/beta/dt + m/beta/dt/dt
    a = m/beta/dt + gamma*c/beta
    b = 0.5*m/beta + dt*(gamma*0.5/beta - 1)*c
    Np = acc.size
    Nt = period.size
    SD = np.zeros(Nt)
    PSV = np.zeros(Nt)
    PSA = np.zeros(Nt)
    SV = np.zeros(Nt)
    SA = np.zeros(Nt)
    for i_T in np.arange(Nt):
        p = -m*acc
        dp = np.diff(p)
        dp1 = np.zeros(Np-1)
        u=np.zeros(Np)
        du=np.zeros(Np-1)
        du1=np.zeros(Np-1)
        du2=np.zeros(Np-1)
        u1=np.zeros(Np)
        u2=np.zeros(Np)
        for i_s in np.arange(Np-1):
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

def CumArias(acc, dt):
    Ia = np.pi/2.0/9.81*np.cumsum(acc**2.0)*dt

    return Ia

def ricker(f0, t0, time):
# Generate a ricker wavelet with the central frequency 'f0'
# position at time 't0'
# time is the time vector
     w=(1-2*(np.pi*f0*(time-t0))**2)*np.exp(-(np.pi*f0*(time-t0))**2);
     return w

#def husid(acc, dt):

           
    
#impulse = np.zeros(2048)
#impulse[256] = 1.0

#dt=0.01
#xi=0.05
#T=np.linspace(0.1,10,100)

#SD, PSV, PSA, SV, SA = response_spectra(impulse, dt, xi, T)
        

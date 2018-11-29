#!/usr/local/bin/python3
import numpy as np

class Spline():
    def __init__(self, x=None, func=None):
        if ((x is None) and (func is None)):
            return
        if ((x is None) or (func is None)):
            raise ValueError()
        T = np.diff(x)
        N = T.shape[0]
        A = np.zeros((N-1, N-1))
        f = np.zeros(N - 1)
        func_diff = np.diff(func)
        for i in range(N - 1):
            A[i][i] = (T[i] + T[i+1]) / 3
            if (i != 0):
                A[i][i-1] = T[i] / 6
            if (i != N-2):
                A[i][i+1] = T[i+1] / 6
            f[i] = (func[i+2]-func[i+1]) / T[i+1] - (func[i+1]-func[i])/T[i]
        self.m = self.thomas(A, f)
        self.m = np.append(self.m, np.zeros(1))
        self.m = np.append(np.zeros(1), self.m)
        m_diff = np.diff(self.m)
        self.a = func_diff / T - T * m_diff / 6
        self.b = func[:-1]-self.m[:-1]*T*T/6-self.a*x[:-1]
        self.t = x
    
    def thomas(self, A, f):
        N = f.shape[0]
        if (N == 1):
            return f[0] / A[0][0]
        p = np.zeros(N)
        q = np.zeros(N)
        X = np.zeros(N)
        p[1] = -A[0][1]/A[0][0]
        q[1] = f[0] / A[0][0]
        for i in range(1, N-1):
            p[i+1] = -A[i][i+1]/(A[i][i-1]*p[i]+A[i][i])
            q[i+1] = (f[i]-A[i][i-1]*q[i])/(A[i][i-1]*p[i]+A[i][i])
        X[N-1] = (f[N-1]-A[N-1][N-2]*q[N-1])/(A[N-1][N-2]*p[N-1]+A[N-1][N-1])
        for i in range(N-2, -1, -1):
            X[i] = p[i+1]*X[i+1]+q[i+1]
        return X
    
    def write_cef(self):
        return self.t, self.m, self.a, self.b
    
    def read_cef(self, t, m, a, b):
        self.t = t
        self.m = m
        self.a = a
        self.b = b
    
    def __call__(self, x_real):
        f_s = np.zeros(x_real.shape[0])
        for i in range(x_real.shape[0]):
            n = -1
            for j in range(self.t.shape[0] - 1):
                if ((x_real[i] >= self.t[j]) and (x_real[i] <= self.t[j+1])):
                    n = j
                    break
            T = self.t[n + 1] - self.t[n]
            f_s[i] = 1/6/T*(self.m[n]*(self.t[n+1] - x_real[i])**3+self.m[n+1]*(x_real[i] - self.t[n])**3)+self.a[n]*x_real[i]+self.b[n]
        return f_s

import numpy as np
from scipy.sparse import hstack, vstack, coo_matrix
from math import *
from timeit import timeit

class CQT :
    def __init__(self, fmin, fmax, bins, fs, wnd) :
        self.eps = 1e-3
        self.fmin = fmin
        self.fmax = fmax
        self.bins = bins
        self.wnd  = wnd
        self.fs = fs
        self.Q = 1 / (pow(2, 1.0 / bins) - 1)
        K = int(ceil(bins * log(fmax / fmin) / log(2)))
        # print 'K:', K
        self.fftlen = int(pow(2, ceil(log(self.Q * fs / fmin) / log(2))))
        return 
        self.ker = []
        print '[CQT] Initializing...', fmin, fmax, bins, fs, self.fftlen, self.Q
        for k in range(K, 0, -1) :
            N = ceil(self.Q * fs / (fmin * pow(2, (k - 1.0) / bins)))
            tmpKer = wnd(N) * np.exp(2 * pi * 1j * self.Q * np.arange(N) / N) / N;
            ker = np.fft.fft(tmpKer, self.fftlen)
            print '[CQT] Running...', k
            ker = np.select([abs(ker) > self.eps], [ker])
            print np.sum(ker > self.eps)
            self.ker += [coo_matrix(ker, dtype = np.complex128)]
        # print 'shape:', hstack(self.ker).tocsc().shape
        self.ker.reverse()
        self.ker = vstack(self.ker).tocsc().transpose().conj() / self.fftlen
        print '[CQT] Initialized OK.'

    def fast_pp(self, x) :
        # print self.ker.shape, np.fft.fft(x, self.fftlen).shape
        return (np.fft.fft(x, self.fftlen).reshape(1, self.fftlen) * self.ker)[0]

    def fast(self, x) :
        x = np.array(x)
        print x.shape
        cq = []
        for k in range(1, int(ceil(self.bins * log(self.fmax / self.fmin) / log(2))) + 1) :
            N = int(ceil(self.Q * self.fs / (self.fmin * pow(2, (k - 1.0) / self.bins))))
            xl = min(len(x), N)
            # print x[:N].shape, (wnd(N) * np.exp(2 * pi * 1j * np.arange(N) / N) / N).shape
            cq += [x[:xl].dot((self.wnd(N, xl) * np.exp(-2 * pi * 1j * self.Q * np.arange(xl) / N) / N)[:xl])]
            
        # return np.array(cq)
        cq = map(abs,cq)
        print '[CQT] Done.'
        return cq

def hamming(length, xl) :
    return 0.54 - 0.46 * np.cos(2 * pi * np.arange(xl) / length)

# np.arange()
def test() :
    global drd
    length = 44100
    x = np.random.random(length)
    drd = CQT(40, 22050, 12, 44100, hamming)
    
    # y, z = drd.fast(x), drd.slow(x)
    y = drd.fast(x)
    print 'Benchmark the `EFFICIENT` method:'
    #timeit('y = drd.fast(x)')

    print 'Benchmark the `BRUTE-FORCE` method:'
    #timeit('z = drd.slow(x)')

    # print 'The difference: ', max(abs(z - y))



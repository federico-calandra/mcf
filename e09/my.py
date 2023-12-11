import numpy
import pandas
import matplotlib.pyplot
from scipy import fft

def info(x):
    print('********************')
    print('print: ', x)
    print('type : ', type(x))

    if isinstance(x, list):
        print('len: ', len(x))
        
    if isinstance(x, tuple):
        print('len: ', len(x))
        
    if isinstance(x, dict):
        print('len: ', len(x))
        print('keys: ', list(x))        
        
    if isinstance(x, numpy.ndarray):
        print('shape: ', x.shape)
        
    if isinstance(x, pandas.core.frame.DataFrame):
        print('n rows: ', len(x))
        print('n cols: ', len(x.columns))
        
    if isinstance(x, matplotlib.figure.Figure):
        pass
    
    if isinstance(x, matplotlib.axes._axes.Axes):
        pass
    
    print('********************')
    print()
    
    
def fourier(seq):
    # FFT
    fft_seq=fft.rfft(seq)
    freq1=0.5*fft.rfftfreq(len(seq))
    freq2=0.5*fft.rfftfreq(len(fft_seq))
    pwsp=numpy.absolute(fft_seq)**2
    # GRAFICI
    fig,ax=matplotlib.pyplot.subplots(1,3)
    ax[0].plot(freq1[:len(pwsp)//2], pwsp[:len(pwsp)//2])
    ax[1].semilogy(freq1[:len(pwsp)//2], pwsp[:len(pwsp)//2])
    ax[2].loglog(freq1[:len(pwsp)//2], pwsp[:len(pwsp)//2], '.')
    ax_style=[{'title':'linear'}, {'title':'semilogy'}, {'title':'loglog'}]
    ax[0].set(**ax_style[0])
    ax[1].set(**ax_style[1])
    ax[2].set(**ax_style[2])
    return fft_seq,freq1,pwsp,(fig,ax)

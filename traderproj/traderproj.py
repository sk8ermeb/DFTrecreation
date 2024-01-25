

from ftplib import parse150
import matplotlib.pyplot as plt
import time
from threading import Thread
import numpy as np
from matplotlib.backend_bases import MouseButton
import random
import math
import matplotlib
#matplotlib.use('TkAgg')
def runplot(data):
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.ylabel(data)
    plt.show()


totalpts = 100
start = 50

x = np.linspace(0, totalpts, totalpts)
xfft = np.linspace(0, int(totalpts/2), int(totalpts/2))
#x = np.linspace(0, 6*np.pi, 100)
cnt = 0
y = [start]
while(cnt < totalpts - 1):
    cnt += 1
    diff = random.random()
    diff = diff*diff*diff*3
    if(random.randint(0, 1)):
        diff *= -1
    start += diff
    y.append(start)
#y = np.sin(x)

#print(x)
#print(y)
#print(len(x))
#print(len(y))



handle = plt.ion()
fig = plt.figure()
ax = fig.add_subplot(311)
line1, = ax.plot(x, y, 'r-')


line1.set_ydata(y)
#fig.canvas.draw()
#fig.canvas.flush_events()

dft = np.fft.rfft(y)


absdft = []
phasedft = []

cnt= 0
while(cnt < totalpts/2):
    imag = dft[cnt].imag
    real = dft[cnt].real
    absdft.append(math.sqrt((imag*imag) + (real*real)))
    phasedft.append(math.atan2(imag,real))
    cnt +=1


#print(absdft)
#print(phasedft)
abdpad = []
cnt = 0
while(cnt < totalpts/2):
    abdpad.append(absdft[cnt])
    cnt +=1
cnt = 0
while(cnt < totalpts/2):
    abdpad.append(0)
    cnt +=1
ax2 = fig.add_subplot(313)
line2, = ax2.plot(xfft, absdft, 'r+')
line2.set_ydata(absdft)
ax2.set_ylim(0, 100)
#fig.canvas.flush_events()
#fig.canvas.draw()

dftout = []
cnt=0
while(cnt <totalpts/2):    
    dftout.append((cnt, absdft[cnt],phasedft[cnt] ))
    cnt +=1
dftoutf = []
cnt=0
while(cnt <totalpts/2):
    cntn = 0
    indexm = 0
    peak = dftout[cntn][1]
    while(cntn < len(dftout)):
        if(dftout[cntn][1] > peak):
            peak = dftout[cntn][1]
            indexm = cntn
        cntn +=1
    dftoutf.append(dftout.pop(indexm))
    cnt +=1
print("ordered dft out")
print(dftoutf)
dftline = []

cnt=0
while(cnt<totalpts):
    yval = 0
    ycnt = 0
    #while(ycnt < len(absdft)):
    while(ycnt < 1):
        if(ycnt == -1):
            yval += absdft[ycnt]/totalpts
        else:
            yval += absdft[ycnt]*math.cos((ycnt*cnt*2*math.pi/(totalpts)) + phasedft[ycnt])/totalpts
        ycnt +=1
    dftline.append(yval)
    cnt +=1


ax3 = fig.add_subplot(312)
line3, = ax3.plot(x, dftline, 'r-')
line3.set_ydata(dftline)

indexes = 1

def on_press(event):
    global indexes
    global line3
    global fig
    #print('press', event.key)
    if event.key == 'up' and (indexes < int(totalpts/2)-1):
        indexes +=1        
    if event.key == 'down' and indexes > 1:
        indexes -=1
    print(indexes)
    dftline = []

    cnt=0
    while(cnt<totalpts):
        yval = 0
        ycnt = 0
        #while(ycnt < len(absdft)):
        while(ycnt < indexes):
            if(ycnt == -1):
                yval += absdft[ycnt]/totalpts
            else:
                yval += absdft[ycnt]*math.cos((ycnt*cnt*2*math.pi/(totalpts)) + phasedft[ycnt])/totalpts
            ycnt +=1
        dftline.append(yval)
        cnt +=1
    ax3.clear()
    line3, = ax3.plot(x, dftline, 'r-')
    line3.set_ydata(dftline)
    fig.canvas.flush_events()
    fig.canvas.draw()


def on_click(event):
    if event.button is MouseButton.LEFT:
        print('left button clicked')
fig.canvas.mpl_connect('key_press_event', on_press)
fig.canvas.mpl_connect('button_press_event', on_click)



fig.canvas.flush_events()
fig.canvas.draw()
a = input("sdfsdf")
#for phase in np.linspace(0, 10*np.pi, 500):
#    line1.set_ydata(np.sin(x + phase))
#    fig.canvas.draw()
#    fig.canvas.flush_events()
#    time.sleep(0.1)


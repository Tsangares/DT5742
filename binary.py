from util.caen import *
import os
import statistics as stats
from numpy import polyfit,linspace

def getCritialPoints(waveform,threshold):
    if not issubclass(type(waveform),list) or len(waveform) <= 1:
        raise Exception("Waveform must be a list of points")
    critialPoints=[]
    for i,b in enumerate(waveform):
        if i == 0: continue
        a=waveform[i-1]
        crossValue=cross(a,b,threshold)
        if abs(crossValue) == 1:
            critialPoints.append((i-1,crossValue))
    return critialPoints

def cross(a,b,threshold):
    if a < threshold and b > threshold:
        return 1
    if a > threshold and b < threshold:
        return -1
    else: return 0

def getPulse(waveform,polarity=1):
    width=getPulseWidth(waveform,polarity)
    if width[1]-width[0] == 1:
        threshold=getGentleThreshold(waveform,polarity)
        width=getPulseWidth(waveform,polarity,threshold)
        #As an alternative you could try a different window.
    plt.plot(waveform[width[0]:width[1]],linestyle="None",marker='.')
    plt.xlabel('Time (index)')
    plt.ylabel('Voltage (V)')
    plt.title("Example of an extracted pulse from a waveform")
    plt.plot()
    plt.show()
    return waveform[width[0]:width[1]]

def getPulseWidth(waveform,polarity=1,threshold=None):
    if threshold is None:
        threshold=getAgressiveThreshold(waveform,polarity)
    polarity=polarity/abs(polarity)
    cp=getCritialPoints(waveform,threshold)
    width=None
    skips=0
    for index,criticalPoint in enumerate(cp):
        if index == 0: continue
        currentIndex,currentSlope=criticalPoint
        lastIndex,lastSlope=cp[index-1]
        if lastSlope == 1*polarity and currentSlope == -1*polarity:
            width=(lastIndex,currentIndex)
            #if currentIndex-lastIndex==1: continue
            break
    if width is None:
        raise Exception("No pulse found.")
    return width

def getGentleThreshold(waveform,polarity=1):
    width=getPulseWidth(waveform,polarity=-1,threshold=stats.mean(waveform))
    return max(waveform[width[0]+1:width[1]-1])

def getAgressiveThreshold(waveform,polarity=1):
    width=getPulseWidth(waveform,polarity=-1,threshold=stats.mean(waveform))
    return stats.mean(waveform[width[0]:width[1]])

def getSum(waveform):
    minimum=min(waveform)
    waveform=[w-minimum for w in waveform]
    return sum(waveform)

if __name__ == '__main__':
    CWD=os.getcwd()
    DATA_PATH=os.path.join(CWD,'binary')
    files=os.listdir(DATA_PATH)
    x=[]
    y=[]
    for filename in files[::-1]:
        filepath=os.path.join(DATA_PATH,filename)
        waveform=parseBinary(filepath)
        waveform=list(waveform[0])
        binary=filename.replace('.dat','')
        nPulses=sum([int(c) for c in binary])
        print(binary, int(binary,2))
        pulse=getPulse(waveform)
        summation=getSum(pulse)
        if summation < .1e8 and nPulses != 0:
            continue
            print(filename)
            plt.plot(range(len(waveform)),waveform,linestyle="None",marker='.')
            plt.plot(range(len(pulse)),pulse,linestyle="None",marker='.')
            plt.show()
        x.append(nPulses)
        y.append(summation)
    m,b=polyfit(x,y,1)
    plt.plot([0,8],[b,m*8+b],label="y=%.02e x + %.02e"%(m,b),color='y')
    plt.plot(x,y,linestyle="None",marker="8",color='m')
    plt.ylabel("Area Under the Pulse's Waveform (32 bit ADC Count)")
    plt.xlabel("Number of Pulses (N)")
    plt.title("Area of Various Pulse Bunches through the Spreader")
    plt.legend()
    plt.show()
    #plotEvent(data,1)
    
                


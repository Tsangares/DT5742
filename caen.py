import matplotlib.pyplot as plt
from numpy import fromfile,dtype
import ROOT
from array import array
import time,os,random
import sys
from statistics import mean
def parseBinary(filename, header=True, offset=None):
    with open(filename, mode='rb') as f:
        if not header:
            return fromfile(f,dtype=dtype("<f"),count=-1)
        d=fromfile(f,dtype=dtype("<f"),count=-1)
        trace=[]
        length=1030
        offset=6
        vOffset=0
        for i in range(len(d)//length):
            trace.append([float(w)/(2**12-1)+vOffset for w in d[i*length+offset:(i+1)*length]])
        return trace


def parseAscii(filename):
    with open(filename,mode='r') as f:
        return [float(n) for n in f.parse().split('\n')[:-1]]
def parse(filename):
    if '.dat' in filename[-4:]: return parseBinary(filename)
    else: return parseAscii(filename)


def checkTruncateOffset(data,truncate,offset):
    if offset >= len(data):
        offset=0
        print("offset %d greater than the size of the dataset %d."%(offset,len(data)))
    truncate=truncate+offset
    if truncate >= len(data) or truncate==-1: truncate=len(data)
    return truncate,offset

def plot(filename,truncate=1000,offset=0):
    data=parse(filename)
    truncate,offset=checkTruncateOffset(data,truncate,offset)
    plt.plot(range(truncate-offset),data[offset:truncate],linestyle='none',marker='.')
    return plt

def plotEvent(data,event=1):
    plt.plot(range(len(data[event])),data[event],linestyle="None",marker=".")
    plt.show()

def plotGrid(folder,mapping,plt=None):
    columns=max([len(l) for l in mapping])
    rows=len(mapping)
    files=sorted([(int(f[-7:-4].replace('e','').replace('_','')),os.path.join(folder,f)) for f in os.listdir(folder) if 'wave' in f])
    files=[f[1] for f in files]
    data=[parseBinary(f)[0] for f in files]
    if plt is None: plt=ROOT.TH2F('h3','Grid',columns,0,columns-1,rows,0,rows-1)
    unordered=[]
    for j in range(rows):
        for i in range(columns):
            digit=int(mapping[j][i])
            unordered.append(digit)
            mapping[j][i]=digit
    reverseMap=[None for i in range(max(unordered)+1)]
    index=0
    for j in range(rows):
        for i in range(columns):
            coord=int(mapping[j][i])
            reverseMap[coord]=(i,j)
            index+=1
    for index,datum in enumerate(data):
        if reverseMap[index] is not None:
            x,y=reverseMap[index]
            plt.SetBinContent(x+1,y+1,min(data[index]))
    ROOT.gStyle.SetOptStat(0)
    plt.Draw("COLZ")
    return plt
    
    
if __name__=='__main__':
    index=0
    mapFile="map.txt"
    if len(sys.argv) == 2:
        mapFile=sys.argv[1]
    with open(mapFile,'r') as f:
        lines=f.read().split('\n')
        mapping=[l.split(' ') for l in lines]
    averageColumn=mean([len(l) for l in mapping])
    mapping=[m for m in mapping if len(m) >= averageColumn]
    #dataPath=os.path.join(os.getcwd(),'1event_binary')
    dataPath=os.getcwd()
    plot=None
    while True:
        plot=plotGrid(dataPath,mapping,plot)
        print("Plot refreshed.",time.time())
        time.sleep(4)
        
    


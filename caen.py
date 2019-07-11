import matplotlib.pyplot as plt
from numpy import fromfile,dtype
from array import array
import seaborn as sns
import time,os,random
import sys,subprocess

def extractFieldInGroup(data,field,key):
    if issubclass(type(data),str): data=data.split('\n')
    found=False
    for i,d in enumerate(data):
        if field in d and '#' not in d:
            found=True
        if found and key in d:
            return d

def getOffset(filename,config='config.txt'):
    chan=getChan(filename)
    with open(config,'r') as f:
        configData=f.read().split('\n')
        group1=extractFieldInGroup(configData,'[0]','GRP_CH_DC_OFFSET').split(' ')[-1].split(',')
        group2=extractFieldInGroup(configData,'[1]','GRP_CH_DC_OFFSET').split(' ')[-1].split(',')
        offsets=[float(o) for o in group1+group2]
        dc_offset=offsets[chan]/50
        return dc_offset

def parseBinary(filename, header=True, offset=None, readConfig=True):
    with open(filename, mode='rb') as f:
        if not header:
            return fromfile(f,dtype=dtype("<f"),count=-1)
        d=fromfile(f,dtype=dtype("<f"),count=-1)
        trace=[]
        dc_offset=0
        if readConfig:
            dc_offset=getOffset(filename)
        length=1030
        offset=6
        for i in range(len(d)//length):
            trace.append([float(w)/(2**12-1)+dc_offset for w in d[i*length+offset:(i+1)*length]])
            #trace.append([float(w) for w in d[i*length+offset:(i+1)*length]])
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

def getChan(filename):
    return int(filename[-7:-4].replace('e','').replace('_',''))
def plotGrid(folder,mapping,plot=None):
    columns=max([len(l) for l in mapping])
    rows=len(mapping)
    files=sorted([(getChan(f),os.path.join(folder,f)) for f in os.listdir(folder) if '.dat' in f and 'wave' in f])
    files=[f[1] for f in files]
    data=[min(parseBinary(f)[-1]) for f in files]
    img=[[-1 for i in range(columns)] for j in range(rows)]
    for j in range(rows):
        for i in range(columns):
            chan=int(mapping[j][i])-1
            num=data[chan]
            img[j][i]=num
    fig=plt.figure()
    timer=fig.canvas.new_timer(interval=4000)
    timer.add_callback(lambda: plt.close())
    timer.start()
    #plt.imshow(img,cmap='hot')
    sns.heatmap(img, linewidth=0.5)
    plt.savefig('static/heatmap.png')
    #plt.show()

from flask import Flask
from multiprocessing import Process
app = Flask(__name__)
@app.route('/')
def hello():
    make2D()
    return app.send_static_file('index.html')

def startWeb():
    app.run(host='0.0.0.0',port='8888')

def make2D():
    mapFile="map.txt"
    if len(sys.argv) == 2:
        mapFile=sys.argv[1]
    with open(mapFile,'r') as f:
        lines=f.read().split('\n')
        mapping=[l.split(' ') for l in lines]
    a=[len(l) for l in mapping]
    averageColumn=sum(a)/len(a)
    mapping=[m for m in mapping if len(m) >= averageColumn]
    dataPath=os.getcwd()
    plot=None

    plot=plotGrid(dataPath,mapping,plot)
    print("Plot refreshed.",time.time())
if __name__=='__main__':
    p=Process(target=startWeb)
    p.start()
    time.sleep(1)
    p2=subprocess.Popen('start firefox localhost:8888',shell=True)

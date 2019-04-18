import matplotlib.pyplot as plt
from numpy import fromfile,dtype

def parseBinary(filename):
    with open(filename, mode='rb') as f:
        return fromfile(f,dtype=dtype("<I"),count=-1)
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


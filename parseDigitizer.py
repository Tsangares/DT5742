#!/
import matplotlib.pyplot as plt
from numpy import fromfile,dtype


def parseBinary(filename):
    with open(filename, mode='rb') as f:
        rawBinary=fromfile(f,dtype=dtype("<f"),count=-1)
        lenEvent=1030 #Length of an event
        lenHeader=6   #Length of the header info
        nEvents=len(rawBinary)//lenEvent
        
        #Seperate traces
        traces=[ [float(adc) for adc in rawBinary[i*lenEvent+lenHeader:(i+1)*lenEvent]] for i in range(nEvents) ]
        return traces

def plotEvent(data,event=1):
    plt.plot(range(len(data[event])),data[event],linestyle="None",marker=".")
    plt.show()

def extractChannel(filename):
    try:
        return int(filename[-7:-4].replace('e','').replace('_',''))
    except:
        print("Could not parse the channel number")
        return None
        
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parse and view the output data from the Caen Digitizer DT5742.')
    parser.add_argument('filename', type=str, help='The path to a single data file produced by the digitizer.')
    parser.add_argument('-e','--event', metavar='event', type=int, help='The index of the event you want returned. If you do not enable this it will return all the events.',default=0)
    args = parser.parse_args()
    print("Opening",args.filename)
    events=parseBinary(args.filename)
    chan=extractChannel(args.filename)
    print('This is channel {} and there are {} events.'.format(chan,len(events)))
    print("Plotting event",args.event)
    plotEvent(events,args.event)
    
    

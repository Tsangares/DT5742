from reader import readWavedump
import os,sys
from statistics import *
import matplotlib.pyplot as plt

if __name__=='__main__':
    filename=sys.argv[1]
    points=readWavedump(filename)
    midpoint=(max(points)-min(points))/2+min(points)
    last=None
    totalUp=0
    totalDown=0
    uninteresting=0
    for i,point in enumerate(points):
        if last is None: last=point
        elif point > midpoint and last < midpoint: totalUp+=1
        elif point < midpoint and last > midpoint: totalDown+=1
        else: uninteresting += 1
        last=point
    print("Total up: %d"%totalUp)
    print("Total down: %d"%totalDown)
    print("Total uninteresting: %d"%uninteresting)
    if len(sys.argv)==3: print("HZ: %.02f"%(totalUp/float(sys.argv[2])))

        
    
    

import struct,numpy

def readBinaryWavedump(filename):
    with open(filename, mode='rb') as f:
        #content=f.read()
        #data=list(struct.unpack('I'*(len(content)//4),content))
        data=numpy.fromfile(f,dtype=numpy.dtype("<I"),count=-1)
        return [int(n) for n in data]

def readAsciiWavedump(filename):
    with open(filename,mode='r') as f:
        data=f.read().split('\n')
        return [float(n) for n in data[:-1]]
    
def readWavedump(filename):
    if '.dat' in filename[-4:]:
        return readBinaryWavedump(filename)
    else:
        return readAsciiWavedump(filename)

if __name__=='__main__':
    from sys import argv
    if len(argv) == 3:
        from json import dumps
        data=readWavedump(argv[1])
        with open(argv[2], 'w+') as f:
            f.write(json.dumps(data))
        print("Wrote %d elements to %s."%(len(data),argv[2]))
    elif len(argv) == 2:
        import matplotlib.pyplot as plt
        data=readWavedump(argv[1])
        print("Data parsed, plotting first 1000 events.")
        truncate=1000
        if len(argv)==3: tuncate=int(argv[2])
        plt.plot(range(truncate),data[:truncate],linestyle='none',marker='.')
        plt.show()
    else:
        print("Either import %s, or use it like: python %s [src] [dest]"%(argv[0],argv[0]))
              

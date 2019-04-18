import reader,os,sys
import matplotlib.pyplot as plt

def lsGrep(path, contains):
    return [dir for dir in os.listdir(path) if contains in dir]

if __name__=='__main__':
    if len(sys.argv) >= 3:
        truncate=int(sys.argv[2])
    else:
        truncate=1000
    print("Truncating at %d"%truncate)
    data=reader.readWavedump(sys.argv[1])
    if truncate > len(data) or truncate == -1: truncate=len(data)
    plt.plot(range(truncate),data[:truncate],linestyle='none',marker='.')
    FOLDER="/tmp/www/"
    FILE=os.path.join(FOLDER,"img.png")
    if not os.path.isdir(FOLDER):
        os.mkdir(FOLDER)
    plt.show()
    #plt.savefig(FILE)
    #print("saved at %s"%FILE)
    
        
    


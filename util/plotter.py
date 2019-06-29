import caen,argparse

if __name__=='__main__':
    DESC="Command line utility to plot binary or ascii output from wavedump."
    parser=argparse.ArgumentParser(description=DESC)
    parser.add_argument('filename',type=str,nargs=1,help="The name of the file to open.")
    parser.add_argument('-t','-n','--truncate',dest='truncate',metavar='truncate',type=int,nargs="?",help="The number of points to plot.",default=1000)
    parser.add_argument('-o','--offset',dest='offset',metavar='offset',type=int,nargs="?",help="The number of points to initially skip.",default=0)
    args=parser.parse_args()
    plt=caen.plot(args.filename[0],args.truncate,args.offset)
    plt.show()
    
        
    


import caen,argparse,json

if __name__=='__main__':
    DESC="Command line utility to convert a wavedump binary file to json."
    parser=argparse.ArgumentParser(description=DESC)
    parser.add_argument('readFilename',type=str,nargs=1,help="The name of the file to open.")
    parser.add_argument('writeFilename',type=str,nargs=1,help="The name of the file to write to.")
    parser.add_argument('-t','-n','--truncate',dest='truncate',metavar='truncate',type=int,nargs="?",help="The number of points to plot.",default=-1)
    parser.add_argument('-o','--offset',dest='offset',metavar='offset',type=int,nargs="?",help="The number of points to initially skip.",default=0)
    args=parser.parse_args()
    data=caen.parse(args.readFilename[0])
    truncate,offset=caen.checkTruncateOffset(data,args.truncate,args.offset)
    with open(args.writeFilename[0], mode='w+') as f:
        f.write(json.dumps([int(n) for n in data][offset:truncate]))
    print("Wrote %d elements from %s to %s."%(truncate-offset,args.readFilename,args.writeFilename))
              

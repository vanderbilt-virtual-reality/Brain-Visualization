import os
import sys
import numpy as np
from pynrrd import *

def main():
    print('Hello')
    if len(sys.argv) >=2:
        pathToFile = sys.argv[1]
        print('dir to nrrd is ', pathToFile)
        data, header=read(pathToFile,index_order='C')
        #convert type
        data=data*10**15
        data=data.astype(np.int64)
        if not os.path.exists('.\\Assets\\tmp'):
            os.mkdir('.\\Assets\\tmp')
        np.save('.\\Assets\\tmp/sample.npy', data)
    else:
        print ('Required to specify path to nrrd')
    return 0
 
 
if __name__=='__main__':
    main()
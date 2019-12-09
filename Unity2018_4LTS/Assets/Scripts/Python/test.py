import sys
import numpy as np

def main():
    print('Hello')
    if len(sys.argv) >=3:
        x = sys.argv[1]
        y = sys.argv[2]
        # print concatenated parameters
        print(x+y)
        x=int(x)
        y=int(y)
        #print parameter in num sum
        print(x+y)
    a=np.array(range(10))
    print (a)
    return 666
 
 
if __name__=='__main__':
    main()